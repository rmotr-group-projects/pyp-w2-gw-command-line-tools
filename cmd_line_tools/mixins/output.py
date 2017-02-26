import sys
import csv
import os

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


class CSVOutputMixin(object):
    """
    Outputs to CSV file
    Expects to receive dictionaries as input
    Outputs fields in order of sorted(keys)
    """
    FILE_PATH = None

    def write(self, message):
        if not self.FILE_PATH:
            raise ValueError("FILE_PATH not provided")

        file_exists = os.path.isfile(self.FILE_PATH)
        with open(self.FILE_PATH, 'a') as csvfile:
            fieldnames = list(sorted(message.keys()))
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Only write headers if new file.
            if not file_exists:
                writer.writeheader()
            writer.writerow(message)
