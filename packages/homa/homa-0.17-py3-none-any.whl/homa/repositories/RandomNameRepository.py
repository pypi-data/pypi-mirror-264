from random import shuffle

from ..helpers import fileAsArray
from ..helpers import oneOf
from ..helpers import root
from ..helpers import replaceVowels
from ..helpers import resource


class RandomNameRepository:
    def __init__(self) -> None:
        self.__masculine_firstnames = fileAsArray(resource("masculine_names"))
        self.__feminine_firstnames = fileAsArray(resource("feminine_names"))
        self.__surnames = fileAsArray(resource("surnames"))

        shuffle(self.__masculine_firstnames)
        shuffle(self.__feminine_firstnames)
        shuffle(self.__surnames)

        self.lastGender = None

    def gender(self, gender: str | None):
        genderMap = {
            "girl": "F",
            "girls": "F",
            "female": "F",
            "boy": "M",
            "male": "M"
        }
        self.lastGender = oneOf(
            ["F", "M"]) if not gender else genderMap[gender]

    def firstname(self) -> str:
        targetArrayMap = {
            "M": self.__masculine_firstnames,
            "F": self.__feminine_firstnames,
        }

        return oneOf(targetArrayMap[self.lastGenderOrRandom()])

    def surname(self) -> str:
        return replaceVowels(oneOf(self.__surnames))

    def prefix(self):
        targetArrayMap = {
            "M": ["Lord", "Sir", "Gentleman", "Dr."],
            "F": ["Madam", "Dr.", "Miss", "Ms."]
        }
        return oneOf(targetArrayMap[self.lastGenderOrRandom()])

    def lastGenderOrRandom(self):
        return self.lastGender if self.lastGender else oneOf(["M", "F"])

    def fullname(self, gender=None):
        self.gender(gender)

        usePrefix = oneOf([True, False])
        if usePrefix:
            return f"{self.prefix()} {self.firstname()} {self.surname()}"

        return f"{self.firstname()} {self.surname()}"
