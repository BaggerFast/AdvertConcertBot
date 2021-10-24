from abc import ABC
from misc import Database, EventInfo


class BaseState(ABC):
    def __init__(self, bot, request: EventInfo):
        self.bot = bot
        self.request: EventInfo = request
        self.db: Database = self.bot.db

    def run(self) -> None:
        raise NotImplementedError
