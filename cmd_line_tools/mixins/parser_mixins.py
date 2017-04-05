import sys

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})

        for argv in sys.argv:
            if '=' in argv:
                arguments.update(dict([tuple(argv.split('='))]))

        # Equivalent:
        # self._arguments = arguments
        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments)


# Can you implement an argparse version?

class CommaSeparatedCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'


    def parse_arguments(self):
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, [])

        args_list = sys.argv
        if len(args_list) <= 1:
            arguments.append(args_list[0])

        else:
            actual_args = args_list[1]
            arguments.append(args_list[0])
            for arg_item in actual_args.split(","):
                arguments.append(arg_item)

        # Equivalent:
        # self._arguments = arguments
        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments)
