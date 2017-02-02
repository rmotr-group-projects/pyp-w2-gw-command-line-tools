import sys
import unittest
import pytest
from mock import patch, MagicMock

from cmd_line_tools.commands import *

__name__ = 'test_commands'

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
    with patch('six.moves.input', something):
        InputCalculatorCommand().main()

    out, err = capsys.readouterr()
    assert out == 'Result: 2\n'


def test_weather_with_arguments(capsys):
    testargs = ["cmd", "username=rmotr_user", "password=python123", "api_key=2cc9c28ac5bc116faba3f6609fba562f", "zipcode=90210", "countrycode=us"]
    with patch.object(sys, 'argv', testargs):
        ArgumentWeatherCommand().main()

    out, err = capsys.readouterr()
    assert out == 'Result: Beverly Hills, US\n'


def weather_params(message):
    if 'username' in message:
        return 'rmotr_user'
    if 'password' in message:
        return 'python123'
    if 'api_key' in message:
        return '2cc9c28ac5bc116faba3f6609fba562f' 
    if 'zipcode' in message:
        return '11229'
    if 'countrycode' in message:
        return 'us'


def test_weather_with_user_input(capsys):
    with patch('six.moves.input', weather_params):
        InputWeatherCommand().main()
    out, err = capsys.readouterr()
    assert out == 'Result: Bensonhurst, US\n'
