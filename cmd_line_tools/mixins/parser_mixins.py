import sys

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})

        for arg in sys.argv:
            if '=' in arg:
                key, value = arg.split('=')
                arguments[key] = value
        self._arguments = arguments
        
    def __init__(self, *args, **kwargs):
        self.parse_arguments()
        super(SimpleCommandLineParserMixin,self).__init__(*args, **kwargs)