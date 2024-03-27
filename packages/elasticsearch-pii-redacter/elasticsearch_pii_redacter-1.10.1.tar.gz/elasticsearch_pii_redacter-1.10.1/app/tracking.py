"""Functions for creating & updating the progress/status update doc in Elasticsearch"""
# pylint: disable=broad-exception-caught, too-many-arguments, too-many-instance-attributes, missing-function-docstring
import logging
from app.defaults import index_settings, status_mappings
from app import elastic_api
from app.exceptions import FatalException, MissingDocument, MissingIndex, ResultNotExpected
from app.helpers import now_iso8601, parse_job_config

MOD = __name__

class Job:
    """Class to manage a redaction job"""
    ATTRLIST = ['start_time', 'completed', 'end_time', 'errors', 'logs']
    def __init__(self, client, index, name, config, dry_run=False):
        self.logger = logging.getLogger(f'{MOD}.{self.__class__.__name__}')
        self.client = client
        self.index = index
        self.name = name
        self.file_config = config
        self.dry_run = dry_run
        self.prev_dry_run = False
        self.cleanup = []
        try:
            # If the index is already existent, this function will log that fact and return cleanly
            elastic_api.create_index(
                client, index, settings=index_settings(), mappings=status_mappings())
        except ResultNotExpected as exc:
            self.logger.critical(exc)
            raise FatalException from exc
        self.get_history()

    @property
    def config(self):
        return self._config

    @property
    def indices(self):
        return self._indices

    @property
    def total(self):
        return self._total

    @property
    def status(self):
        return self._status

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def completed(self):
        return self._completed

    @property
    def errors(self):
        return self._errors

    @property
    def logs(self):
        return self._logs

    @config.setter
    def config(self, value):
        self._config = value

    @indices.setter
    def indices(self, value):
        self._indices = value

    @total.setter
    def total(self, value):
        self._total = value

    @status.setter
    def status(self, value):
        self._status = value

    @start_time.setter
    def start_time(self, value):
        # self.logger.debug('Setting start_time to %s', value)
        self._start_time = value

    @end_time.setter
    def end_time(self, value):
        # self.logger.debug('Setting end_time to %s', value)
        self._end_time = value

    @completed.setter
    def completed(self, value):
        # self.logger.debug('Setting completed to %s', value)
        self._completed = value

    @errors.setter
    def errors(self, value):
        # self.logger.debug('Setting errors to %s', value)
        self._errors = value

    @logs.setter
    def logs(self, value):
        # self.logger.debug('Setting logs to %s', value)
        self._logs = value

    def add_log(self, value):
        """Append another entry to self.logs"""
        if self.logs is None:
            _ = []
            _.append(f'{now_iso8601()} {value}')
        else:
            _ = self.logs
            _.append(f'{now_iso8601()} {value}')
        self.logs = _

    def get_status(self, data):
        """Read the status keys from the data
        
        :param data: The raw contents of the job progress doc
        :type data: dict

        :returns: Dictionary of results extracted from data
        :rtype: bool
        """
        result = {}
        for key in self.ATTRLIST:
            if key in data:
                result[key] = data[key]
            else:
                result[key] = None
        if not result:
            self.logger.info('No execution status for job %s', self.name)
        if 'dry_run' in result:
            if result['dry_run']:
                self.logger.info('Prior record of job %s was a dry-run', self.name)
                self.prev_dry_run = True
        return result

    def update_status(self):
        """Update instance attribute doc with the current values"""
        contents = {}
        for val in self.ATTRLIST:
            contents[val] = getattr(self, val)
        self.status = contents

    def build_doc(self):
        """Build the dictionary which will be the written to the tracking doc

        :returns: The tracking doc dictionary
        :rtype: dict
        """
        doc = {}
        self.update_status()
        for key in self.ATTRLIST:
            doc[key] = self.status[key]
        if 'config' not in doc:
            doc['config'] = {}
        doc['job'] = self.name
        doc['join_field'] = 'job'
        doc['config'] = parse_job_config(self.config, 'write')
        doc['dry_run'] = self.dry_run
        if not self.dry_run:
            doc['cleanup'] = self.cleanup
        # self.logger.debug('Updated tracking doc: %s', doc)
        return doc

    def get_job(self):
        """Get any job history that may exist for self.name

        :rtype: dict
        :returns: The job object from the progress/status update doc
        """
        result = {}
        try:
            result = elastic_api.get_tracking_doc(self.client, self.index, self.name)
        except MissingDocument:
            self.logger.debug('Job tracking doc does not yet exist.')
            self.config = {}
            self.status = {}
            return
        except Exception as exc:
            self.logger.critical(exc)
            raise FatalException from exc
        try:
            self.config = parse_job_config(result['config'], 'read')
        except KeyError:
            self.logger.info('No configuration data for job %s', self.name)
            self.config = {}
        self.status = self.get_status(result)

    def launch_prep(self):
        """We don't need to do these actions until self.begin() calls this method"""
        if self.dry_run:
            msg = 'DRY-RUN: No changes will be made'
            self.logger.info(msg)
            self.add_log(msg)
        self.indices = list(elastic_api.get_index(self.client, self.config['pattern']))
        self.logger.debug('Indices from provided pattern: %s', self.indices)
        self.total = len(self.indices)
        self.logger.debug("Total number of indices to scrub: %s", self.total)

    def load_status(self):
        """Load prior status values (or not)"""
        for key in self.ATTRLIST:
            if self.prev_dry_run:
                # If our last run was a dry run, set each other attribute to None
                setattr(self, key, None)
            else:
                if key in self.status:
                    setattr(self, key, self.status[key])
                else:
                    setattr(self, key, None)

    def get_history(self):
        """
        Get the history of a job, if any. Ensure all values are populated from the doc, or None

        :rtype: None
        :returns: No return value
        """
        self.logger.debug('Pulling any history for job: %s', self.name)
        try:
            self.get_job()
        except MissingIndex as exc:
            self.logger.critical(exc)
            raise FatalException from exc
        if not self.config:
            self.logger.info('No stored config for job: %s. Using file-based config', self.name)
            self.config = self.file_config
        if not self.status:
            self.logger.debug('No event history for job: %s', self.name)
        self.load_status()

    def report_history(self):
        """
        Report the history of any prior attempt to run the Job
        Log aspects of the history here.

        :rtype: None
        :returns: No return value
        """
        prefix = f'The prior run of job: {self.name}'
        if self.prev_dry_run:
            self.logger.info('%s was a dry_run', prefix)
        if self.start_time:
            self.logger.info('%s started at %s', prefix, self.start_time)
        if self.completed:
            if self.end_time:
                self.logger.info('%s completed at %s', prefix, self.end_time)
            else:
                msg = 'is marked completed but did not record an end time'
                self.logger.warning('%s started at %s and %s', prefix, self.start_time, msg)
        if self.errors:
            self.logger.warning('%s encountered errors.', prefix)
            if self.logs:
                # Only report the log if a error is True
                self.logger.warning('%s had log(s): %s', prefix, self.logs)

    def begin(self):
        """Begin the job and record the current status

        :rtype: None
        :returns: No return value
        """
        self.logger.info('Beginning job: %s', self.name)
        self.launch_prep()
        self.start_time = now_iso8601()
        self.completed = False
        self.record()

    def end(self, state, errors=False, logmsg=None):
        """End the job and record the current status
        
        :param state: The completion status of the job
        :param errors: Errors encountered doing the job
        :param logs: Logs recorded doing the job (only if errors)

        :type state: bool
        :type errors: bool
        :type logs: str

        :rtype: None
        :returns: No return value
        """
        if self.dry_run:
            msg = f'DRY-RUN: Not recording snapshots that can be deleted: {self.cleanup}'
            self.logger.info(msg)
            self.add_log(msg)
        self.end_time = now_iso8601()
        self.completed = state
        self.errors = errors
        if logmsg:
            self.add_log(logmsg)
        self.record()
        self.logger.info('Job: %s ended. Completed: %s', self.name, state)

    def record(self):
        """Record the current status of the job

        :rtype: None
        :returns: No return value
        """
        doc = self.build_doc()
        try:
            elastic_api.update_doc(self.client, self.index, self.name, doc)
        except Exception as exc:
            self.logger.critical(exc)
            raise FatalException from exc

    def finished(self):
        """Check if a prior run was recorded for this job and log accordingly
        
        :rtype: bool
        :returns: State of whether a prior run failed to complete
        """
        if self.completed:
            if self.dry_run:
                self.logger.info(
                    'DRY-RUN: Ignoring previous successful run of job: %s', self.name)
            else:
                self.logger.info('Job %s was completed previously.', self.name)
                return True
        if self.start_time:
            self.report_history()
            self.logger.info('Restarting or resuming job: %s', self.name)
        return False

class Task:
    """An individual task item, tracked in Elasticsearch"""
    ATTRLIST = ['start_time', 'completed', 'end_time', 'errors', 'logs']
    def __init__(self, job, index=None, id_suffix=None, task_id=None):
        self.logger = logging.getLogger(f'{MOD}.{self.__class__.__name__}')
        self.job = job
        if task_id:
            self.task_id = task_id
        elif not id_suffix or not index:
            raise FatalException('task_id, or both index and id_suffix must be provided')
        else:
            self.task_id = f'{index}---{id_suffix}'
        self.index = index
        self.doc_id = None
        self.get_history()

    @property
    def status(self):
        return self._status

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def completed(self):
        return self._completed

    @property
    def errors(self):
        return self._errors

    @property
    def logs(self):
        return self._logs

    @status.setter
    def status(self, value):
        self._status = value

    @start_time.setter
    def start_time(self, value):
        # self.logger.debug('Setting start_time to %s', value)
        self._start_time = value

    @end_time.setter
    def end_time(self, value):
        # self.logger.debug('Setting end_time to %s', value)
        self._end_time = value

    @completed.setter
    def completed(self, value):
        # self.logger.debug('Setting completed to %s', value)
        self._completed = value

    @errors.setter
    def errors(self, value):
        # self.logger.debug('Setting errors to %s', value)
        self._errors = value

    @logs.setter
    def logs(self, value):
        # self.logger.debug('Setting logs to %s', value)
        self._logs = value

    def add_log(self, value):
        """Append another entry to self.logs"""
        if not self.logs:
            _ = []
            _.append(f'{now_iso8601()} {value}')
        else:
            _ = self.logs
            _.append(f'{now_iso8601()} {value}')
        self.logs = _

    def load_status(self):
        """Load prior status values (or not)"""
        for key in self.ATTRLIST:
            if self.job.prev_dry_run:
                # If our last run was a dry run, set each other attribute to None
                setattr(self, key, None)
            else:
                if key in self.status:
                    setattr(self, key, self.status[key])
                else:
                    setattr(self, key, None)

    def get_task(self):
        """Get any task history that may exist for self.job.name and self.task_id

        :rtype: dict
        :returns: The task object from the progress/status update doc
        """
        retval = {}
        try:
            retval = elastic_api.get_task_doc(
                self.job.client, self.job.index, self.job.name, self.task_id)
        except MissingDocument:
            self.logger.debug(
                'Doc tracking job: %s, task: %s does not exist yet', self.job.name, self.task_id)
            return retval
        except Exception as exc:
            self.logger.critical(exc)
            raise FatalException from exc
        self.doc_id = retval['_id']
        return retval['_source']

    def get_history(self):
        """
        Get the history of a taskid, if any. Ensure all values are populated from the doc, or None

        :rtype: None
        :returns: No return value
        """
        self.logger.debug('Pulling any history for task: %s', self.task_id)
        self.status = self.get_task()
        if not self.status:
            self.logger.debug('No history for job: %s, task: %s', self.job.name, self.task_id)
        self.load_status()

    def report_history(self):
        """
        Get the history of any prior attempt to run self.task_id of self.job.name
        Log aspects of the history here.

        :rtype: None
        :returns: No return value
        """
        prefix = f'The prior run of job: {self.job.name}, task: {self.task_id}'
        if self.start_time:
            self.logger.info('%s started at %s', prefix, self.start_time)
        if self.completed:
            if self.end_time:
                self.logger.info('%s completed at %s', prefix, self.end_time)
            else:
                msg = 'is marked completed but did not record an end time'
                self.logger.warning('%s started at %s and %s', prefix, self.start_time, msg)
        if self.errors:
            self.logger.warning('%s encountered errors.', prefix)
            if self.logs:
                # Only report the log if a error is True
                self.logger.warning('%s had log(s): %s', prefix, self.logs)

    def begin(self):
        """Begin the task and record the current status

        :rtype: None
        :returns: No return value
        """
        self.logger.info('Beginning job: %s, task: %s', self.job.name, self.task_id)
        if self.job.dry_run:
            msg = 'DRY-RUN: No changes will be made'
            self.logger.info(msg)
            self.add_log(msg)
        self.start_time = now_iso8601()
        self.completed = False
        self.record()
        if not self.doc_id:
            self.get_task()
            self.load_status()
            self.logger.debug('self.doc_id = %s', self.doc_id)

    def end(self, state, errors=False, logmsg=None):
        """End the task and record the current status
        
        :param state: The completion status of the task
        :param errors: Errors encountered doing the task
        :param logs: Logs recorded doing the task (only if errors)

        :type state: bool
        :type errors: bool
        :type logs: str

        :rtype: None
        :returns: No return value
        """
        self.end_time = now_iso8601()
        self.completed = state
        self.errors = errors
        if logmsg:
            self.add_log(logmsg)
        self.record()
        self.logger.info(
            'Job: %s, task: %s ended. Completed: %s', self.job.name, self.task_id, state)

    def update_status(self):
        """Update instance attribute doc with the current values"""
        # self.logger.debug('Current status: %s', self.status)
        contents = {}
        for val in self.ATTRLIST:
            if getattr(self, val) is not None:
                contents[val] = getattr(self, val)
        self.status = contents
        # self.logger.debug('Updated status: %s', self.status)

    def build_doc(self):
        """Build the dictionary which will be the written to the tracking doc

        :returns: The tracking doc dictionary
        :rtype: dict
        """
        doc = {}
        self.update_status()
        for key in self.ATTRLIST:
            if key in self.status:
                doc[key] = self.status[key]
        if self.index:
            # For the PRE check, there is no value here, so let's not add a null field.
            doc['index'] = self.index
        doc['job'] = self.job.name
        doc['task'] = self.task_id
        doc['join_field'] = {'name': 'task', 'parent': self.job.name}
        doc['dry_run'] = self.job.dry_run
        # self.logger.debug('Updated task doc: %s', doc)
        return doc

    def record(self):
        """Record the current status of the task

        :rtype: None
        :returns: No return value
        """
        doc = self.build_doc()
        try:
            elastic_api.update_doc(self.job.client, self.job.index, self.doc_id, doc)
        except Exception as exc:
            self.logger.critical(exc)
            raise FatalException from exc

    def finished(self):
        """Check if a prior run was recorded for this task and log accordingly
        
        :rtype: bool
        :returns: State of whether a prior run failed to complete
        """
        if self.completed:
            if self.job.dry_run:
                self.logger.info(
                    'DRY-RUN: Ignoring previous run of job: %s, task %s',
                    self.job.name, self.task_id)
            else:
                self.logger.info(
                    'Job: %s, task: %s was completed previously.', self.job.name, self.task_id)
                return True
        if self.start_time:
            self.report_history()
            self.logger.warning('Restarting or resuming task: %s', self.task_id)
        return False
