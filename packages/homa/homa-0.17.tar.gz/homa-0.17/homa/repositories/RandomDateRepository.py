from ..helpers import randint
import datetime


class RandomDateRepository:
    def __init__(self):
        self.generatedYear = None
        self.generatedMonth = None
        self.generatedDay = None
        self.dayCounts = {
            1: 31,  # January
            2: 28,  # February
            3: 31,  # March
            4: 30,  # April
            5: 31,  # May
            6: 30,  # June
            7: 31,  # July
            8: 31,  # August
            9: 30,  # September
            10: 31,  # October
            11: 30,  # November
            12: 31  # December
        }

    def year(self, start: int = 2000, end: int = 2020) -> int:
        self.generatedYear = randint(start, end + 1)
        self.isLeap = self.generatedYear % 4 == 0

        if self.isLeap:
            self.dayCounts[2] = 29
        else:
            self.dayCounts[2] = 28

        return self.generatedYear

    def month(self) -> int:
        self.generatedMonth = randint(1, 12 + 1)
        return self.generatedMonth

    def day(self) -> int:
        self.generatedDay = randint(1, self.dayCounts[self.generatedMonth])
        return self.generatedDay

    def date(self, asString=False, separator="/"):
        if asString:
            return f"{self.year()}{separator}{self.month()}{separator}{self.day()}"

        return datetime.datetime(
            self.year(),
            self.month(),
            self.day()
        )

    def datetime(self):
        return datetime.datetime(
            self.year(),
            self.month(),
            self.day(),
            randint(0, 23 + 1),
            randint(0, 60),
            randint(0, 60),
        )
