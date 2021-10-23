from keyboards import Keyboards
from misc import EventInfo
from states import BaseState


class StateMenu(BaseState):
    def __init__(self, bot, event: EventInfo):
        super().__init__(bot, event)
        self.cashed_authors = self.get_authors()
        self.messages = {
            "sintez": self.sintez,
            "концерт": self.concert,
            "артисты": self.authors,
            "закрыть": self.close,
        }

    def run(self) -> bool:
        if self.request.command in self.messages.keys():
            self.messages[self.request.command]()
        else:
            return False
        return True

    def concert(self):
        # ссылка на яндекс карты
        site = "https://yandex.ru/maps/192/vladimir/house/dvoryanskaya_ulitsa_27ak2/YEkYdQ9pTU0BQFtsfX1zd3RiZA==/?ll=40" \
               ".389486%2C56.126810&source=wizgeo&utm_medium=maps-desktop&utm_source=serp&z=17.08"
        text = "Концерт состоиться 14 ноября в 18:00 \n По адресу Дворянская улица, 27Ак2, Владимир"
        self.bot.send_msg(self.request.user_id, f"{site}\n{text}")

    def sintez(self):
        self.bot.send_msg(self.request.user_id, '"SINTEZ" - это музакальное объединение '
                                              "Владимирских исполнителей...")

    def authors(self):
        self.bot.send_msg(self.request.user_id, f'{self.cashed_authors}\nВведите номер артиста:', keyboard=Keyboards.back)
        self.bot.change_state(self.request.user_id, 2)

    def get_authors(self):
        artists_text = ''
        for i, artist in enumerate(self.bot.db.get_authors()):
            artists_text += f'{i + 1}. {artist.name}\n'
        return artists_text

    def close(self):
        self.bot.send_msg(self.request.user_id, 'Чтобы снова открыть меню, напишите "Меню"', Keyboards.empty,
                          True)
