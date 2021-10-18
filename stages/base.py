class Stage:
    def __init__(self, bot, event):
        self.bot = bot
        self.message = event.obj['message']
        self.user_id = self.message['peer_id']
        self.command = self.message['text'].strip().lower()

    def action(self) -> None:
        pass
