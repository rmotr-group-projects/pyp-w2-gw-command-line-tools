import sys
import unittest
import pytest
from mock import patch
import pdb
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

def login_test(message):
    if 'username' in message:
        return 'admin'
    if 'password' in message:
        return 'admin'

def test_login_privileges(capsys):
    with patch('six.moves.input',login_test) as m:
        PriviledgedArgumentsExampleCommand().main()
    
    out,err = capsys.readouterr()
    print('"{}"'.format(out))
    assert out.startswith('Welcome')

def new_user1(message):
    if 'username' in message:
        return 'user1'
    if 'password' in message:
        return 'pAssw0rd'

def test_new_user(capsys):
    with patch('six.moves.input',new_user1) as m:
        CreateNewUser().main()
    
    out,err = capsys.readouterr()
    assert out.startswith('User added')

def new_password(message):
    if "username" in message:
        return "admin123"
    elif 'new password' in message:
        return 'pAssw0rd'
    elif 'password' in message:
        return "passW0rd123"
    
def test_reset_password(capsys):
    #pdb.set_trace()
    rp = ResetPassword()
    old_password = rp.AUTHORIZED_USERS[0]['password']
    with patch('six.moves.input',new_password) as m:
        rp.main()
    new_user_password = rp.AUTHORIZED_USERS[0]['password']
    out,err = capsys.readouterr()
    print(out)
    assert old_password != new_user_password
    assert 'Password succ' in out

def your_honour(message):
    if 'What' in message:
        return 'A log may float in a river, but that does not make it a crocodile'

def test_judge_patrice_lessner(capsys):
    with patch('six.moves.input', your_honour) as m:
        JudgePatriceLessner().main()
    
    out,err = capsys.readouterr()
    assert "in my opinion" in out