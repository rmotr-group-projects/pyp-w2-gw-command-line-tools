import sys
from six import moves

import unittest
from mock import patch



class RequestUserCredentials(object):
    def read_user(self):
        self.username = self.request_input_data('username')


unittest.main()
