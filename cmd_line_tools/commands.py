from .mixins import (
    SimpleCommandLineParserMixin, ArgumentsRequestMixin, StdoutOutputMixin,
    InputRequestMixin, SimpleAuthenticationMixin,
    LoginMixin, LangDetectMixin, FileRequestMixin)
from .languages import LANGUAGES as langs

__all__ = [
    'ArgumentCalculatorCommand', 'InputCalculatorCommand',
    'PriviledgedArgumentsExampleCommand', 'InputLangAnalyzer', 'ArgumentLangAnalyzer', 'FileArgumentLangAnalyzer']


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
        
    def main(self):
        result = self.calculate()
        self.write("Result: {}".format(result))


class ArgumentCalculatorCommand(ArgumentsRequestMixin,  # Different mixin
                                StdoutOutputMixin,
                                BaseCalculatorCommand):
    """Extends the BaseCalculatorCommand to receive cmd line arguments.

    Should be invoked:
    - python cmd.py x_value=15 y_value=7 operation=addition
    """
    pass

class InputCalculatorCommand(InputRequestMixin,  # Different mixin
                             StdoutOutputMixin,
                             BaseCalculatorCommand):
    """Extends the BaseCalculatorCommand and will ask for user input.

    Should be invoked:
    - python cmd.py
    """
    pass

class PriviledgedArgumentsExampleCommand(InputRequestMixin,
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

class LangAnalyzerBase(LangDetectMixin, StdoutOutputMixin):
    #Possible TODO:
    #language file location as cmd argument
    #extract language file contents, store it
    LANGUAGES = langs
    
    def analyze_user_text(self):
        text = self.request_input_data('text')
        language = self.detect_language(text)
        self.write('Analysis has detected {}.'.format(language))
        
    main = analyze_user_text
        
class InputLangAnalyzer(LangAnalyzerBase, InputRequestMixin):
    pass
    
class ArgumentLangAnalyzer(LangAnalyzerBase, ArgumentsRequestMixin):
    """
    should be invoked with command line parameter of this form: text="blah blah blah"
    """
    pass

class FileArgumentLangAnalyzer(FileRequestMixin, ArgumentLangAnalyzer):
    FILE_KEY = 'text'
    """
    pass a file via cmd line parameter file=filename
    """
    def main(self):
        self.FILE_NAME = self.request_input_data('file')
        return super(FileArgumentLangAnalyzer, self).main()
        