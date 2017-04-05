import sys
import unittest
import pytest
from mock import patch
from freezegun import freeze_time

from cmd_line_tools.commands import *


# These tests are written in a different way than the ones you're probably
# used to. We're using a neat py.test feature called "Fixtures". In particular
# we're using capture fixtures.
# Read more here: http://doc.pytest.org/en/latest/capture.html
def test_calculator_with_arguments(capsys):
    testargs = ["cmd", "x_value=15", "y_value=7", "operation=addition"]
    with patch.object(sys, 'argv', testargs):
        ArgumentCalculatorCommand().main()

    out, err = capsys.readouterr()
    assert out == 'Result: 22\n'


def something(message):
    if 'x_value' in message:
        return '7'
    if 'y_value' in message:
        return '5'
    if 'operation' in message:
        return 'subtraction'


def test_calculator_with_user_input(capsys):
    with patch('six.moves.input', something) as m:
        InputCalculatorCommand().main()

    out, err = capsys.readouterr()
    assert out == 'Result: 2\n'

def authorized_input_calculator_cmd_responses(message):
    if 'Please provide username: ' in message:
        return 'admin'
    if 'Please provide password: ' in message:
        return 'admin'
    if 'Please provide x_value: ' in message:
        return '2'
    if 'Please provide y_value: ' in message:
        return '3'
    if 'Please provide operation: ' in message:
        return 'multiplication'
        
        
def unauthorized_input_calculator_cmd_responses(message):
    if 'Please provide username: ' in message:
        return 'not_admin'
    if 'Please provide password: ' in message:
        return 'h4ckoR'
    if 'Please provide x_value: ' in message:
        return '1'
    if 'Please provide y_value: ' in message:
        return '5'
    if 'Please provide operation: ' in message:
        return 'addition'
        
@freeze_time('2017-04-04T12:00:00Z')     
def test_unauthorized_input_calculator_command(capsys):
    # perform action no logging
    # otherwise:
    #   perform action, log action, let user know action was logged
    
    # Test 1: pass authorized user, multiply 2*3
    
    # ask for username: pw
     # if auth is valid: 
    with patch('six.moves.input', authorized_input_calculator_cmd_responses) as m:
        LogUnauthorizedInputCalculatorCommand().main()
        out, err = capsys.readouterr()
        assert out == 'Authorized\nresult was 6\n'
        
    with patch('six.moves.input', unauthorized_input_calculator_cmd_responses) as m:
        LogUnauthorizedInputCalculatorCommand().main()
        out, err = capsys.readouterr()
        assert out == "Unauthorized login\n"
        
        with open('./logs/log.txt', 'r') as fp:
            for line in fp:
                pass
            last = line
        assert last == 'Unauthorized login at : 2017-04-04 12:00:00\n'
        
        
        # Test 2: pass unauthorized user, add 1 + 5
        # take input for command
        # x_value = int(self.request_input_data('x_value'))
        # y_value = int(self.request_input_data('y_value'))
        # operation = self.request_input_data('operation')
        
    

    
    
    # Test 2: pass unauthorized user, add 1 + 1
    
    
    
    