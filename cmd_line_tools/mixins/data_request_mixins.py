import re
from six import moves


__all__ = ['InputRequestMixin', 'ArgumentsRequestMixin',
           'RequestValidatorMixin', 'ValidationError']


class ValidationError(Exception):
    pass


class RequestValidatorMixin(object):
    '''
    A validator mixin which depends on an object which implements the
    interface `request_input_data`
    '''
    _validators = {'slug_validator': '^[a-z0-9-]+$',
                   'email_validator':
                       '^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$',
                   'ip_address_validator':
                       '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)'
                       '{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                   'html_tag_validator':
                       '^<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$'}

    def _validate_regex(self, expression):
        '''
        returns true if regex is valid
        '''
        try:
            re.compile(expression)
            return True
        except re.error:
            return False

    def get_validators(self):
        return list(self._validators.keys)

    def validate(self, validator='.*'):
        # try to convert the validator to one of the built in expressions
        validator = self._validators.get(validator, validator)
        if self._validate_regex(validator):
            data = self.request_input_data('data')
            if re.match(validator, data):
                return data
            else:
                raise ValidationError('{} is not valid.'.format(data))


class InputRequestMixin(object):

    def request_input_data(self, input_name):
        value = moves.input("Please provide {}: ".format(input_name))
        return value


class ArgumentsRequestMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def request_input_data(self, input_name):
        return getattr(self, self.ARGUMENTS_ATTR_NAME).get(input_name)
