import vk_api

from states import BaseState
from misc import EventInfo


class AdminCommands(BaseState):
    def __init__(self, bot, event: EventInfo):
        super().__init__(bot, event)
        self.__messages = {
            "r1": self.remind,
        }

    def remind(self) -> None:
        all_members = self.bot.vk.method('groups.getMembers', {'group_id': self.bot.group_id})['items']
        text = """What’s up! 👋
Ты слышал про самый громкий концерт этого года? Вытаскивай свои наушники и послушай нас в лайве)

Наш концерт - это обилие стилей и жанров, которые подарят тебе незабываемые эмоции! 🔥
Но главная задача, это классно провести время.
Справишься?
Тогда мы тебя ждем!

Пссс
Билеты уже доступны здесь:
https://www.vladimirkoncert.ru/
Или приобретай их на прямую у организатора!"""

        for user_id in all_members:
            try:
                self.bot.send_msg(user_id=user_id, msg=text)
            except vk_api.exceptions.ApiError:
                continue

    def run(self) -> bool:
        all_members = self.bot.vk.method('groups.getMembers', {'group_id': self.bot.group_id, 'filter': 'managers'})
        admins = [data['id'] for data in all_members['items'] if data['role'] in ('administrator', 'creator')]
        if self.request.user_id in admins and self.request.command in self.__messages.keys():
            self.__messages[self.request.command]()
        else:
            return False
        return True
