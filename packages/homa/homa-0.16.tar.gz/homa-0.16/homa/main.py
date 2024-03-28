import string

from .repositories.RandomNameRepository import RandomNameRepository
from .repositories.RandomTextRepository import RandomTextRepository
from .repositories.RandomDateRepository import RandomDateRepository
from .repositories.RandomImageRepository import RandomImageRepository


class Homa:
    def __init__(self) -> None:
        self.repositories = {
            "name": RandomNameRepository(),
            "date": RandomDateRepository(),
            "text": RandomTextRepository(),
            "image": RandomImageRepository()
        }

    def __getattr__(self, name: string):
        if name in self.repositories.keys():
            return self.repositories[name]

        for repository in self.repositories.values():
            if hasattr(repository, name):
                return getattr(repository, name)

        raise Exception("No method found")


def homa():
    return Homa()


def fake():
    return homa()
