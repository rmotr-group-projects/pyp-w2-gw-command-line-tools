from six import moves
import timeit

__all__ = ['InputRequestMixin', 'ArgumentsRequestMixin', 'TimingMixin']


class InputRequestMixin(object):
    def request_input_data(self, input_name):
        value = moves.input("Please provide {}: ".format(input_name))
        return value


class ArgumentsRequestMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def request_input_data(self, input_name):
        return getattr(self, self.ARGUMENTS_ATTR_NAME).get(input_name)

class TimingMixin(object):
    def function_time(self, func):
        return timeit.timeit(func)
    
