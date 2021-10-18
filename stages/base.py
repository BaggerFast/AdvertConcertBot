class Stage:

    def __init__(self, bot, event):
        self.bot = bot
        self.message = event.obj['message']
        self.user_id = self.message['peer_id']
        self.request = self.message['text'].lower()

    def action(self):
        pass
