import dataclasses
import os
from abc import ABC
from typing import Union
from fuzzywuzzy import fuzz


@dataclasses.dataclass
class EventInfo:
    message: dict
    user_id: int
    command: str


class Settings(ABC):
    debug: bool = False
    words_coef: int = 75
    token: str = str(os.environ.get('VK_TOKEN', 'define me!'))
    group_id: int = int(os.environ.get('VK_ID', 'define me!'))


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


ROOT_DIR = os.path.dirname(os.path.abspath('run.py'))


def get_path(path: str) -> str:
    print(os.path.abspath('run.py'))
    return os.path.join(*[ROOT_DIR] + path.lower().replace('\\', '/').split('/'))
