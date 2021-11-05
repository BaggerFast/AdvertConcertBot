import os
import dataclasses
import traceback
from abc import ABC
from datetime import datetime
from typing import Union
from fuzzywuzzy import fuzz


@dataclasses.dataclass
class EventInfo:
    message: dict
    user_id: int
    command: str


class Settings(ABC):
    debug: bool = bool(int(os.environ.get('DEBUG', 0)))
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
        return os.path.join(*'home/vk_bot/'.split('/') + path.lower().replace('\\', '/').split('/'))


def convert_error(error):
    parts = ["Traceback (most recent call last):\n"]
    parts.extend(traceback.format_tb(error.__traceback__))
    parts.extend(f'{type(error).__name__}: {error}')
    return "".join(parts)


def write_log_file(bot, error) -> None:
    name = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    exception_path = get_path(f"exceptions")
    if not os.path.exists(exception_path):
        os.mkdir(exception_path)
    file_path = f"{exception_path}/{name}.txt"
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(convert_error(error))
    bot.send_log_to_admin(name, file_path)
