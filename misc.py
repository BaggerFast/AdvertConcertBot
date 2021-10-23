import dataclasses
from abc import ABC
from typing import Union
from fuzzywuzzy import fuzz


@dataclasses.dataclass
class EventInfo:
    message: dict
    user_id: int
    command: str


class Settings(ABC):
    debug: bool = True
    words_coef: int = 75


class StateIndex(ABC):
    default: int = 0
    menu: int = 1
    authors: int = 2
    state_manager: int = 3


def words_compare(command: str, words: Union[list, tuple]) -> bool:
    for word in words:
        if fuzz.ratio(command, word) >= Settings.words_coef:
            return True
    return False

