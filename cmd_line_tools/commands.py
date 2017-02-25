from cmd_line_tools.mixins import (
    SimpleCommandLineParserMixin, ArgumentsRequestMixin, StdoutOutputMixin,
    InputRequestMixin, SimpleAuthenticationMixin, LoginMixin, WeatherMixin,
    ApiCheckMixin)

__all__ = [
    'ArgumentCalculatorCommand', 'InputCalculatorCommand',
    'PriviledgedArgumentsExampleCommand', 'WeatherMixin', 'ApiCheckMixin', 
    'ArgumentWeatherCommand', 'InputWeatherCommand']


class BaseCalculatorCommand(object):
    """Base command to demonstrate the parsing/requesting mixins."""

    OPERATIONS = {
        'addition': lambda x, y: x + y,
        'subtraction': lambda x, y: x - y,
        'multiplication': lambda x, y: x * y,
        'division': lambda x, y: x / y,
    }

    def calculate(self):
        x_value = int(self.request_input_data('x_value'))
        y_value = int(self.request_input_data('y_value'))
        operation = self.request_input_data('operation')

        if operation not in self.OPERATIONS:
            raise AttributeError('Invalid Operation: %s' % operation)

        return self.OPERATIONS[operation](x_value, y_value)


class ArgumentCalculatorCommand(SimpleCommandLineParserMixin,
                                ArgumentsRequestMixin,  # Different mixin
                                StdoutOutputMixin,
                                BaseCalculatorCommand):
    """Extends the BaseCalculatorCommand to receive cmd line arguments.

    Should be invoked:
    - python cmd.py x_value=15 y_value=7 operation=addition
    """

    def main(self):
        self.parse_arguments()
        result = self.calculate()
        self.write("Result: {}".format(result))


class InputCalculatorCommand(SimpleCommandLineParserMixin,
                             InputRequestMixin,  # Different mixin
                             StdoutOutputMixin,
                             BaseCalculatorCommand):
    """Extends the BaseCalculatorCommand and will ask for user input.

    Should be invoked:
    - python cmd.py
    """

    def main(self):
        result = self.calculate()
        self.write("Result: {}".format(result))


class PriviledgedArgumentsExampleCommand(SimpleCommandLineParserMixin,
                                         InputRequestMixin,
                                         StdoutOutputMixin,
                                         SimpleAuthenticationMixin,
                                         LoginMixin):
    AUTHORIZED_USERS = [{
        'username': 'admin',
        'password': 'admin'
    }, {
        'username': 'rmotr',
        'password': 'python'
    }]

    def main(self):
        if self.is_authenticated:
            username = self.user['username']
            self.write("Welcome %s!" % username)
        else:
            self.write("Not authorized :(")


class BaseWeatherCommand(object):
    """Base command for Checking the Weather using OpenWeatherMap's API.
    The user will first be authenticated by username and password. Then, 
    an API key must be entered to check that it is valid. When requesting
    the weather, a zipcode(11229, 90210, etc) and country code(us, nz, etc)
    must also be entered."""
    AUTHORIZED_USERS = [{
        'username': 'admin',
        'password': 'admin'
    }, {
        'username': 'rmotr',
        'password': 'python'
    }, {
        'username': 'rmotr_user',
        'password': 'python123'
    }]
    def make_weather_request(self):
        if self.is_authenticated:
            api_key = self.request_input_data("api_key")
            if self.authenticate_key(api_key):
                userzip = self.request_input_data("zipcode")
                usercountry = self.request_input_data("countrycode")
                user_weather = self.checkweather(userzip, usercountry, api_key)
                return user_weather
            return "Sorry, your API key is not valid! :( </3"
        return "Sorry, you are not authenticated to use this super secret API..."


class ArgumentWeatherCommand(SimpleCommandLineParserMixin,
                                ArgumentsRequestMixin, 
                                StdoutOutputMixin, WeatherMixin,
                                BaseWeatherCommand, LoginMixin,
                                SimpleAuthenticationMixin, ApiCheckMixin):
    
    """Extends the BaseCalculatorCommand to receive cmd line arguments."""
    def main(self):
        self.parse_arguments()
        result = self.make_weather_request()
        if __name__ == '__main__':
            weather_statement = "The temperature is {} degrees with {}.".format(result["main"]["temp"], result["weather"][0]["description"])
            self.write("Result: {}".format(weather_statement))
        else:
            self.write("Result: {}, {}".format(result["name"], result["sys"]["country"]))


class InputWeatherCommand(SimpleCommandLineParserMixin,
                             InputRequestMixin,  # Different mixin
                             StdoutOutputMixin,
                             BaseWeatherCommand, WeatherMixin,
                            SimpleAuthenticationMixin, LoginMixin, ApiCheckMixin):
    
    """Extends the BaseWeatherCommand and will ask for user input."""
    def main(self):
        result = self.make_weather_request()
        if __name__ == '__main__':
            weather_statement = "The temperature is {} degrees with {}.".format(result["main"]["temp"], result["weather"][0]["description"])
            self.write("Result: {}".format(weather_statement))
        else:
            self.write("Result: {}, {}".format(result["name"], result["sys"]["country"]))