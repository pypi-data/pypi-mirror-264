.. _readme:

elastic-pii-redacter
====================

Did you find PII (Personally Identifiable Information) in your Elasticsearch
indices that doesn't belong there? This is the tool for you!

The elastic-pii-redacter can help you redact information from even Searchable
Snapshot mounted indices. It works with deeply nested fields, too!


Client Configuration
--------------------

The tool connects using the ``es_client`` Python module.

You can use command-line options, or a YAML configuration file to configure the client connection.
If using a configuration file is desired, the configuration file structure requires
``elasticsearch`` at the root level as follows::

    ---
    elasticsearch:
      client:
        hosts: https://10.11.12.13:9200
        cloud_id:
        bearer_auth:
        opaque_id:
        request_timeout: 60
        http_compress:
        verify_certs:
        ca_certs:
        client_cert:
        client_key:
        ssl_assert_hostname:
        ssl_assert_fingerprint:
        ssl_version:
      other_settings:
        master_only:
        skip_version_test:
        username:
        password:
        api_key:
          id:
          api_key:
          token:

    logging:
      loglevel: INFO
      logfile: /path/to/file.log
      logformat: default
      blacklist: []


`REDACTIONS_FILE` Configuration
-------------------------------

::

  ---
  redactions:
    - job_name_20230731_redact_hot:
        pattern: hot-*
        query: {'match': {'message': 'message1'}}
        fields: ['message']
        message: REDACTED
        expected_docs: 1
        restore_settings: {'index.routing.allocation.include._tier_preference': 'data_warm,data_hot,data_content'}
    - job_name_20230731_redact_cold:
        pattern: restored-cold-*
        query: {'match': {'nested.key': 'nested19'}}
        fields: ['nested.key']
        message: REDACTED
        expected_docs: 1
        restore_settings: {'index.routing.allocation.include._tier_preference': 'data_warm,data_hot,data_content'}
        forcemerge:
          max_num_segments: 1
    - job_name_20230731_redact_frozen:
        pattern: partial-frozen-*
        query: {'range': {'number': {'gte': 8, 'lte': 11}}}
        fields: ['deep.l1.l2.l3']
        message: REDACTED
        expected_docs: 4
        forcemerge:
          only_expunge_deletes: True
