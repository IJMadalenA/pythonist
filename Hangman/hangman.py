import ast  # Abstract Syntax Trees - https://docs.python.org/3.8/library/ast.html
import random
import os
import sys
import unicodedata
import re


def clear():
    os.system('clear')


TITLE = """
███████╗██╗           █████╗ ██╗  ██╗ █████╗ ██████═╗ █████══╗ █████╗ ██████═╗  █████╗ 
██╔════╝██║          ██╔══██╗██║  ██║██╔══██║██╔══██║██╔═══██╝██╔══██╗██╔══██╚╗██╔══██║
███████╗██║          ███████║███████║██║  ██║███████╝██║      ███████║██║   ██║██║  ██║
██╔════╝██║          ██╔══██║██╔══██║██║  ██║██╔═██╚╗██║   ██╗██╔══██║██║  ██╔╝██║  ██║ 
███████╗███████╗     ██║  ██║██║  ██║╚█████╔╝██║  ██║ ██████╔╝██║  ██║██████╔╝ ╚█████╔╝
╚══════╝╚══════╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝   ╚════╝
"""

HANGMAN_PICS = [
    '''
    +---+
    |   |
        |
        |
        |
        |
=========
''', '''  
    +---+
    |   |
    O   |
        |
        |
        |
==========
''', '''
    +---+
    |   |
    O   |
    |   |
        |
        |
==========
''', '''  
    +---+
    |   |
    O   |
   /|   |
        |
        |
==========
''', '''  
    +---+
    |   |
    O   |
   /|\  |
        |
        |
==========
''', '''  
    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
==========
''', '''  
    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
==========
'''
]

help_message = f"""
"El Ahorcado Game"
Link al proyecto: https://github.com/santigo171/python-hangman
Comandos:
"ahorcado --play": Comienza a jugar.
"ahorcado --rules": Reglas del juego.
"ahorcado --words": Lista de palabras.
"ahorcado --añadir": Añade una palabra a la lista.
"ahorcado --eliminar": Elimina una palabra de la lista.
"""

alphabet = {
    'a': '▄▀█\n'
         '█▄█\n'
         '█ █',

    'b': '█▀▄\n'
         '█▀█\n'
         '█▄█',

    'c': '▄▀▀\n'
         '█░░\n'
         '▀▄▄',

    'd': '█▀▄\n'
         '█░█\n'
         '█▄▀',

    'e': '█▀▀\n'
         '█▀▀\n'
         '█▄▄',

    'f': '█▀▀\n'
         '█▀░\n'
         '█░░',

    'g': '█▀▀\n'
         '█░█\n'
         '█▄█',

    'h': '█░█\n'
         '█▄█\n'
         '█░█',

    'i': '▀█▀\n'
         '░█░\n'
         '▄█▄',

    'j': '░░█\n'
         '░░█\n'
         '█▄█',

    'k': '█░█\n'
         '██░'
         '█░█',

    'l': '█░░\n'
         '█░░'
         '█▄▄',

    'm': '╔╗╗\n'
         '║║║'
         '║║║',

    'n': '█▀█\n'
         '█░█\n'
         '█░█',

    'o': '█▀█\n'
         '█░█\n'
         '█▄█',

    'p': '█▀█\n'
         '█▀▀\n'
         '█░░',

    'q': '█▀█\n'
         '▀▀█\n'
         '░░█',

    'r': '█▀█\n'
         '█▀▄\n'
         '█░█',

    's': '█▀▄\n'
         '▀▄░\n'
         '▀▄█',

    't': '▀█▀\n'
         '░█░\n'
         '░█░',

    'u': '█░█\n'
         '█░█\n'
         '█▄█',

    'v': '▄ ▄\nº'
         '█░█\n'
         '▀▄▀',

    'w': '║║║\n'
         '║║║\n'
         '╚╝╝',

    'x': '█░█\n'
         '░█░'
         '█░█',

    'y': '█▄█\n'
         '░█░\n'
         '░█░',

    'z': '▀▀█\n'
         '░█░'
         '█▄▄'
}

settings_file = 'settings_file.txt'

es_words_easy = ['ganar', 'golpear', 'espeso', 'esposo', 'ancho', 'babear', 'imaginar', 'seco', 'calcio', 'bomba', ]
es_words_medium = ['caramelos', 'lavanderia', 'prisionera', 'reconocer', 'abrazadera', 'zodiaco', 'remolacha']
es_words_hard = ['velociraptor', 'indiferentemente', 'desaparecido', 'desesperacion', 'auriculares', 'eliminacion']

en_words_easy = ['crude', 'lawn', 'lamp', 'tooth', 'redeem', 'defend', 'program', 'weapon', 'respect', 'python']
en_words_medium = ['horizon', 'antiquity', 'chicken', 'favorable', 'architect', 'convince', 'execution', 'expectation']
en_words_hard = ['broadcaster', 'successfully', 'embarrassment', 'superintendent', 'unaccountable']


# This function validate the data entered and normalize it.
def normalize(letter):
    assert isinstance(letter, str), 'The parameter most be a str.'

    if letter.isalpha():
        letter = letter.lower()

        if letter in ('á', 'é', 'í', 'ó', 'ú'):
            replacements = (
                ("á", "a"),
                ("é", "e"),
                ("í", "i"),
                ("ó", "o"),
                ("ú", "u"),
            )
            for a, b in replacements:
                letter = letter.replace(a, b)

        return letter

    else:
        return TypeError


def read_file():
    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'w', encoding='utf-8') as file:
                data = file.read()
                res = ast.literal_eval(data)
            return res

        else:
            new_file = {
                'user_info': {'language': 'es'},
                'word_list': {'es_words': {'easy': es_words_easy, 'medium': es_words_medium, 'hard': es_words_hard}}
            }
            file = open('settings.txt', "w")
            file.write(str(new_file))
            file.close()

    except (TypeError, NameError, SyntaxError, FileNotFoundError):
        print(
            f"'Error: ' Can't find the file named 'settings.txt'.")
        quit()


def modify_file(value, path1, path2):
    new_file = read_file()  # dictionary
    new_file[path1][path2] = value
    with open(settings_file, 'w', encoding='utf8') as file:
        file.write(str(new_file))


def restore_file():
    new_file = {'user_info': {'language': 'es'}, 'word_list': {'es_words': es_words, 'en_words': en_words}}
    file = open('settings.txt', "w")
    file.write(str(new_file))
    file.close()


def get_config(message, error_message, option1, option2, path):
    option1 = option1.lower()
    option2 = option2.lower()

    setting = input(message).lower()


def get_word(language, difficulty):
    language = language.lower()
    difficulty = difficulty.lower()

    file = read_file()
    words = file['word_list'][language][difficulty]
    i = random.randint(0, len(words) - 1)


def play():
    file = read_file()
    language = file['user_info']['language']
    difficulty = file['user_info']['difficulty']
    word = get_word(language)

    true_letters = [{'hit': True, 'letter': char} for char in word]
    hit_letters = [{'hit': False, 'letter': char} for char in word]
    user_input_list = []
    hangman_state = 0
    won = False
    error = ''

    updateScreen(hangman_state, word, hit_letters, language, error)

    while hangman_state < 6 or won == True:
        updateScreen(hangman_state, word, hit_letters, language, error)
        forbidden_character = False
        already_guessed = False
        user_input = input('Guess: ')
        user_input = user_input.lower()

        if not user_input.isalpha():
            break

        normalized_input = normalize(user_input)

        # VERIFICAR LETRAS INGRESADAS REPETIDAS.
        for letter in user_input_list:
            if letter == normalized_input:
                already_guessed = True

        if len(user_input) > 1:
            error = ''


# Field management.
def _load_words(self):
    """Loads the words from a text file."""
    base_dir = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(base_dir, 'data.txt'), 'r', encoding='UTF-8') as file:
        for line in file:
            normalized_word = line.strip().upper()
            self.words.append(normalized_word)

    assert len(self.words) > 0, 'There are not words in the data file'


game_settings = 'game_settings'


def run():
    pass


if __name__ == '__main__':
    run()
