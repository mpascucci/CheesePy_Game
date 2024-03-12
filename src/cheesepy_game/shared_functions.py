from typing import List
import random
import string


def random_name(length: int) -> str:
    alphabet = set(string.ascii_lowercase)
    vowels = {'a', 'e', 'i', 'o', 'u'}
    consonants = alphabet - vowels

    vowels = list(vowels)
    consonants = list(consonants)

    s = ""

    for i in range(length):
        if i % 2 == 0:
            s += random.choice(consonants)
        else:
            s += random.choice(vowels)

    return s.capitalize()


def shuffle_and_return(l: List):
    """shuffle list and return it"""
    random.shuffle(l)
    return l


if __name__ == "__main__":
    print(random_name(8))
