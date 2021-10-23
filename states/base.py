from misc import EventInfo


class BaseState:
    def __init__(self, bot, request: EventInfo):
        self.bot = bot
        self.request = request

    def run(self) -> None:
        raise NotImplementedError
