import sys
import argparse

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})
        # empty dict

        for argv in sys.argv:
            if '=' in argv:
                arguments.update(dict([tuple(argv.split('='))]))

        # Equivalent:
        # self._arguments = arguments
        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments)

'''
# Can you implement an argparse version?
class SimpleCommandLineArgParseMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'
    
    def parse_arguments(self):
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME,{})

        import pdb
        pdb.set_trace()      
        
        parser = argparse.ArgumentParser(description='Argmunt stuff')
        for argv  in sys.argv[1::]:

            parser.add_argument(argv) 
            parser.parse_args()

    
        setattr(self, self.ARGUMENTS_ATTR_NAME, vars(args))
'''