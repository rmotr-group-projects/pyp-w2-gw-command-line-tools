import sys
import os
import csv
import unittest
import pytest
from mock import patch

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
    
def pokemon_input_mock(message):
    if 'pokemon_name' in message:
        return 'bulbasaur'

def test_pokemon_with_user_input(capsys):
    with patch('six.moves.input', pokemon_input_mock) as m:
        InputBasedPokemon().main()
        
    out, err = capsys.readouterr()
    assert out.startswith("Result: \nName: bulbasaur\nMoves:\nrazor-wind")
    
def test_pokemon_with_arguments(capsys):
    testargs = ["pokemon_name=bulbasaur"]
    with patch.object(sys, 'argv', testargs):
        CommandLinePokemon().main()

    out, err = capsys.readouterr()
    assert out.startswith('Result: \nName: bulbasaur\nMoves:\nrazor-wind')
    
def test_random_chooser_pokemon(capsys):
    RandomChooserPokemon().main()
        
    out, err = capsys.readouterr()
    assert out.startswith("Result: \nName:")

class RandomPokemonTester(unittest.TestCase):
    def test_random_chooser_pokemon_with_bad_random(self):
        #Test using known bad random value
        rp = RandomChooserPokemon()
        pokemon = rp._get_random_pokemon(id=752)
        #print(pokemon)
        assert pokemon.startswith("\nName:")


def test_pokemon_printer(capsys):
    PokemonBerryPrinter().main()
        
    out, err = capsys.readouterr()
    assert 'cheri' in out
    
    
def test_berry_csv_writer(capsys):
    PokemonBerryCSVWriter().main()
    
    with open('pokemonberries.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        assert 'cheri' in [row['name'] for row in reader]
        
    os.remove('pokemonberries.csv')