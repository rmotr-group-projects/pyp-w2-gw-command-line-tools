import sys
from pprint import pprint

__all__ = ['StdoutOutputMixin', 'FileOutputMixin','OutputJSONMixin']


class StdoutOutputMixin(object):
    def write(self, message):
        sys.stdout.write(message + '\n')


class FileOutputMixin(object):
    FILE_PATH = None

    def write(self, message):
        if not self.FILE_PATH:
            raise ValueError("FILE_NAME not provided")

        with open(self.FILE_PATH, 'a') as fp:
            fp.write(message)

class OutputJSONMixin(object):
    
    def output_json(self, data):
        from pprint import pprint
        return pprint(data)