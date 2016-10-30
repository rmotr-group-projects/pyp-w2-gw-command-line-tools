import sys

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})

        for arg in sys.argv:
            if '=' in arg:
                #arguments.update(dict([tuple(arg.split('='))]))
                key, value = arg.split('=')
                arguments[key] = value

        # Equivalent:
        self._arguments = arguments
        #setattr(self, self.ARGUMENTS_ATTR_NAME, arguments)


# Can you implement an argparse version?
