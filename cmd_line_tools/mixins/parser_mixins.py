import sys
import argparse

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):
        # arguments = self._arguments or {}
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})

        for argv in sys.argv:
            if '=' in argv:
                arguments.update(dict([tuple(argv.split('='))]))

        # Equivalent:
        # self._arguments = arguments
        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments)


# Can you implement an argparse version?
class ArgParseCommandLineParserMixin(object):
    """
    python cmd.py --x_value 5 --y_value 7
    sys.argv == ["--x_value", 5, "--y_value", 7]
    parser.add_argument('--x_value')
    parser.add_argument('--y_value')
    args = parser.parse_args(sys.argv)
    print(vars(args))
    """
    """
    sys.argv == ["my_script", '--x_value', 5, '--y_value', 7]
    args = sys.argv[1::]
    for idx, arg in enumerate(args):
        if idx % 2 == 0:
            parser.add_argument(arg)
    """
    ARGUMENTS_ATTR_NAME = '_arguments'
    
    def parse_arguments(self):
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})
        
        parser = argparse.ArgumentParser('Process some arguments.')
        args = sys.argv[1::] 
        for idx, arg in enumerate(args):
            if idx % 2 == 0:
                parser.add_argument(arg)
                
        arguments.update(vars(parser.parse_args()))
        
        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments)