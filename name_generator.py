import random


class UnsupportedCharacter(Exception):
    pass


def transform_char(ch):
    if ch == 'X':
        return chr(ord('A') + random.randrange(26))
    elif ch == 'x':
        return chr(ord('a') + random.randrange(26))
    elif ch == '_':
        return ch
    else:
        raise UnsupportedCharacter(ch)


def generate_name(format):
    """ accepts strings of form [xX ]*"""

    result = ''
    for x in format:
        result += transform_char(x)

    return result

