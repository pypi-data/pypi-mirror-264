import string
import random

from .helpers import randint
from .helpers import repeat
from .helpers import root

from .repositories.NameRepository import NameRepository


class Homa:
    letters = list(string.ascii_lowercase)

    @staticmethod
    def shuffle(times: int = 10) -> None:
        repeat(times, lambda: random.shuffle(Homa.letters))

    @staticmethod
    def word(lowerBound: int = 4, higherBound: int = 14) -> str:
        Homa.shuffle()
        size = randint(lowerBound, higherBound)
        return "".join(Homa.letters[:size])

    @staticmethod
    def words(count: int = 10, lowerBound: int = 4, higherBound: int = 14) -> list:
        return [Homa.word(lowerBound, higherBound) for _ in range(count)]

    @staticmethod
    def text(wordCount: int = 10, lowerBound: int = 4, higherBound: int = 14) -> str:
        return " ".join(Homa.words(wordCount, lowerBound, higherBound))

    @staticmethod
    def name():
        nameRepository = NameRepository()
        return nameRepository.name()
