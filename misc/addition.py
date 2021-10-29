import os
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
    debug: bool = bool(os.environ.get('DEBUG', 0))
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


def get_path(path: str) -> str:
    ROOT_DIR: str = os.path.dirname(os.path.abspath('run.py'))
    if Settings.debug:
        return os.path.join(*[ROOT_DIR] + path.lower().replace('\\', '/').split('/'))
    else:
        return os.path.join(*'home/vk_bot/'.replace('\\', '/').split('/') + path.lower().replace('\\', '/').split('/'))
