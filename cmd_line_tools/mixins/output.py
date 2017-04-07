import sys

__all__ = ['StdoutOutputMixin', 'FileOutputMixin']


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

class JudgePatriceLessnerMixin(object):
    """
    In the CBS show 'The Good Wife', Judge Patrice Lessner requires all lawyers
    in her courtroom follow an argument or statement with 'in my opinion.'

    This mixin allows you to do the same with random quotations.
    """
    def write(self, message):
        sys.stdout.write(message + ', in my opinion.')