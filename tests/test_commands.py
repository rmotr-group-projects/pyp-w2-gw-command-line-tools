import sys
import unittest
import pytest
from mock import patch

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

def password_input(message):
    if 'username' in message:
        return 'admin'
    if 'password' in message:
        return 'admin'
    
def test_login(capsys):
    
    
    with patch('six.moves.input', password_input) as x:
        PriviledgedArgumentsExampleCommand().main()
    
    out, err = capsys.readouterr()
    assert out == 'Welcome admin!\n'


def toDoInput(message):
    if 'title' in message:
        return 'complete decorators assignments'
    if 'body' in message:
        return 'There are a number of class assignments for python decorators'
    if 'questions' in message:
        return 6
    if 'Would you like to view?' in message:
        return 'y'

def test_to_do_list(capsys):
    
    with patch('six.moves.input', toDoInput) as x:
        ToDoListCommand().main()
    
    out, err = capsys.readouterr()
    assert out ==  "{'body': 'There are a number of class assignments for python decorators',\n 'questions': 6,\n 'title': 'complete decorators assignments'}\n"