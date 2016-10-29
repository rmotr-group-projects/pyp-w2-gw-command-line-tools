import sys
import os
import unittest
import csv
from mock import patch, MagicMock

from cmd_line_tools.mixins import *


class SimpleCommandLineParserMixinTestCase(unittest.TestCase):
    def test_with_arguments(self):
        testargs = ["my_script", "username=johndoe", "password=123"]
        with patch.object(sys, 'argv', testargs):
            m = SimpleCommandLineParserMixin()
            m.parse_arguments()
            self.assertEqual(m._arguments['username'], 'johndoe')
            self.assertEqual(m._arguments['password'], '123')

    def test_with_no_arguments(self):
        testargs = ["my_script"]
        with patch.object(sys, 'argv', testargs):
            m = SimpleCommandLineParserMixin()
            m.parse_arguments()
            self.assertEqual(len(m._arguments), 0)


class InputTestCase(unittest.TestCase):
    def test_with_simple_arguments_request(self):
        mixin = InputRequestMixin()
        # Patch Username
        with patch('six.moves.input', return_value='johndoe') as m:
            value = mixin.request_input_data('username')
            m.assert_called_once_with("Please provide username: ")
            self.assertEqual(value, 'johndoe')

        # Patch Password
        with patch('six.moves.input', return_value='PW123') as m:
            value = mixin.request_input_data('password')
            m.assert_called_once_with("Please provide password: ")
            self.assertEqual(value, 'PW123')


# See test_commands.py for an explanation of this test
def test_calculator_with_user_input(capsys):
    class DummyTestingClass(StdoutOutputMixin):
        def main(self):
            self.write("Hello World")
            self.write("Goodbye World")

    DummyTestingClass().main()
    out, err = capsys.readouterr()
    assert out == 'Hello World\nGoodbye World\n'


class AuthenticationMixinsTestCase(unittest.TestCase):

    def test_authenticate_user(self):
        authenticated_mock = MagicMock(return_value={
            'username': 'johndoe',
            'password': 'password'
        })

        class DummyLoginCommand(LoginMixin):
            def request_input_data(self, data):
                if data == 'username':
                    return 'johndoe'
                elif data == 'password':
                    return 'PWD$123'

            authenticate = authenticated_mock

        obj = DummyLoginCommand()
        user = obj.login()

        self.assertEqual(user, {
            'username': 'johndoe',
            'password': 'password'
        })
        self.assertEqual(user, obj.user)

        obj.authenticate.assert_called_once_with('johndoe', 'PWD$123')
        self.assertTrue(obj.is_authenticated)

    def test_invalid_user(self):
        authenticated_mock = MagicMock(return_value=None)

        class DummyLoginCommand(LoginMixin):
            def request_input_data(self, data):
                if data == 'username':
                    return 'no-user'
                elif data == 'password':
                    return 'no-pass'

            authenticate = authenticated_mock

        obj = DummyLoginCommand()
        user = obj.login()

        self.assertIsNone(user)
        obj.authenticate.assert_called_once_with('no-user', 'no-pass')
        self.assertFalse(obj.is_authenticated)
        self.assertIsNone(obj.user)

class JSONDataTestCase(unittest.TestCase):
    
    def test_json_data(self):
        class YahooWeather(JSONDataRequestMixin):
            # Default request url from yahoo weather api documentation, points to Nome, AK
            REQUEST_URL="https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak    %22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
            
            def get_city(self):
                return self.request_data()['query']['results']['channel']['location']['city']
        
        yahoo = YahooWeather()
        self.assertEqual(yahoo.get_city(), "Nome")
        
    def test_star_wars(self):
        class StarWars(JSONDataRequestMixin):
            REQUEST_URL="http://swapi.co/api/people/1"
            
            def get_name(self):
                return self.request_data()['name']
        
        luke = StarWars()
        self.assertEqual(luke.get_name(), "Luke Skywalker")
        
class PagedJSONDataTestCase(unittest.TestCase):
    def test_paged_data(self):
        class PokeTest(PagedJSONDataMixin):
            REQUEST_URL="http://pokeapi.co/api/v2/berry"
            
            def num_berries(self):
                return len(self.request_data())
            
        pokedata = PokeTest()
        self.assertEqual(pokedata.num_berries(), 64)
        
class CSVOutputTestCase(unittest.TestCase):
    def test_write_csv(self):
        class CSVWriter(CSVOutputMixin):
            FILE_PATH = 'test.csv'
            def test_write(self):
                test = {'test1': 'one', 'test2': 'two'}
                self.write(test)
        
        w = CSVWriter()
        # call write multiple times to make sure it isn't
        # messing up the dictionary order
        w.test_write()
        w.test_write()
        w.test_write()
        
        with open('test.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.assertEqual(row['test1'], 'one')
                self.assertEqual(row['test2'], 'two')
                
        # remove test file so we don't clutter up the filesystem
        os.remove(w.FILE_PATH)