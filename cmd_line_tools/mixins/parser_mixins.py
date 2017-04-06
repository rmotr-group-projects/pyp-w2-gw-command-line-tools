import sys
import argparse

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    
    ARGUMENTS_ATTR_NAME = '_arguments'

# Can you implement an argparse version?
    def parse_arguments(self):
        p = argparse.ArgumentParser()
        p.add_argument('cmd', nargs='*')
        setattr(
        self, 
        self.ARGUMENTS_ATTR_NAME, 
        dict(i.split('=') for i in vars(p.parse_args()).pop('cmd') if '=' in i)
        )