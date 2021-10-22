from misc import EventInfo
from stages import Stage


class StageMenu(Stage):

    def __init__(self, bot, event: EventInfo):
        super().__init__(bot, event)
        self.cashed_authors = self.get_authors()
        self.messages = {
            "концерт": self.concert,
            "артисты": self.authors,
            "закрыть": self.close,
        }

    def action(self) -> bool:
        if self.event.command in ("sintez", "синтез"):
            self.bot.send_msg(self.event.user_id, '"SINTEZ" - это музакальное объединение '
                                                  "Владимирских исполнителей...")
        elif self.event.command.isdigit():
            self.bot.stage = self.bot.Stage.authors(self.bot, self.event)
            self.bot.stage.action()
        elif self.event.command in self.messages.keys():
            self.messages[self.event.command]()
        else:
            return False
        return True

    def concert(self):
        # ссылка на яндекс карты
        site = "https://yandex.ru/maps/192/vladimir/house/dvoryanskaya_ulitsa_27ak2/YEkYdQ9pTU0BQFtsfX1zd3RiZA==/?ll=40" \
               ".389486%2C56.126810&source=wizgeo&utm_medium=maps-desktop&utm_source=serp&z=17.08"
        text = "Концерт состоиться 14 ноября в 18:00 \n По адресу Дворянская улица, 27Ак2, Владимир"
        self.bot.send_msg(self.event.user_id, f"{site}\n{text}")

    def authors(self):
        self.bot.send_msg(self.event.user_id, f'{self.cashed_authors}\nВведите номер артиста:')

    def get_authors(self):
        artists_text = ''
        for i, artist in enumerate(self.bot.db.get_authors()):
            artists_text += f'{i + 1}. {artist.name}\n'
        return artists_text

    def close(self):
        self.bot.send_msg(self.event.user_id, 'Чтобы снова открыть меню, напишите "Меню"', self.bot.cashed_kb.empty,
                          True)
