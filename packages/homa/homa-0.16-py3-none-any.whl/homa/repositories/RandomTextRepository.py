import string
import random

from ..helpers import randint
from ..helpers import oneOf
from ..helpers import fileAsArray
from ..helpers import root
from ..helpers import replaceVowels


class RandomTextRepository:
    def __init__(self) -> None:
        self.titles = fileAsArray(
            root("wordlists/text/titles.txt")
        )
        random.shuffle(self.titles)

    def token(self, lowerBound: int = 4, upperBound: int = 14):
        letters = list(string.ascii_lowercase)
        random.shuffle(letters)
        return "".join(letters[:randint(lowerBound, upperBound)])

    def title(self):
        return replaceVowels(oneOf(self.titles))
