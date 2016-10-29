import random

from .mixins import (
    SimpleCommandLineParserMixin, ArgumentsRequestMixin, StdoutOutputMixin,
    InputRequestMixin, SimpleAuthenticationMixin,
    LoginMixin, JSONDataRequestMixin, PagedJSONDataMixin, CSVOutputMixin)

__all__ = [
    'ArgumentCalculatorCommand', 'InputCalculatorCommand',
    'PriviledgedArgumentsExampleCommand', 'InputBasedPokemon',
    'CommandLinePokemon','RandomChooserPokemon','PokemonBerryPrinter',
    'PokemonBerryCSVWriter']

class BaseAllPokemonBerriesCommand(object):
    REQUEST_URL = 'http://pokeapi.co/api/v2/berry/'
    
    def get_pokemon(self):
        return self.request_data()
        
class PokemonBerryPrinter(PagedJSONDataMixin,
                     StdoutOutputMixin,
                     BaseAllPokemonBerriesCommand):
    def main(self):
        results = self.get_pokemon()
        for berry in results:
            self.write(berry['name'])
 
class PokemonBerryCSVWriter(PagedJSONDataMixin,
                             CSVOutputMixin,
                             BaseAllPokemonBerriesCommand):
    FILE_PATH='pokemonberries.csv'
    
    def main(self):
        results = self.get_pokemon()
        for berry in results:
            self.write(berry)       

class BasePokemonCommand(object):
    URL = 'http://pokeapi.co/api/v2/pokemon/{}'
            
    OUTPUT_FORMAT = "\nName: {}\nMoves:\n{}"
            
    def get_pokemon(self, name=None):
        if name is None:
            name = self.request_input_data('pokemon_name')
        self.REQUEST_URL = self.URL.format(name)
        data = self.request_data()
        
        moves = ""
        for move in data['moves']:
            moves += move['move']['name'] + "\n"
            
        return self.OUTPUT_FORMAT.format(data['name'], moves)
        
class InputBasedPokemon(SimpleCommandLineParserMixin,
                        InputRequestMixin,
                        JSONDataRequestMixin,# Different mixin
                        StdoutOutputMixin,
                        BasePokemonCommand):
    def main(self):
        result = self.get_pokemon()
        self.write("Result: {}".format(result))

class CommandLinePokemon(SimpleCommandLineParserMixin,
                        ArgumentsRequestMixin,
                        JSONDataRequestMixin,# Different mixin
                        StdoutOutputMixin,
                        BasePokemonCommand):
    def main(self):
        self.parse_arguments()
        result = self.get_pokemon()
        self.write("Result: {}".format(result))

class RandomChooserPokemon(JSONDataRequestMixin,
                          StdoutOutputMixin,
                          BasePokemonCommand):
    N_POKEMON = 811
    
    def main(self):
        pokemon_id = random.choice(range(1,self.N_POKEMON))
        result = self.get_pokemon(name=pokemon_id)
        self.write("Result: {}".format(result))
        
        
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
