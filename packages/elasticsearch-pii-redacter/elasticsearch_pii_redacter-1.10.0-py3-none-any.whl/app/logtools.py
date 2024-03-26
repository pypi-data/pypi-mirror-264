"""Logging tools"""
import sys
import logging
import ecs_logging

class Whitelist(logging.Filter):
    """How to whitelist logs"""
    # pylint: disable=super-init-not-called
    def __init__(self, *whitelist):
        self.whitelist = [logging.Filter(name) for name in whitelist]

    def filter(self, record):
        return any(f.filter(record) for f in self.whitelist)

class Blacklist(Whitelist):
    """Blacklist monkey-patch of Whitelist"""
    def filter(self, record):
        return not Whitelist.filter(self, record)

class LogInfo:
    """Logging Class"""
    def __init__(self, cfg):
        """Class Setup

        :param cfg: The logging configuration
        :type: cfg: dict
        """
        cfg['loglevel'] = 'INFO' if not 'loglevel' in cfg else cfg['loglevel']
        cfg['logfile'] = None if not 'logfile' in cfg else cfg['logfile']
        cfg['logformat'] = 'default' if not 'logformat' in cfg else cfg['logformat']
        #: Attribute. The numeric equivalent of ``cfg['loglevel']``
        self.numeric_log_level = getattr(logging, cfg['loglevel'].upper(), None)
        #: Attribute. The logging format string to use.
        self.format_string = '%(asctime)s %(levelname)-9s %(message)s'

        if not isinstance(self.numeric_log_level, int):
            msg = f"Invalid log level: {cfg['loglevel']}"
            print(msg)
            raise ValueError(msg)

        #: Attribute. Which logging handler to use
        self.handler = logging.StreamHandler(stream=sys.stdout)
        if cfg['logfile']:
            self.handler = logging.FileHandler(cfg['logfile'])

        if self.numeric_log_level == 10: # DEBUG
            self.format_string = (
                '%(asctime)s %(levelname)-9s %(name)22s %(funcName)22s:%(lineno)-4d %(message)s')

        if cfg['logformat'] == 'ecs':
            self.handler.setFormatter(ecs_logging.StdlibFormatter())
        else:
            self.handler.setFormatter(logging.Formatter(self.format_string))
