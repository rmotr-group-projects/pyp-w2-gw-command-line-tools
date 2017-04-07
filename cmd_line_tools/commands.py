from .mixins import (
    SimpleCommandLineParserMixin, ArgumentsRequestMixin, StdoutOutputMixin,
    InputRequestMixin, SimpleAuthenticationMixin,
    LoginMixin, CreateNewUserMixin, ResetPasswordMixin, JudgePatriceLessnerMixin)

__all__ = [
    'ArgumentCalculatorCommand', 'InputCalculatorCommand',
    'PriviledgedArgumentsExampleCommand', 'CreateNewUser', 'ResetPassword', 'JudgePatriceLessner']
import pdb

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

# New commands

class CreateNewUser(InputRequestMixin, 
                    CreateNewUserMixin, 
                    StdoutOutputMixin, 
                    SimpleCommandLineParserMixin):
    
    def main(self):
        new_user = self.create_new_user()
        self.write("User added to the list")
        
class ResetPassword(InputRequestMixin, 
                    ResetPasswordMixin, 
                    StdoutOutputMixin, 
                    SimpleCommandLineParserMixin,
                    LoginMixin,
                    SimpleAuthenticationMixin):
    AUTHORIZED_USERS = [{'username': "admin123", 'password': 'passW0rd123'}]
    
    def main(self):
        #pdb.set_trace()
        self.login()
        if self.is_authenticated:
            self.reset_password()
            self.write("Password successfully changed")

class JudgePatriceLessner(InputRequestMixin, JudgePatriceLessnerMixin):

    def main(self):
        yourhonour = str(self.request_input_data("your opinion"))
        
        inmyopinion = self.write(yourhonour)

        return inmyopinion
