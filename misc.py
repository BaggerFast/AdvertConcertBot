import dataclasses
from fuzzywuzzy import fuzz


@dataclasses.dataclass
class EventInfo:
    message: dict
    user_id: int
    command: str


class Settings:
    debug = True
    words_coef = 75


class StateIndex:
    default = 0
    menu = 1
    authors = 2
    authors2 = 3


def words_compare(command, words):
    for word in words:
        if fuzz.ratio(command, word) >= Settings.words_coef:
            return True
    return False

