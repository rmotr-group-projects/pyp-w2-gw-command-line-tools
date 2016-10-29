from six import moves

import requests
import json

__all__ = ['InputRequestMixin', 'ArgumentsRequestMixin']


class InputRequestMixin(object):
    def request_input_data(self, input_name):
        value = moves.input("Please provide {}: ".format(input_name))
        return value


class ArgumentsRequestMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def request_input_data(self, input_name):
        return getattr(self, self.ARGUMENTS_ATTR_NAME).get(input_name)


class JSONDataRequestMixin(object):
    #Assumes self.REQUEST_URL exists
    def request_input_data(self, input_name):
        data = self._get(self.REQUEST_URL)
        return data[input_name]
    
    def _get(self,url,params=None):
        r = requests.get(url, params=params)
        return r.json()
    
    