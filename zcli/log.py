import logging


class zlog (object):
    """This intermediates stdlib logging to facilitate mocking."""

    warn = staticmethod(logging.warn)
    debug = staticmethod(logging.debug)
