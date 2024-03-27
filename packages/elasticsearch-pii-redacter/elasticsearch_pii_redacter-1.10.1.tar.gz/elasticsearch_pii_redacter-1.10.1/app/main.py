"""Main app definition"""
# pylint: disable=broad-exception-caught
import logging
from es_client.helpers.config import get_client
from app import elastic_api
from app.exceptions import FatalException, MissingIndex
from app.helpers import end_it, get_redactions
from app.tracking import Job, Task
from app.redacters import RedactIndex
from app.version import __version__

class Main:
    """It's the main class"""

    def __init__(self, ctx, redactions, tracking_index, dry_run=False):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Redactions file: %s', redactions)
        self.counter = 0

        try:
            self.client = get_client(configdict=ctx.obj['configdict'])
        except Exception as exc:
            raise FatalException('Unable to establish connection to Elasticsearch!') from exc

        self.redactions = get_redactions(redactions)
        self.tracking_index = tracking_index
        self.dry_run = dry_run

    def verify_doc_count(self, job):
        """Verify that expected_docs and the hits from the query have the same value

        :param job: The job object for the present redaction run

        :type job: :py:class:`~.app.tracking.Job`

        :rtype: None
        :returns: No return value
        """
        task = Task(job, task_id=f'PRE---{job.name}---DOC-COUNT-VERIFICATION')
        success = False
        errors = False
        if task.finished():
            return True # We're done already
        # Log task start
        task.begin()
        hits = elastic_api.get_hits(self.client, job.config['pattern'], job.config['query'])
        msg = f'{hits} hit(s)'
        self.logger.debug(msg)
        task.add_log(msg)
        self.logger.info("Checking expected document count...")
        zeromsg = (
            f"For index pattern {job.config['pattern']}, with query {job.config['query']} "
            f"'expected_docs' is {job.config['expected_docs']} but query results "
            f"is {hits} matches."
        )
        if job.config['expected_docs'] == hits:
            msg = f'Query result hits: {hits} matches expected_docs: {job.config["expected_docs"]}'
            self.logger.debug(msg)
            task.add_log(msg)
            success = True
            if hits == 0:
                self.logger.critical(zeromsg)
                self.logger.info('Continuing to next configuration block (if any)')
                success = False
        else:
            self.logger.critical(zeromsg)
            self.logger.info('Continuing to next configuration block (if any)')
        if not success:
            errors = True
            task.add_log(zeromsg)
        task.end(success, errors=errors)
        return success

    def iterate_indices(self, job):
        """Iterate over every index in job.indices"""
        all_succeeded = True
        for idx in job.indices:
            task = Task(job, index=idx, id_suffix='PARENT-TASK')
            # First check to see if idx has been touched as part of a previous run
            if task.finished():
                continue # This index has already been verified
            task.begin()
            task_success = False
            try:
                msg = f'Iterating per index: Index {idx} of {job.indices}'
                self.logger.debug(msg)
                task.add_log(msg)
                redact = RedactIndex(idx, job, self.counter)
                redact.run()
                task_success = redact.success
                self.counter = redact.counter
                self.logger.debug('RESULT: %s', task_success)
            except (MissingIndex, FatalException) as exc:
                self.logger.critical(exc)
                raise FatalException from exc
            end_it(task, task_success)
            if not task.completed:
                all_succeeded = False
                job.add_log(f'Unable to complete task {task.task_id}')
        return all_succeeded

    def iterate_configuration(self):
        """Iterate over every configuration block in self.redactions"""
        self.logger.debug('Full redactions object from config: %s', self.redactions)
        for config_block in self.redactions['redactions']:
            job_success = True
            # Reset counter to zero for each full iteration
            self.counter = 0
            if self.dry_run:
                self.logger.info("DRY-RUN MODE ENABLED. No data will be changed.")

            # There's really only 1 root-level key for each configuration block, and that's job_id
            job_name = list(config_block.keys())[0]
            job = Job(
                self.client, self.tracking_index, job_name, config_block[job_name],
                dry_run=self.dry_run)
            if job.finished():
                continue
            job.begin()
            if not self.verify_doc_count(job):
                # This configuration block can't go further because of the result mismatch
                job_success = False
                end_it(job, job_success)
                continue

            job_success = self.iterate_indices(job)
            # At this point, self.counter should be equal to total, indicating that we matched
            # expected_docs. We should therefore register that the job was successful, if we have
            # reached this point with no other errors having interrupted the process.

            end_it(job, job_success)

    def run(self):
        """Do the thing"""
        self.logger.info('PII scrub initiated')
        self.iterate_configuration()
