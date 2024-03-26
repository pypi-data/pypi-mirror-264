"""Index Redaction"""
# pylint: disable=missing-function-docstring
import logging
from datetime import datetime
from app import elastic_api
from app.exceptions import FatalException, FailedReindex, MissingIndex, ResultNotExpected
from app.helpers import get_field_matches, get_fname, get_index_version, strip_index_name
from app.tracking import Task

MOD = __name__

class RedactIndex:
    """Redact index per settings"""
    def __init__(self, index, job, counter):
        self.logger = logging.getLogger(f'{MOD}.{self.__class__.__name__}')
        self.task = Task(job, index=index, id_suffix='REDACT-INDEX')
        self.index = index
        self.counter = counter
        self.verify_index()

    @property
    def hits(self):
        return self._hits

    @property
    def phase(self):
        return self._phase

    @property
    def result(self):
        return self._result

    @property
    def success(self):
        return self._success

    @hits.setter
    def hits(self, value):
        self._hits = value

    @phase.setter
    def phase(self, value):
        self._phase = value

    @result.setter
    def result(self, value):
        self._result = value

    @success.setter
    def success(self, value):
        self._success = value

    def verify_index(self):
        """Verify the index exists"""
        # If the index name changed because of an ILM phase shift from hot to cold
        # or cold to frozen, then we should verify the name change here. We should raise
        # an exception if the name of the index changed or it disappeared.
        if not elastic_api.verify_index(self.task.job.client, self.index):
            msg = f'Halting execution: Index {self.index} changed or is missing.'
            self.logger.critical(msg)
            self.success = False
            raise MissingIndex(msg)

    def run_query(self):
        """Run the query"""
        self.result = elastic_api.do_search(
            self.task.job.client, self.index, self.task.job.config['query'], size=10000)
        self.hits = self.result['hits']['total']['value']
        self.logger.debug('Checking document fields on index: %s...', self.index)
        if self.hits == 0:
            self.counter += 1
            msg = f'Documents matching redaction query not found on index: {self.index}'
            self.logger.debug(msg)
            msg = f'Index {self.counter} of {self.task.job.total} processed...'
            self.logger.info(msg)
            # Record success for this task but send msg to the log field
            # An index could be in the pattern but have no matches.
            self.task.end(True, logmsg=msg)
        self.task.add_log(f"Hits: {self.hits}")

    def verify_fields(self):
        """Verify the fields in the query results match what we expect"""
        if not get_field_matches(self.task.job.config, self.result) > 0:
            msg = f'Fields required for redaction not found on index: {self.index}'
            self.logger.warning(msg)
            self.task.end(True, logmsg=msg)
            self.logger.warning(
                'Not a fatal error. Index in pattern does not have the specified fields')

    def get_phase(self):
        """Get the ILM phase (if any) for the index"""
        nope = 'Not assigned an ILM Phase'
        try:
            self.phase = elastic_api.get_phase(self.task.job.client, self.index) or nope
        except MissingIndex as exc:
            msg = f'Missing index error: {exc}'
            self.logger.critical(msg)
            self.task.end(False, errors=True, logmsg=msg)
            raise FatalException from exc
        self.logger.debug('Index in phase: %s', self.phase.upper())
        self.task.add_log(f'ILM Phase: {self.phase}')

    def normal_redact(self):
        """Redact data from a normal (not searchable-snapshot) index"""
        msg = 'Initiating redaction of data from writeable index...'
        self.logger.info(msg)
        self.task.add_log(msg)
        # As the redact_from_index function doesn't track dry-run, we have to do it
        if not self.task.job.dry_run:
            msg = f'Redacting data from {self.index}'
            self.logger.info(msg)
            self.task.add_log(msg)
            try:
                elastic_api.redact_from_index(
                    self.task.job.client, self.index, self.task.job.config)
            except (MissingIndex, ResultNotExpected) as exc:
                self.logger.critical(exc)
                self.task.end(False, errors=True, logmsg=exc)
        else:
            msg = f'DRY-RUN: Will not redact data from {self.index}'
            self.logger.info(msg)
            self.task.add_log(msg)

    def snapshot_redact(self):
        """Redact data from searchable snapshot-backed index"""
        msg = 'Initiating redaction of data from mounted searchable snapshot...'
        self.logger.info(msg)
        self.task.add_log(msg)
        try:
            snp = RedactSnapshot(self.index, self.task.job, self.phase)
        except Exception as exc:
            self.logger.critical('Unable to build RedactSnapshot object. Exception: %s', exc)
            raise
        try:
            snp.run()
        except Exception as exc:
            self.logger.critical('Unable to run RedactSnapshot object. Exception: %s', exc)
            raise

    def run(self):
        """Do the actual run"""
        if self.task.finished():
            self.success = True
            return
        # Log task start time
        self.task.begin()
        self.run_query()
        if self.task.completed:
            self.success = True
            return
        self.verify_fields()
        if self.task.completed:
            self.success = True
            return
        self.get_phase()
        if self.phase in ('cold', 'frozen'):
            self.snapshot_redact()
        else:
            self.normal_redact()
        # If we have reached this point, we've succeeded.
        self.counter += 1
        msg = f'Index {self.counter} of {self.task.job.total} processed...'
        self.logger.info(msg)
        self.task.add_log(msg)
        self.task.end(True, logmsg='DONE')
        self.success = True

class RedactSnapshot:
    """Redact PII from indices mounted as searchable snapshots"""
    def __init__(self, index, job, phase):
        self.logger = logging.getLogger(f'{MOD}.{self.__class__.__name__}')
        self.index = index
        self.phase = phase
        self.task = Task(job, index=index, id_suffix='REDACT-SNAPSHOT')
        self.var = self.ConfigAttrs(job.client, index, phase)

    # pylint: disable=missing-class-docstring, missing-function-docstring
    class ConfigAttrs:
        def __init__(self, client, index, phase):
            self.logger = logging.getLogger(f'{MOD}.{self.__class__.__name__}')
            self.client = client
            self.index = index
            self.phase = phase
            self.prefix = phase
            self.storage = phase
            self.og_name = strip_index_name(index)
            now = datetime.now()
            self.redaction_target = f'redacted-{now.strftime("%Y%m%d%H%M%S")}-{self.og_name}'
            self.new_snap_name = f'{self.redaction_target}-snap'
            # Check if the old index has been redacted before and has a version number
            self.ver = get_index_version(index)
            # The mount name contains a version at the end in case we need to redact the index again
            # The version allows us to use a similar naming scheme without redundancy
            self.mount_name = f'{self.prefix}redacted-{self.og_name}---v{self.ver + 1:03}'
            self.logger.debug('mount_name = %s', self.mount_name)

        @property
        def aliases(self):
            return self._aliases
        @aliases.setter
        def aliases(self, value):
            self._aliases = value

        @property
        def repository(self):
            return self._repository
        @repository.setter
        def repository(self, value):
            self._repository = value

        @property
        def ss_snap(self):
            return self._ss_snap
        @ss_snap.setter
        def ss_snap(self, value):
            self._ss_snap = value

        @property
        def ss_idx(self):
            return self._ss_idx
        @ss_idx.setter
        def ss_idx(self, value):
            self._ss_idx = value

        @property
        def restore_settings(self):
            return self._restore_settings
        @restore_settings.setter
        def restore_settings(self, value):
            self._restore_settings = value

        @property
        def prefix(self):
            return self._prefix
        @prefix.setter
        def prefix(self, value):
            # ignore whatever is passed
            value = self.phase
            prefix = ''
            if value == 'cold':
                prefix = 'restored-'
            elif value == 'frozen':
                prefix = 'partial-restored-'
            self._prefix = prefix

        @property
        def storage(self):
            return self._storage
        @storage.setter
        def storage(self, value):
            # ignore whatever is passed
            value = self.phase
            storage = ''
            if value == 'cold':
                storage = 'full_copy'
            elif value == 'frozen':
                storage = 'shared_cache'
            self._storage = storage

        def get_index_deets(self):
            """Return searchable snapshot values from deeply nested index settings"""
            response = elastic_api.get_index(self.client, self.index)
            self.logger.debug('Found indices: %s', list(response.keys()))
            self.aliases = response[self.index]['aliases']
            snap_data = response[self.index]['settings']['index']['store']['snapshot']
            self.repository = snap_data['repository_name']
            self.ss_snap = snap_data['snapshot_name']
            self.ss_idx = snap_data['index_name']
            self.logger.debug('ss_idx = %s', self.ss_idx)

    @property
    def success(self):
        return self._success

    @success.setter
    def success(self, value):
        self._success = value

    def run(self):
        """Do the actual run"""
        if self.task.finished():
            self.success = True
            return
        # Log task start time
        self.task.begin()
        self.logger.info("Getting index info: %s", self.index)
        self.var.restore_settings = self.task.job.config['restore_settings']
        self.var.get_index_deets()

        steps = RedactionSteps(self.task, self.var)
        steps.run()

        if not self.task.job.dry_run:
            msg = f'Index {self.index} has completed all steps.'
            self.logger.info(msg)
            self.task.add_log(msg)
            self.task.end(True, errors=False)
            self.success = True
            return
        # Implied else (meaning it is a dry run)
        _ = f'DRY-RUN || {self.task.logs}'
        self.success = False
        self.task.logs = _

        # Write this tidbit
        fdesc = open("snapshotstodelete.txt", "a", encoding='utf8')
        fdesc.write(self.var.ss_snap+"\n")
        fdesc.close()

class RedactionSteps:
    """All of the redaction steps for the final flow"""
    def __init__(self, task, var):
        self.logger = logging.getLogger(f'{MOD}.{self.__class__.__name__}')
        self.task = task
        self.var = var

    def failed_step(self, stepname, exc):
        """Function to avoid repetition of code if a step fails"""
        self.logger.critical(exc)
        self.task.end(False, errors=True, logmsg=f'Failed {stepname}: {exc}')
        raise FatalException from exc

    def log_step(self, stepname, kind):
        """Function to avoid repetition of code"""
        msgmap = {
            'start': 'starting...',
            'end': 'completed.',
            'dry-run': 'DRY-RUN. No change will take place'
        }
        msg = f'{stepname} {msgmap[kind]}'
        self.logger.info(msg)
        self.task.add_log(msg)

    def check_dotted_fields(self, result, field):
        """Iterate through dotted fields to ensure success

        :param result: The search result object
        :param field: The field with dotted notation

        :type result: dict
        :type field: str

        :returns: Success (``True``) or Failure (``False``)
        :rtype: bool
        """
        success = False
        self.logger.debug('Dotted field detected: (%s) ...', field)
        fielder = result['hits']['hits'][0]['_source']
        iterations = len(field.split('.'))
        counter = 1
        for key in field.split('.'):
            # This should recursively look for each subkey
            if key in fielder:
                fielder = fielder[key]
            else:
                break
            if counter == iterations:
                if fielder == self.task.job.config['message']:
                    success = True
            counter += 1
        return success

    def check_fields(self, result):
        """Check document fields in result to ensure success

        :param result: The search result object

        :type result: dict

        :returns: Success (``True``) or Failure (``False``)
        :rtype: bool
        """
        complete = True
        hit = result['hits']['hits'][0]['_source']
        for field in self.task.job.config['fields']:
            success = False
            if len(field.split('.')) > 1:
                success = self.check_dotted_fields(result, field)

            elif field in hit:
                if hit[field] == self.task.job.config['message']:
                    success = True

            else:
                self.logger.warning("Field %s not present in document", field)
                # Don't need to report the expected fail 2x, so we break the loop here
                break

            if success:
                self.logger.info("Field %s is redacted correctly", field)
            else:
                # A single failure is enough to make it a complete failure.
                complete = False
                self.logger.error("Field %s is not redacted correctly", field)
        return complete

    def check_index(self, index_name):
        """Check the index"""
        self.logger.info('Making a quick check on redacted index docs...')
        result = elastic_api.do_search(
            self.task.job.client, index_name, self.task.job.config['query'])
        if result['hits']['total']['value'] == 0:
            self.logger.warning(
                'Query returned no results, assuming it only returns docs '
                'to be redacted and not already redacted...')
            return
        success = self.check_fields(result)
        if not success:
            msg = 'One or more fields were not redacted. Check the logs'
            self.logger.error(msg)
            raise ResultNotExpected(msg)

    def fmwrapper(self):
        """Do some task logging around the forcemerge api call

        :rtype: None
        :returns: No return value
        """
        logger = logging.getLogger(__name__)
        client = self.task.job.client
        index = self.var.redaction_target
        msg = f'Before forcemerge, {elastic_api.report_segment_count(client, index)}'
        logger.info(msg)
        self.task.add_log(msg)
        if 'forcemerge' in self.task.job.config:
            kwargs = self.task.job.config['forcemerge']
        kwargs['index'] = index
        if 'only_expunge_deletes' in kwargs and kwargs['only_expunge_deletes']:
            msg = 'Forcemerge will only expunge deleted docs!'
            logger.info(msg)
            self.task.add_log(msg)
        else:
            mns = 1 # default value
            if 'max_num_segments' in kwargs and isinstance(kwargs['max_num_segments'], int):
                mns = kwargs['max_num_segments']
            msg = f'Proceeding to forcemerge to {mns} segments per shard'
            logger.info(msg)
            self.task.add_log(msg)
        # Do the actual forcemerging
        elastic_api.forcemerge_index(client, **kwargs)
        msg = f'After forcemerge, {elastic_api.report_segment_count(client, index)}'
        logger.info(msg)
        self.task.add_log(msg)
        logger.info('Forcemerge completed.')

    def step1_pre_delete(self):
        """Pre-delete the redacted index to ensure no collisions. Ignore if not present"""
        self.log_step(get_fname(), 'start')
        if not self.task.job.dry_run:
            try:
                elastic_api.delete_index(self.task.job.client, self.var.redaction_target)
            except MissingIndex:
                self.logger.debug('Pre-delete did not find index "%s"', self.var.redaction_target)
                # No problem. This is expected.
        else:
            self.log_step(get_fname(), 'dry-run')
        self.log_step(get_fname(), 'end')

    def step(self, name, func, *args, **kwargs):
        """The reusable step"""
        self.log_step(name, 'start')
        if not self.task.job.dry_run:
            try:
                func(*args, **kwargs)
            except (FailedReindex, MissingIndex, ResultNotExpected) as exc:
                self.failed_step(name, exc)
        else:
            self.log_step(name, 'dry-run')
        self.log_step(name, 'end')

    def step2_restore_index(self):
        """Restore index from snapshot"""
        self.step(get_fname(), elastic_api.restore_index,
                    self.task.job.client, self.var.repository, self.var.ss_snap, self.var.ss_idx,
                    self.var.redaction_target, index_settings=self.var.restore_settings)

    def step3_redact_from_index(self):
        """Run update by query on new restored index"""
        self.step(get_fname(), elastic_api.redact_from_index,
                    self.task.job.client, self.var.redaction_target, self.task.job.config)

    def step4_forcemerge_index(self):
        """Force merge redacted index"""
        self.step(get_fname(), self.fmwrapper)

    def step5_clear_cache(self):
        """Clear cache of redacted index"""
        self.step(get_fname(), elastic_api.clear_cache, self.task.job.client, self.var.redaction_target)

    def step6_confirm_redaction(self):
        """Check update by query did its job"""
        self.step(get_fname(), self.check_index, self.var.redaction_target)

    def step7_snapshot_index(self):
        """Create a new snapshot for mounting our redacted index"""
        self.step(get_fname(), elastic_api.take_snapshot,
                  self.task.job.client, self.var.repository, self.var.new_snap_name,
                  self.var.redaction_target)

    def step8_mount_snapshot(self):
        """Mount the index as a searchable snapshot to make the redacted index available"""
        self.step(get_fname(), elastic_api.mount_index,
                  self.task.job.client, self.var.repository, self.var.new_snap_name,
                  self.var.redaction_target, self.var.mount_name, self.var.storage)

    def step9_delete_redaction_target(self):
        """Now that it's mounted (with a new name), we should delete the redaction_target index"""
        self.step(get_fname(), elastic_api.delete_index, self.task.job.client, self.var.redaction_target)

    def _step10_builder(self):
        """This is makes the real step 10 a one liner"""
        alias_names = self.var.aliases.keys()
        if not alias_names:
            msg = f'{get_fname()} No aliases associated with index {self.var.index}'
            self.task.add_log(msg)
            self.logger.warning(msg)
        else:
            msg = f'{get_fname()} Transferring aliases to new index {self.var.mount_name}'
            self.task.add_log(msg)
            self.logger.debug(msg)
            self.task.job.client.indices.update_aliases(
                actions=elastic_api.get_alias_actions(
                    self.var.index, self.var.mount_name, self.var.aliases))
            verify = self.task.job.client.indices.get(
                index=self.var.mount_name)[self.var.mount_name]['aliases'].keys()
            if alias_names != verify:
                msg = f'Alias names do not match! {alias_names} does not match: {verify}'
                msg2 = f'Failed {get_fname()}: {msg}'
                self.logger.critical(msg2)
                self.task.add_log(msg2)
                raise ResultNotExpected(msg)

    def step10_fix_aliases(self):
        """Using the aliases collected from self.index, update mount_name and verify"""
        self.step(get_fname(), self._step10_builder)

    def step11_close_old_index(self):
        """Close old mounted snapshot"""
        self.step(get_fname(), elastic_api.close_index, self.task.job.client, self.var.index)

    def _step12_builder(self):
        """This makes step 12 work with self.step"""
        if self.task.job.config['delete']:
            msg = f'Deleting original mounted index: {self.var.index}'
            self.task.add_log(msg)
            self.logger.info(msg)
            try:
                elastic_api.delete_index(self.task.job.client, self.var.index)
            except MissingIndex as exc:
                self.failed_step(get_fname(), exc)
        else:
            msg = f'delete set to False — not deleting original mounted index: {self.var.index}'
            self.task.add_log(msg)
            self.logger.warning(msg)

    def step12_delete_old_index(self):
        """Delete old mounted snapshot, if configured to do so"""
        self.step(get_fname(), self._step12_builder)

    def step13_assign_aliases(self):
        """Put the starting index name on new mounted index as alias"""
        self.step(get_fname(), elastic_api.assign_alias,
                  self.task.job.client, self.var.mount_name, self.var.index)

    def step14_record_it(self):
        """Record the now-deletable snapshot in the job's tracking index."""
        self.log_step(get_fname(), 'start')
        self.task.job.cleanup.append(self.var.ss_snap)
        self.log_step(get_fname(), 'end')

    def run(self):
        """Run the steps in sequence"""
        self.step1_pre_delete()
        self.step2_restore_index()
        self.step3_redact_from_index()
        self.step4_forcemerge_index()
        self.step5_clear_cache()
        self.step6_confirm_redaction()
        self.step7_snapshot_index()
        self.step8_mount_snapshot()
        self.step9_delete_redaction_target()
        self.step10_fix_aliases()
        self.step11_close_old_index()
        self.step12_delete_old_index()
        self.step13_assign_aliases()
        self.step14_record_it()
