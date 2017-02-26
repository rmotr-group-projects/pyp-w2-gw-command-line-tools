import random
from requests.exceptions import HTTPError

from .mixins import (
    SimpleCommandLineParserMixin, ArgumentsRequestMixin, StdoutOutputMixin,
    InputRequestMixin, SimpleAuthenticationMixin,
    LoginMixin, JSONDataRequestMixin, PagedJSONDataMixin, CSVOutputMixin,
    PrintURLPageTitleToStdoutMixin, GoogleFeelingLuckyMixin, OpenURLInBrowser,
    RequestValidatorMixin, ValidationError)

__all__ = [
    'ArgumentCalculatorCommand', 'InputCalculatorCommand',
    'PriviledgedArgumentsExampleCommand', 'InputBasedPokemon',
    'CommandLinePokemon', 'RandomChooserPokemon', 'PokemonBerryPrinter',
    'PokemonBerryCSVWriter', 'StdoutArgsFeelingLucky', 'ValidatedInputCommand']


class ValidatedInputCommand(InputRequestMixin,
                            RequestValidatorMixin,
                            StdoutOutputMixin):

    def __init__(self, validator=None):
        self.validator = validator

    def main(self):
        self.request_input_data('data')
        try:
            result = self.validate(validator=self.validator)
        except ValidationError as e:
            result = str(e)
        self.write(result)


class BaseFeelingLucky(object):
    """
    Takes a search term and returns the Google I'm Feeling Lucky result
    """

    def feeling_lucky(self):
        search_term = self.request_input_data('search_term')
        url = self.request_data(search_term)
        self.open(url)


class StdoutArgsFeelingLucky(BaseFeelingLucky,
                             GoogleFeelingLuckyMixin,
                             ArgumentsRequestMixin,
                             SimpleCommandLineParserMixin,
                             PrintURLPageTitleToStdoutMixin):
    """ Prints resulting page's title and url to stdout """

    def main(self):
        self.parse_arguments()
        self.feeling_lucky()


class OpenInBrowserArgsFeelingLucky(BaseFeelingLucky,
                                    GoogleFeelingLuckyMixin,
                                    ArgumentsRequestMixin,
                                    SimpleCommandLineParserMixin,
                                    OpenURLInBrowser):
    """ Opens resulting url in web browser """

    def main(self):
        self.parse_arguments()
        self.feeling_lucky()


class BaseAllPokemonBerriesCommand(object):
    """
    Grabs entries for all berries from PokeAPI
    and then outputs them
    """
    REQUEST_URL = 'http://pokeapi.co/api/v2/berry/'

    def get_pokemon(self):
        return self.request_data()


class PokemonBerryPrinter(PagedJSONDataMixin,
                          StdoutOutputMixin,
                          BaseAllPokemonBerriesCommand):
    """ Prints to stdout """

    def main(self):
        results = self.get_pokemon()
        for berry in results:
            self.write(berry['name'])


class PokemonBerryCSVWriter(PagedJSONDataMixin,
                            CSVOutputMixin,
                            BaseAllPokemonBerriesCommand):
    FILE_PATH = 'pokemonberries.csv'
    """ Exports to CSV file """

    def main(self):
        results = self.get_pokemon()
        for berry in results:
            self.write(berry)


class BasePokemonCommand(object):
    """
    Retrieves info on a specific pokemon from PokeAPI
    Works for both pokemon name and id in the api
    ID/Name may be passed or will be requested

    Output as following:
    Name: Pokemon Name
    Moves:
    move 1
    move 2
    ...
    last move
    """

    URL = 'http://pokeapi.co/api/v2/pokemon/{}'

    OUTPUT_FORMAT = "\nName: {}\nMoves:\n{}"

    def get_pokemon(self, name=None):
        if name is None:
            name = self.request_input_data('pokemon_name')
        self._get_data(name)
        return self._format()

    def _get_data(self, id):
        self.REQUEST_URL = self.URL.format(id)
        self.data = self.request_data()

    def _format(self):
        if self.data:
            moves = ""
            for move in self.data['moves']:
                moves += move['move']['name'] + "\n"

            return self.OUTPUT_FORMAT.format(self.data['name'], moves)
        else:
            return ""


class InputBasedPokemon(SimpleCommandLineParserMixin,
                        InputRequestMixin,
                        JSONDataRequestMixin,
                        StdoutOutputMixin,
                        BasePokemonCommand):
    """ Retrieves pokemon based on user input """

    def main(self):
        result = self.get_pokemon()
        self.write("Result: {}".format(result))


class CommandLinePokemon(SimpleCommandLineParserMixin,
                         ArgumentsRequestMixin,
                         JSONDataRequestMixin,
                         StdoutOutputMixin,
                         BasePokemonCommand):
    """ Retrieves pokemon based on command line argument """

    def main(self):
        self.parse_arguments()
        result = self.get_pokemon()
        self.write("Result: {}".format(result))


class RandomChooserPokemon(JSONDataRequestMixin,
                           StdoutOutputMixin,
                           BasePokemonCommand):
    """
    Retrieves information of random pokemon
    N_POKEMON = Number of pokemon available from PokeAPI
    """
    N_POKEMON = 811

    def main(self):
        result = self._get_random_pokemon()
        self.write("Result: {}".format(result))

    def _get_random_pokemon(self, id=None):
        # for testing purposes
        if id is not None:
            pokemon_id = id
        else:
            pokemon_id = random.choice(range(1, self.N_POKEMON))
        try:
            result = self.get_pokemon(name=pokemon_id)
            return result
        # retrieved invalid random pokemon, retrieve another
        except HTTPError:
            return self._get_random_pokemon()


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
