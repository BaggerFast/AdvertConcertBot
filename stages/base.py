from misc import EventInfo


class Stage:
    def __init__(self, bot, event: EventInfo):
        self.bot = bot
        self.event = event

    def action(self) -> None:
        raise NotImplementedError
