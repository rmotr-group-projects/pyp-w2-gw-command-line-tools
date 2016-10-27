from six import moves


class InputRequestMixin(object):
    def request_input_data(self, input_name):
        value = moves.input("Please provide {}: ".format(input_name))
        return value


class ArgumentsRequestMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def request_input_data(self, input_name):
        return getattr(self, self.ARGUMENTS_ATTR_NAME).get(input_name)
