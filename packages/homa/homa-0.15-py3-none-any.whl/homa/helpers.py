import random
import math
import re
import os


def replaceVowels(raw: str) -> str:
    """
    The function `replaceVowels` takes a string input and replaces all vowels with random vowels.
    
    :param raw: The `replaceVowels` function takes a string `raw` as input and replaces all vowels (a,
    o, i, e, u) in the string with a random vowel using the `randomVowel` function
    :type raw: str
    :return: The `replaceVowels` function is returning a modified version of the input string `raw`
    where all vowels (a, o, i, e, u) have been replaced with random vowels.
    """
    return re.sub(
        "[aoieu]",
        lambda vowel: randomVowel(vowel),
        raw
    )


def randint(low=0, high=100):
    """
    The function `randint` generates a random integer within a specified range.

    :param low: The `low` parameter in the `randint` function represents the lower bound of the range
    from which a random integer will be generated. By default, it is set to 0 if no value is provided
    when calling the function, defaults to 0 (optional)
    :param high: The `high` parameter in the `randint` function represents the upper bound of the range
    from which a random integer will be generated. By default, if no value is provided for `high`, it is
    set to 100. This means that if you call `randint()` without specifying a, defaults to 100 (optional)
    :return: The function `randint` is returning a random integer within the range specified by the
    `low` and `high` parameters. The integer is generated using the `random.random()` function to get a
    random float between 0 and 1, which is then scaled and shifted to fit within the specified range.
    """
    return low + math.floor(random.random() * (high - low))


def repeat(times: int, callback: callable) -> None:
    """
    The `repeat` function takes an integer `times` and a callback function `callback`, and executes the
    callback function `times` number of times.

    :param times: The `times` parameter specifies the number of times the `callback` function should be
    executed in the `repeat` function
    :type times: int
    :param callback: The `callback` parameter in the `repeat` function is a callable object, which means
    it can be a function, method, or any other callable object that can be called using parentheses
    `()`. When you pass a callback function to the `repeat` function, it will be executed `times`
    :type callback: callable
    """
    for i in range(times):
        callback()


def fileAsArray(location: str) -> list:
    """
    The function `fileAsArray` reads a file at a specified location and returns its contents as a list
    of strings with leading and trailing whitespaces removed.

    :param location: The `location` parameter in the `fileAsArray` function is a string that represents
    the file path of the file you want to read and convert into a list
    :type location: str
    :return: The function `fileAsArray` reads a file located at the specified `location`, strips any
    leading or trailing whitespace from each line, and returns the contents of the file as a list of
    strings.
    """
    with open(location) as handler:
        return list(map(lambda x: x.strip(), handler.readlines()))


def oneOf(values: list) -> any:
    """
    The function `oneOf` takes a list of values and returns a random element from the list.

    :param values: The `values` parameter is a list of elements from which the `oneOf` function will
    randomly select and return one element
    :type values: list
    :return: The `oneOf` function is returning a random element from the `values` list.
    """
    return values[randint(0, len(values))]


def root(path="") -> str:
    """
    The `root` function returns the absolute path of the directory containing the current script file,
    with an optional additional path appended to it.

    :param path: The `path` parameter in the `root` function is a string that represents the relative
    path from the current file's directory to another directory or file. It is used to construct the
    full absolute path by appending it to the directory of the current file
    :return: The function `root(path)` returns the absolute path of the directory containing the current
    Python script file (__file__) concatenated with the provided `path` argument.
    """
    return os.path.dirname(os.path.abspath(__file__)) + "/" + path


def isVowel(letter: str) -> bool:
    """
    This Python function checks if a given letter is a vowel.

    :param letter: The `isVowel` function takes a single parameter `letter` of type `str`, which
    represents a letter of the alphabet. The function checks if the first character of the input
    `letter` is a vowel (either 'a', 'o', 'i', 'e', or 'u
    :type letter: str
    :return: The function `isVowel` is returning a boolean value indicating whether the input `letter`
    is a vowel or not.
    """
    return letter[0] in "aoieu"


def randomVowel(otherThan=None) -> str:
    """
    This Python function returns a random vowel, excluding a specified vowel if provided.

    :param otherThan: The `randomVowel` function generates a random vowel, with an optional parameter
    `otherThan` which specifies a vowel that should not be included in the random selection
    :return: a random vowel from the string "aoieu", excluding the vowel specified in the `otherThan`
    parameter if provided.
    """
    vowels = "aoieu"
    otherThan = str(otherThan)

    if bool(otherThan):
        vowels.replace(otherThan, "")

    return oneOf(list(vowels))
