from six import moves
from .parser_mixins import SimpleCommandLineParserMixin
from io import open

__all__ = ['InputRequestMixin', 'ArgumentsRequestMixin']


class InputRequestMixin(object):
    def request_input_data(self, input_name):
        value = moves.input("Please provide {}: ".format(input_name))
        return value


class ArgumentsRequestMixin(SimpleCommandLineParserMixin):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def request_input_data(self, input_name):
        self.parse_arguments()
        return getattr(self, self.ARGUMENTS_ATTR_NAME).get(input_name)
        
class FileRequestMixin(object):
    def request_input_data(self, input_name):
        if input_name == self.FILE_KEY:
            with open(self.FILE_NAME, encoding = 'utf-8') as file:
                return file.read()
        else:
            return super(FileRequestMixin, self).request_input_data(input_name)