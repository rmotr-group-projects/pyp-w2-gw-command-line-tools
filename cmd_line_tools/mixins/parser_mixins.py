import sys
import argparse

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    
    ARGUMENTS_ATTR_NAME = '_arguments'

# Can you implement an argparse version?
    def parse_arguments(self):
        p = argparse.ArgumentParser()
        p.add_argument('cmd', nargs='*')
        args = vars(p.parse_args())
        pos = args.pop('cmd')
        d = dict(i.split('=') for i in pos if '=' in i)
        setattr(self, self.ARGUMENTS_ATTR_NAME, d)