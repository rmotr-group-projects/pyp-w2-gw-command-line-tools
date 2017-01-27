from mixins import (
    SimpleCommandLineParserMixin, ArgumentsRequestMixin, StdoutOutputMixin,
    InputRequestMixin, SimpleAuthenticationMixin,
    LoginMixin)
import random
import requests

__all__ = [
    'ArgumentCalculatorCommand', 'InputCalculatorCommand',
    'PriviledgedArgumentsExampleCommand', 'RockPaperScissorsGame', 'StockInfo']


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


class RockPaperScissorsGame(SimpleCommandLineParserMixin,
                            InputRequestMixin,
                            StdoutOutputMixin):
    
    POSSIBLE_ARGUMENTS = ['paper', 'rock', 'scissors']
    
    def main(self):
        input_choice = self.request_input_data('choice').lower()
        if input_choice not in self.POSSIBLE_ARGUMENTS:
            self.write("You lose, that's not a valid choice!")
        computer_choice = random.choice(self.POSSIBLE_ARGUMENTS)
        if input_choice == computer_choice:
            self.write("I chose {}. It's a tie.".format(computer_choice))
        elif input_choice == 'paper':
            if computer_choice == 'scissors':
                self.write("I chose {}. I win!".format(computer_choice))
            elif computer_choice == 'rock':
                self.write("I chose {}. You win!".format(computer_choice))
        elif input_choice == 'rock':
            if computer_choice == 'paper':
                self.write("I chose {}. I win!".format(computer_choice))
            elif computer_choice == 'scissors':
                self.write("I chose {}. You win!".format(computer_choice))
        elif input_choice == 'scissors':
            if computer_choice == 'rock':
                self.write("I chose {}. I win!".format(computer_choice))
            elif computer_choice == 'paper':
                self.write("I chose {}. You win!".format(computer_choice))


class StockInfo(InputRequestMixin,ArgumentsRequestMixin,StdoutOutputMixin):
    stock_price = type(float)
    
    def main(self):
        # you need to enter a valid ticker (e.g. GOOGL)
        ticker = self.request_input_data('ticker') 
        stock_info_url = 'https://www.google.com/finance/info?q='
        r = requests.get(stock_info_url + ticker)
        # clean up results to make readable in python
        t1 = str(r.text).replace(' ','').replace('\n','') 
        t2 = t1[3:-1] # extract the dict portion
        try:
            # This is the line where the error raised so I put the try there
            ticker_info = eval(t2) # convert to python dict       
            stock_price = ticker_info['l'] # stock price
        except:                                           
            raise SyntaxError("Not a valid ticker.")
        print('{0} is trading at {1}.'.format(ticker, stock_price))
