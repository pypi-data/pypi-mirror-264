"""Helper Functions"""
import logging
import json
from inspect import stack
from datetime import datetime
import re
from es_client.exceptions import ConfigurationError as esc_ConfigError
from es_client.helpers.schemacheck import SchemaCheck
from es_client.helpers.utils import get_yaml
from app.defaults import redaction_schema
from app.exceptions import ConfigurationException

def build_script(message, fields):
    """Build a painless script for redacting fields by way of an update_by_query operation

    :param message: The text to put in place of whatever is in a field
    :param fields: The list of field names to act on

    :type message: str
    :type fields: list

    :rtype: dict
    :returns: A dictionary of ``{"source": (the assembled message), "lang": "painless"}``
    """
    msg = ""
    for field in fields:
        msg += f"ctx._source.{field} = '{message}'; "
    script = {"source": msg, "lang": "painless"}
    return script

def chunk_index_list(indices):
    """
    This utility chunks very large index lists into 3KB chunks.
    It measures the size as a csv string, then converts back into a list for the return value.

    :param indices: The list of indices

    :type indices: list

    :returns: A list of lists (each a piece of the original ``indices``)
    :rtype: list
    """
    chunks = []
    chunk = ""
    for index in indices:
        if len(chunk) < 3072:
            if not chunk:
                chunk = index
            else:
                chunk += "," + index
        else:
            chunks.append(chunk.split(','))
            chunk = index
    chunks.append(chunk.split(','))
    return chunks

def end_it(obj, success):
    """Close out the object here to avoid code repetition"""
    # Record task success or fail here for THIS task_id
    # Each index in per_index has its own status tracker
    if not success:
        err = True
        log = 'Check application logs for detailed report'
    else:
        err = False
        log = 'DONE'
    obj.end(success, errors=err, logmsg=log)

def get_field_matches(config, result):
    """Count docs which have the expected fields

    :param config: The config from the YAML file
    :param result: The query result dict

    :type config: dict
    :type result: dict

    :returns: The count of docs in ``result`` which have the identified fields
    :rtype: int
    """
    logger = logging.getLogger(__name__)
    logger.debug('Extracting doc hit count from result')
    doc_count = result['hits']['total']['value']
    for element in range(0, result['hits']['total']['value']):
        for field in config['fields']:
            if len(field.split('.')) > 1:
                logger.debug('Dotted field "%s" detected...', field)
                fielder = result['hits']['hits'][element]['_source']
                for key in field.split('.'):
                    # This should recursively look for each subkey
                    if key in fielder:
                        fielder = fielder[key]
                    else:
                        doc_count -= 1
                        break
            elif field not in list(result['hits']['hits'][element]['_source'].keys()):
                logger.debug('Fieldname "%s" NOT detected...', field)
                doc_count -= 1
            else:
                logger.debug('Root-level fieldname "%s" detected...', field)
    return doc_count

def get_fname():
    """Return the name of the calling function"""
    return stack()[1].function

def get_index_version(name):
    """Extract a redacted index's version name from the end of the index

    :param name: The index name

    :type name: str

    :returns: The integer value of the current index revision, or 0 if no version
    :rtype: int
    """
    # Anchor the end as 3 dashes, a v, and 3 digits, e.g. ---v001
    match = re.search(r'^.*---v(\d{3})$', name)
    if match:
        return int(match.group(1))
    return 0

def get_redactions(file):
    """Return valid dictionary of redactions from ``file`` after checking Schema

    :param file: YAML file with redactions to check

    :type file: str

    :rtype: dict

    :returns: Redactions configuration data
    """
    logger = logging.getLogger(__name__)
    logger.debug('Getting redactions YAML file')
    try:
        from_yaml = get_yaml(file)
    except esc_ConfigError as exc:
        msg = f'Unable to read and/or parse YAML REDACTIONS_FILE: {file} Exiting.'
        logger.critical(msg)
        raise ConfigurationException(msg) from exc
    return SchemaCheck(
        from_yaml, redaction_schema(), 'Redaction Configuration', 'redactions').result()

def now_iso8601():
    """Get the current timestamp and return it in UTC ISO8601 time format with milliseconds"""
    iso8601 = datetime.utcnow().isoformat()
    return f'{iso8601[:-3]}Z'

def config_fieldmap(rw_val, key):
    """Return the function from this function/key map"""
    which = {
        'read': {
            'pattern': json.loads,
            'query': json.loads,
            'fields': json.loads,
            'message': str,
            'expected_docs': int,
            'restore_settings': json.loads,
            'delete': str
        },
        'write': {
            'pattern': json.dumps,
            'query': json.dumps,
            'fields': json.dumps,
            'message': str,
            'expected_docs': int,
            'restore_settings': json.dumps,
            'delete': str
        }
    }
    return which[rw_val][key]

def parse_job_config(config, behavior):
    """Parse raw config from the index. 
    
    Several fields are JSON escaped, so we need to fix it to put it in a dict.

    :param config: The raw config config
    :param behavior: ``read`` or ``write``

    :type config: dict
    :type behavior: str

    :rtype: dict

    :returns: JSON-(de)sanitized configuration dict
    """
    fields = [
        'pattern', 'query', 'fields', 'message', 'expected_docs', 'restore_settings', 'delete'
    ]
    doc = {}
    for field in fields:
        if field in config:
            func = config_fieldmap(behavior, field)
            doc[field] = func(config[field])
    return doc

def strip_index_name(name):
    """Strip ``partial-``, ``restored-``, ``redacted-``, and trailing ``---v000`` from ``name``

    :param name: The index name

    :type name: str

    :returns: The "cleaned up" and stripped index name
    :rtype: str
    """
    retval = name.replace('partial-', '')
    retval = retval.replace('restored-', '')
    retval = retval.replace('redacted-', '')
    # Anchor the end as 3 dashes, a v, and 3 digits, e.g. ---v001
    match = re.search(r'^(.*)---v\d{3}$', retval)
    if match:
        retval = match.group(1)
    return retval
