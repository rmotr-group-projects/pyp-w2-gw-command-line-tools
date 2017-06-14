import logging, inspect

__all__ = ['LoggingMixin']

class LoggingMixin(object):
    def log(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        print( "Running function %s" % inspect.stack()[1][3])
        print("-"*10)
        #print( "Running function %s" % self.__class__.__name__)