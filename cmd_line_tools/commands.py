from .mixins import (
    SimpleCommandLineParserMixin, ArgumentsRequestMixin, StdoutOutputMixin,
    InputRequestMixin, SimpleAuthenticationMixin,
    LoginMixin)

__all__ = [
    'ArgumentCalculatorCommand', 'InputCalculatorCommand',
    'PriviledgedArgumentsExampleCommand', 'PolishSpeak']


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
#TODO: sqlite3 connect 
#TODO: json connect
     
    
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

class PolishSpeak(SimpleCommandLineParserMixin, InputRequestMixin, StdoutOutputMixin ):
    
    def EnglishInput(self):
        sentence = str(self.request_input_data('EnglishSentence'))
        joiner = 'skee '
        new_word = sentence.split()
        joined_word = joiner.join(new_word)
        joined_word += 'skee'
        
        return joined_word
        
    def main(self):
        Polish = self.EnglishInput()
        self.write("Your Polish-speak is: {}".format(Polish))
        
       