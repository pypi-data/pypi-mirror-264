"""Functions making Elasticsearch API calls"""
import logging
from elasticsearch8.exceptions import ApiError, NotFoundError, TransportError, BadRequestError
from app.exceptions import (
    ConfigurationException, FailedReindex, MissingArgument, MissingDocument, MissingIndex,
    ResultNotExpected, TimeoutException)
from app.helpers import build_script
from app.tracking import Job, Task
from app.waiters import wait_for_it

def assign_alias(client, index_name, alias_name):
    """Assign index to alias(es)"""
    logger = logging.getLogger(__name__)
    try:
        response = client.indices.put_alias(index=index_name, name=alias_name)
        logger.info("Index '%s' was successfully added to alias '%s'", index_name, alias_name)
        logger.debug(response)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        msg = f'Attempt to assign index "{index_name}" to alias "{alias_name}" failed'
        logger.critical(msg)
        raise ResultNotExpected(msg) from err

def clear_cache(client, index_name):
    """Clear the cache for named index

    :param client: A client connection object
    :param index_name: The index name

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_name: str

    :returns: No return value
    :rtype: None
    """
    logger = logging.getLogger(__name__)
    response = {}
    logger.info('Clearing cache data for %s...', index_name)
    try:
        response = client.indices.clear_cache(index=index_name)
        logger.debug(response)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error('clear_cache API call resulted in an error: %s', err)

def close_index(client, name):
    """Close an index

    :param name: The index name to close

    :type name: str

    :rtype: None

    :returns: No return value
    """
    logger = logging.getLogger(__name__)
    try:
        response = client.indices.close(index=name)
        logger.debug(response)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error("Index: '%s' not found. Error: %s", name, err)
        raise MissingIndex(f'Index "{name}" not found') from err

def create_index(client, name, mappings=None, settings=None):
    """Create an Elasticsearch index with associated mappings and settings

    :param name: The index name
    :param mappings: The index mappings
    :param settings: The index settings

    :type name: str
    :type mappings: dict
    :type settings: dict

    :rtype: None

    :returns: No return value
    """
    logger = logging.getLogger(__name__)
    if index_exists(client, name):
        logger.info('Index %s already exists', name)
        return
    try:
        response = client.indices.create(index=name, settings=settings, mappings=mappings)
        logger.debug(response)
    except BadRequestError as err:
        logger.error("Index: '%s' already exists. Error: %s", name, err)
        raise ResultNotExpected(f'Index "{name}" already exists') from err
    except (ApiError, TransportError) as err:
        logger.error("Unknown error trying to create index: '%s'. Error: %s", name, err)
        raise ResultNotExpected(f'Unknown error trying to create index: {name}') from err

def delete_index(client, name):
    """Delete an index

    :param client: A client connection object
    :param name: The index name to delete

    :type name: str

    :rtype: None

    :returns: No return value
    """
    logger = logging.getLogger(__name__)
    try:
        response = client.indices.delete(index=name)
        logger.debug(response)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        # logger.error("Index: '%s' not found. Error: %s", name, err)
        raise MissingIndex(f'Index "{name}" not found') from err

def do_search(client, index_pattern, query, size=10):
    """Return search result of ``query`` against ``index_pattern``

    :param client: A client connection object
    :param index_pattern: A single index name, a csv list of indices, or other pattern
    :param query: An Elasticsearch DSL search query
    :param size: Maximum number of results to return

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_pattern: str
    :type query: dict
    :type size: int

    :returns: A search result object
    :rtype: dict
    """
    logger = logging.getLogger(__name__)
    try:
        response = client.search(index=index_pattern, query=query, size=size)
        logger.debug(response)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        msg = f'Attempt to collect search results yielded an exception: {err}'
        logger.critical(msg)
        raise ResultNotExpected(msg) from err
    return response

def forcemerge_index(client, index=None, max_num_segments=1, only_expunge_deletes=False):
    """
    Force Merge an index

    :param client: A client connection object
    :param index: A single index name
    :param max_num_segments: The maximum number of segments per shard after force merging
    :param only_expunge_deletes: Only expunge deleted docs during force merging.
        If True, ignores max_num_segments.

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str
    :type max_num_segments: int
    :type only_expunge_deletes: bool

    :rtype: None
    :returns: No return value
    """
    logger = logging.getLogger(__name__)
    kwargs = {'index': index, 'wait_for_completion': False}
    if only_expunge_deletes:
        kwargs['only_expunge_deletes'] = True
    else:
        kwargs['max_num_segments'] = max_num_segments
    try:
        response = client.indices.forcemerge(**kwargs)
        logger.debug(response)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error("Index: '%s' not found. Error: %s", index, err)
        raise MissingIndex(f'Index "{index}" not found') from err
    logger.info('Waiting for forcemerge to complete...')
    try:
        wait_for_it(client, 'forcemerge', response['task'])
    except (
        ConfigurationException, FailedReindex, MissingArgument, ResultNotExpected,
        TimeoutException) as exc:
        logger.error('Exception: %s', exc)
        raise ResultNotExpected('Failed to forcemerge') from exc
    logger.info('Forcemerge completed.')

def get_ilm(client, index):
    """Get the ILM lifecycle settings for an index

    :param client: A client connection object
    :param index: The index to check

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str

    :returns: The ILM settings object for the named index
    :rtype: dict
    """
    logger = logging.getLogger(__name__)
    try:
        response = client.ilm.explain_lifecycle(index=index)
        logger.debug(response)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error("Index: '%s' not found. Error: %s", index, err)
        raise MissingIndex(f'Index "{index}" not found') from err
    return response

def get_hits(client, index, query):
    """Return the number of hits matching the query

    :param client: A client connection object
    :param index: The index or pattern to search
    :param query: The query to execute

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str
    :type query: dict

    :rtype: int

    :returns: The number of hits matching the query
    """
    result = do_search(client, index, query)
    return result['hits']['total']['value']

def get_index(client, index):
    """Get the info about an index

    :param client: A client connection object
    :param index: The index, csv indices, or index pattern to get

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str

    :returns: The index information object for the named index
    :rtype: dict
    """
    logger = logging.getLogger(__name__)
    try:
        response = client.indices.get(index=index)
        logger.debug('Found indices: %s', list(response.keys()))
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error("Index: '%s' not found. Error: %s", index, err)
        raise MissingIndex(f'Index "{index}" not found') from err
    return response

def get_phase(client, index):
    """Get the index's ILM phase

    :param client: A client connection object
    :param index: The index name

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str

    :returns: The ILM phase of ``index``
    :rtype: str
    """
    phase = None
    try:
        ilm = get_ilm(client, index)
    except MissingIndex as exc:
        raise MissingIndex from exc
    try:
        phase = ilm['indices'][index]['phase']
    except KeyError: # Perhaps in cold/frozen but not ILM affiliated
        settings = get_settings(client, index)[index]['settings']['index']
        if "store" in settings:
            # Checking if it's a mounted searchable snapshot
            if settings["store"]["type"] == "snapshot":
                phase = get_phase_from_tier_pref(settings)
        else:
            phase = None
    return phase

def get_phase_from_tier_pref(idx_settings):
    """Check the index's ``_tier_preference`` as an indicator which phase the index is in

    :param idx_settings: The results from a get_settings(index=idx)[idx]['settings']['index'] call

    :type idx_settings: dict

    :returns: The ILM phase based on the index settings, or None
    :rtype: str
    """
    try:
        tiers = idx_settings['routing']['allocation']['include']['_tier_preference']
    except KeyError:
        tiers = ''
    if tiers == 'data_frozen':
        return 'frozen'
    if 'data_cold' in tiers.split(','):
        return 'cold'
    return None

def report_segment_count(client, index: str):
    """
    Report the count of segments from index

    :param client: A client connection object
    :param index: The index to check

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str

    :returns: Formatted message describing shard count and segment count for index
    :rtype: str
    """
    logger = logging.getLogger(__name__)
    shardcount = 0
    segmentcount = 0
    output = client.cat.shards(index=index, format='json', h=['index', 'shard', 'prirep', 'sc'])
    for shard in output:
        if shard['prirep'] == 'r':
            # Skip replica shards
            continue
        if index != shard['index']:
            logger.warning(
                'Index name %s does not match what was returned by the _cat API: %s',
                index, shard['index']
            )
        shardcount += 1
        segmentcount += int(shard['sc'])
        logger.debug('Index %s, shard %s has %s segments', index, shard["shard"], shard["sc"])

    return (
        f'index {index} has {shardcount} shards and a total of {segmentcount} segments, '
        f'averaging {float(segmentcount/shardcount)} segments per shard'
    )

def get_settings(client, index):
    """Get the settings for an index

    :param client: A client connection object
    :param index: The index to check

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str

    :returns: The settings object for the named index
    :rtype: dict
    """
    logger = logging.getLogger(__name__)
    logger.debug('Getting settings for index: %s', index)
    try:
        response = client.indices.get_settings(index=index)
        logger.debug(response)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error("Index: '%s' not found. Error: %s", index, err)
        raise MissingIndex(f'Index "{index}" not found') from err
    logger.debug('Index settings collected.')
    return response

def get_task_doc(client, index_name, job_id, task_id):
    """Get a task tracking doc

    :param client: A client connection object
    :param index_name: The index name
    :param job_id: The job_id string for the present redaction run
    :param task_id: The task_id string of the task we are searching for

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_name: str
    :type job_id: str
    :type task_id: str

    :rtype: dict
    :returns: The task tracking document from the progress/status tracking index
    """
    logger = logging.getLogger(__name__)
    if not index_exists(client, index_name):
        msg = f'Tracking index {index_name} is missing'
        logger.critical(msg)
        raise MissingIndex(msg)
    query = {
        "bool": {
            "must": {
                "parent_id": {
                    "type": "task",
                    "id": job_id
                }
            },
            "filter": [{"term":  { "task": task_id }}]
        }
    }
    result = do_search(client, index_pattern=index_name, query=query)
    if result['hits']['total']['value'] != 1:
        msg = 'Tracking document for job: {job_id}, task: {task_id} does not exist'
        raise MissingDocument(msg)
    return result['hits']['hits'][0]

def get_tracking_doc(client, index_name, job_id):
    """Get the progress/status tracking doc

    :param client: A client connection object
    :param index_name: The index name
    :param job_id: The job_id string for the present redaction run

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_name: str
    :type job_id: str

    :rtype: dict
    :returns: The tracking document from the progress/status tracking index
    """
    logger = logging.getLogger(__name__)
    if not index_exists(client, index_name):
        msg = f'Tracking index {index_name} is missing'
        logger.critical(msg)
        raise MissingIndex(msg)
    try:
        doc = client.get(index=index_name, id=job_id)
        # logger.debug('TRACKING DOC = %s', doc)
    except NotFoundError as exc:
        # logger.debug('Tracking document for job_id %s does not exist', job_id)
        raise MissingDocument from exc
    return doc['_source']

def index_exists(client, index_name):
    """Test whether index ``index_name`` exists 

    :param client: A client connection object
    :param index_name: The index name

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_name: str

    :rtype: bool

    :returns: ``True`` if ``index_name`` exists, otherwise ``False``
    """
    return client.indices.exists(index=index_name)

def index_health_check(client, index_name, status='green'):
    """Test whether index ``index_name`` has the expected status

    :param client: A client connection object
    :param index_name: The index name
    :param status: The expected status (red, yellow, green)

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_name: str
    :param status: str

    :rtype: bool

    :returns: ``True`` if ``index_name`` has the expected status, otherwise ``False``
    """
    if not index_exists(client, index_name):
        raise ResultNotExpected(f'Index {index_name} missing')
    result = client.cluster.health(index=index_name, level='indices')
    return result['indices'][index_name]['status'] == status

def job_exists(client, index_name, job_id):
    """Test whether a document exists for the present job_id

    :param client: A client connection object
    :param index_name: The index name
    :param job_id: The job_id string for the present redaction run

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_name: str
    :type job_id: str

    :rtype: bool

    :returns: ``True`` if a document exists with the present job_id, otherwise ``False``
    """
    return client.exists(index=index_name, id=job_id)

def mount_index(client, repo, snap, index, mount_name, storage_val):
    """Mount index as a searchable snapshot

    :param client: A client connection object
    :param repo: The repository name
    :param snap: The snapshot name
    :param index: The index name as it appears in the snapshot metadata
    :param mount_name: The name the index from the searchable snapshot will be mounted as
    :param storage_val: For cold tier, this is ``full_copy``. For frozen tier, this is
        ``shared_cache``

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type repo: str
    :type snap: str
    :type index: str
    :type mount_name: str
    :type storage_val: str

    :returns: No return value
    :rtype: None
    """
    logger = logging.getLogger(__name__)
    response = {}
    msg = (
        f'Mounting {index} renamed as {mount_name} '
        f'from repository: {repo}, snapshot {snap} and storage={storage_val}'
    )
    logger.info(msg)
    try:
        logger.info("Mounting new snapshot...")
        response = client.searchable_snapshots.mount(
            repository=repo, snapshot=snap, index=index,
            renamed_index=mount_name, storage=storage_val
        )
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error("Attempt to mount index 'mounted_%s' failed: %s", index, err)
        logger.debug(response)
        raise ResultNotExpected('Error when mount index attempted') from err
    logger.info('Ensuring searchable snapshot mount is in "green" health state...')
    try:
        wait_for_it(client, 'mount', index=index)
    except (
        ConfigurationException, FailedReindex, MissingArgument, ResultNotExpected,
        TimeoutException) as exc:
        logger.error('Exception: %s', exc)
        raise ResultNotExpected('Failed to mount index from snapshot') from exc
    logger.info("Index '%s' mounted from snapshot succesfully", mount_name)

def restore_index(
        client, repo_name, snap_name, index_name, replacement, re_pattern='(.+)',
        index_settings=None):
    """Restore an index

    :param client: A client connection object
    :param repo_name: The repository name
    :param snap_name: The snapshot name
    :param index_name: The index name as it appears in the snapshot metadata
    :param replacement: The name or substitution string to use as the restored index name
    :param re_pattern: The optional rename pattern for use with ``replacement``
    :param index_settings: Any settings to apply to the restored index, such as _tier_preference

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type repo_name: str
    :type snap_name: str
    :type index_name: str
    :type replacement: str
    :type re_pattern: str
    :type index_settings: dict

    :returns: No return value
    :rtype: None
    """
    logger = logging.getLogger(__name__)
    msg = (
        f"repository={repo_name}, snapshot={snap_name}, indices={index_name},"
        f"include_aliases=False,"
        f"ignore_index_settings=["
        f"    'index.lifecycle.name', 'index.lifecycle.rollover_alias',"
        f"    'index.routing.allocation.include._tier_preference'],"
        f"index_settings={index_settings},"
        f"rename_pattern={re_pattern},"
        f"rename_replacement={replacement},"
        f"wait_for_completion=False"
    )
    logger.debug('RESTORE settings: %s', msg)
    try:
        response = client.snapshot.restore(
            repository=repo_name, snapshot=snap_name, indices=index_name,
            include_aliases=False,
            ignore_index_settings=[
                'index.lifecycle.name', 'index.lifecycle.rollover_alias',
                'index.routing.allocation.include._tier_preference'],
            index_settings=index_settings,
            rename_pattern=re_pattern,
            rename_replacement=replacement,
            wait_for_completion=False
        )
        logger.debug('Response = %s', response)
        logger.info('Checking if restoration completed...')
        try:
            wait_for_it(client, 'restore', repository=repo_name, index_list=[replacement])
        except (
            ConfigurationException, FailedReindex, MissingArgument, ResultNotExpected,
            TimeoutException) as exc:
            logger.error('Exception: %s', exc)
            raise ResultNotExpected('Failed to restore index from snapshot') from exc
        msg = f'Restoration of index {index_name} as {replacement} complete'
        logger.info(msg)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        msg = f'Restoration of index {index_name} as {replacement} yielded an error: {err}'
        logger.error(msg)
        raise ResultNotExpected(msg) from err

def redact_from_index(client, index_name, config):
    """Redact data from an index using a painless script.

    Collect the task_id and wait for the reinding job to complete before returning

    :param client: A client connection object
    :param index_name: The index to act on
    :param config: The config block being iterated. Contains ``query``, ``message``, and ``fields``

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_name: str
    :type config: dict

    :rtype: None
    :returns: No return value
    """
    logger = logging.getLogger(__name__)
    logger.info('Before update by query, %s', report_segment_count(client, index_name))
    logger.debug('Updating and redacting data...')
    script = build_script(config['message'], config['fields'])
    response = {}
    try:
        response = client.update_by_query(
            index=index_name,
            script=script,
            query=config['query'],
            wait_for_completion=False
        )
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.critical('update_by_query yielded an error: %s', err)
        raise FailedReindex('update_by_query API call failed') from err
    logger.debug('Checking update by query status...')
    try:
        wait_for_it(client, 'update_by_query', response['task'])
    except (
        ConfigurationException, FailedReindex, MissingArgument, ResultNotExpected,
        TimeoutException) as exc:
        logger.error('Exception: %s', exc)
        raise ResultNotExpected('Failed to complete update by query') from exc
    logger.info('After update by query, %s', report_segment_count(client, index_name))
    logger.debug('Update by query completed.')

def get_alias_actions(oldidx, newidx, aliases):
    """
    :param oldidx: The old index name
    :param newidx: The new index name
    :param aliases: The aliases

    :type oldidx: str
    :type newidx: str
    :type aliases: dict

    :returns: A list of actions suitable for
        :py:meth:`~.elasticsearch.client.IndicesClient.update_aliases` ``actions`` kwarg.
    :rtype: list
    """
    actions = []
    for alias in aliases.keys():
        actions.append({'remove': {'index': oldidx, 'alias': alias}})
        actions.append({'add': {'index': newidx, 'alias': alias}})
    return actions

def take_snapshot(client, repo_name, snap_name, index_name):
    """Take snapshot of index"""
    logger = logging.getLogger(__name__)
    logger.info('Creating new snapshot...')
    response = {}
    try:
        response = client.snapshot.create(
            repository=repo_name, snapshot=snap_name, indices=index_name,
            wait_for_completion=False
        )
        logger.debug('Snapshot response: %s', response)
    except (ApiError, NotFoundError, TransportError, BadRequestError, KeyError) as err:
        msg = f'Creation of snapshot "{snap_name}" resulted in an error: {err}'
        logger.critical(msg)
        raise ResultNotExpected(msg) from err
    logger.info('Checking on status of snapshot...')
    try:
        wait_for_it(client, 'snapshot', repository=repo_name, snapshot=snap_name)
    except (
        ConfigurationException, FailedReindex, MissingArgument, ResultNotExpected,
        TimeoutException) as exc:
        logger.error('Exception: %s', exc)
        raise ResultNotExpected('Failed to complete index snapshot') from exc
    msg = f'{index_name}: Snapshot to repository {repo_name} in snapshot {snap_name} succeeded.'
    logger.info(msg)

def update_doc(client, index, doc_id, doc, routing=0):
    """Upsert a document in ``index`` at ``doc_id`` with the values of ``doc``

    :param client: A client connection object
    :param index: The index to write to
    :param doc_id: The document doc_id to update
    :param doc: The contents of the document
    :param routing: Because our tracking doc is using parent/child relationships, we need to route

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str
    :type doc_id: str
    :type doc: dict
    :type routing: int

    :rtype: None
    :returns: No return value
    """
    logger = logging.getLogger(__name__)
    # logger.debug('Updating index %s /_doc/ %s with %s', index, doc_id, doc)
    try:
        if doc_id:
            _ = client.update(
                index=index, id=doc_id, doc=doc, doc_as_upsert=True, routing=routing, refresh=True)
        else:
            logger.debug('No value for document id. Creating new document.')
            _ = client.index(index=index, document=doc, routing=routing, refresh=True)
        # logger.debug(_)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error('Error updating document: %s', err)
        raise ResultNotExpected from err
    # logger.debug('Document updated')

def verify_index(client, index):
    """Verify the index exists and is an index, not an alias

    :param client: A client connection object
    :param index: The index to check

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str

    :returns: ``True`` if exists, ``False`` if it doesn't
    :rtype: bool
    """
    logger = logging.getLogger(__name__)
    logger.debug('Verifying index: %s', index)
    retval = True
    response = {}
    try:
        response = client.indices.get_settings(index=index)
    except (ApiError, NotFoundError, TransportError, BadRequestError) as err:
        logger.error("Index: '%s' not found. Error: %s", index, err)
        retval = False
    logger.debug(response)
    if len(list(response.keys())) > 1:
        # We have more than one key, that means we hit an alias
        logger.error('Index %s is one member of an alias.', index)
        retval = False
    elif list(response.keys())[0] != index:
        # There's a 1 to 1 alias, but it is not the index name
        logger.error('Index %s is an alias.', index)
        retval = False
    return retval
