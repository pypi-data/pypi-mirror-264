import random
import math
import os


def randint(low=0, high=100):
    return low + math.floor(random.random() * (high - low))


def repeat(times: int, callback: callable) -> None:
    for i in range(times):
        callback()


def fileAsArray(location: str) -> list:
    with open(location) as handler:
        return list(map(lambda x: x.strip(), handler.readlines()))


def oneOf(values: list) -> any:
    return values[randint(0, len(values))]


def root() -> str:
    return os.path.dirname(os.path.abspath(__file__)) + "/"


def isVowel(letter: str) -> bool:
    return letter[0] in "aoieu"


def randomVowel(otherThan=None) -> str:
    vowels = "aoieu"

    if bool(otherThan):
        vowels.replace(otherThan, "")

    return oneOf(list(vowels))
