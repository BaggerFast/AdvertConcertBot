from abc import ABC
from database import Database
from misc import EventInfo


class BaseState(ABC):
    def __init__(self, bot, request: EventInfo):
        self.bot = bot
        self.request: EventInfo = request
        self.db: Database = self.bot.db

    def run(self) -> None:
        raise NotImplementedError
