"""Redacter Tool Exceptions"""
### Parent exception
class RedacterException(Exception):
    """
    Base class for all exceptions raised by the tool which are not Elasticsearch
    exceptions.
    """
###

class ClientException(RedacterException):
    """
    Exception raised when the Elasticsearch client and/or connection is the source of the problem.
    """

class ConfigurationException(RedacterException):
    """
    Exception raised when there is a configuration error
    """

class FailedReindex(ClientException):
    """
    Exception raised when return value from Elasticsearch API indicates one or more failures.
    """

class MissingArgument(ConfigurationException):
    """
    Exception raised when a required argument or parameter is missing
    """

class MissingIndex(ClientException):
    """
    Exception raised when an index is expected but not found
    """

class MissingDocument(ClientException):
    """
    Exception raised when a document in an index is expected but not found
    """

class ResultNotExpected(ClientException):
    """
    Exception raised when return value from Elasticsearch API call is not or does not contain the
    expected result.
    """

class TimeoutException(RedacterException):
    """
    Exception raised when a task has failed because the allotted time ran out
    """

class ValueMismatch(ConfigurationException):
    """
    Exception raised when a received value does not match what was expected.

    This is particularly used when ``expected_docs`` is specified but a different value is
    returned at query time.
    """

class FatalException(RedacterException):
    """
    Exception raised when the program should be halted.
    """
