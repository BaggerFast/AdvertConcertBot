from stages import Stage, StageAuthors


class StageMenu(Stage):

    def __init__(self, bot, event):
        super().__init__(bot, event)
        self.cashed_authors = self.get_authors()
        self.messages = {
            "концерт": self.concert,
            "артисты": self.authors,
            "закрыть": self.close,
        }

    def action(self) -> bool:
        if self.command in ("sintez", "синтез"):
            self.bot.send_msg(self.user_id, '"SINTEZ" - это музакальное объединение '
                                             "Владимирских исполнителей...")
        elif self.command in self.messages.keys():
            self.messages[self.command]()
        else:
            return False
        return True

    def concert(self):
        # ссылка на яндекс карты
        site = "https://yandex.ru/maps/192/vladimir/house/dvoryanskaya_ulitsa_27ak2/YEkYdQ9pTU0BQFtsfX1zd3RiZA==/?ll=40" \
               ".389486%2C56.126810&source=wizgeo&utm_medium=maps-desktop&utm_source=serp&z=17.08"
        text = "Концерт состоиться 14 ноября в 18:00 \n По адресу Дворянская улица, 27Ак2, Владимир"
        self.bot.send_msg(self.user_id, f"{site}\n{text}")

    def authors(self):
        self.bot.send_msg(self.user_id, f'{self.cashed_authors}\nВведите номер артиста:')
        self.bot.stage = StageAuthors

    def get_authors(self):
        artists = ''
        for number, name, other in self.bot.db.get_authors():
            artists += f'{number + 1}. {name}\n'
        return artists

    def close(self):
        self.bot.send_msg(self.user_id, 'Чтобы снова открыть меню, напишите "Меню"', self.bot.cashed_kb.empty, True)
