from vk_api.keyboard import VkKeyboard
from stages import Stage


class StageMenu(Stage):

    def __init__(self, bot, event):
        super().__init__(bot, event)
        self.messages = {
            "концерт": self.concert,
            "артисты": self.authors,
            "закрыть": self.close,
        }

    def action(self):
        if self.request in ("sintez", "синтез"):
            self.bot.write_msg(self.user_id, '"SINTEZ" - это музакальное объединение '
                                             "Владимирских исполнителей...")
        elif self.request in self.messages.keys():
            self.messages[self.request]()

    def concert(self):
        self.bot.write_msg(self.user_id, "http://surl.li/akzwe")
        self.bot.write_msg(self.user_id, "Концерт состоиться 14 ноября в 18:00 \n"
                                         "По адресу Дворянская улица, 27Ак2, Владимир")

    def authors(self):
        pass
        artistList = ''

        # for i in range(len(artist)):
        #     artistList += str(i + 1) + '. ' + artist[i][0] + '\n'
        # write_msg(user_id, artistList)
        # write_msg(user_id, "Введите номер артиста:")
        # floor = StageAuthors

    def close(self):
        keyboard = VkKeyboard(one_time=False)
        self.bot.write_msg(self.user_id, 'Чтобы снова открыть меню, напишите "Меню"',
                           keyboard.get_empty_keyboard(), True)