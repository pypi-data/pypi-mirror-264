"""App Defaults"""
from six import string_types
from voluptuous import All, Any, Boolean, Coerce, Optional, Range, Required, Schema

TRACKING_INDEX = 'redactions-tracker'

CLICK_DRYRUN = {
    'dry-run': {'help': 'Do not perform any changes.', 'is_flag': True}
}

CLICK_TRACKING = {
    'tracking-index': {
        'help': 'Name for the tracking index.',
        'default': TRACKING_INDEX,
        'show_default': True,
    }
}


# pylint: disable=E1120

def forcemerge_schema():
    """Define the forcemerge schema"""
    return {
        Optional('max_num_segments', default=1): All(Coerce(int), Range(min=1, max=32768)),
        Optional('only_expunge_deletes', default=False): Any(bool, All(Any(*string_types), Boolean()))
    }

def redactions_schema():
    """
    An index pattern to search and redact data from
    """
    merge = forcemerge_schema()
    return {
        Optional(Any(*string_types)): {
            Required('pattern'): Any(*string_types),
            Required('query'): dict,
            Required('fields'): [Any(*string_types)],
            Required('message', default='REDACTED'): Any(*string_types),
            Optional('delete', default=True): Any(bool, All(Any(*string_types), Boolean())),
            Required('expected_docs'): All(Coerce(int), Range(min=1, max=32768)),
            Optional('restore_settings', default=None): Any(dict, None),
            Optional('forcemerge'): merge,
        }
    }

def index_settings():
    """The Elasticsearch index settings for the progress/status tracking index"""
    return {'index': {'number_of_shards': '1'}}

def status_mappings():
    """The Elasticsearch index mappings for the progress/status tracking index"""
    return {
        "properties": {
            "job": {"type": "keyword"},
            "task": {"type": "keyword"},
            "join_field": { 
                "type": "join",
                "relations": {
                    "job": "task" 
                }
            },
            "cleanup": {"type": "keyword"},
            "completed": {"type": "boolean"},
            "end_time": {"type": "date"},
            "errors": {"type": "boolean"},
            "dry_run": {"type": "boolean"},
            "index": {"type": "keyword"},
            "logs": {"type": "text"},
            "start_time": {"type": "date"}
        },
        "dynamic_templates": [
            {
                "configuration": {
                    "path_match":   "config.*",
                    "mapping": {
                        "type": "keyword",
                        "index": False
                    }
                }
            }
        ]
    }

def redaction_schema():
    """The full voluptuous Schema for a redaction file
    """
    return Schema(
        {
            Required('redactions'): [redactions_schema()]
        }
    )

def progress_filename():
    """The name of the file tracking progress
    """
    return 'script_progress'

def snapshot_filename():
    """The name of the file tracking which snapshots should be deleted
    """
    return 'snapshotstodelete'
