from misc import EventInfo, StateIndex, Keyboards, get_path
from states import BaseState


class StateMenu(BaseState):
    def __init__(self, bot, event: EventInfo):
        super().__init__(bot, event)
        self.__cashed_authors = self.__get_authors()
        self.__messages = {
            "sintez": self.__sintez,
            "концерт": self.__concert,
            "артисты": self.__authors,
            "закрыть": self.__close,
        }

    def run(self) -> bool:
        if self.request.command in self.__messages.keys():
            self.__messages[self.request.command]()
        else:
            return False
        return True

    def __concert(self):
        # ссылка на яндекс карты
        site = "https://yandex.ru/maps/192/vladimir/house/dvoryanskaya_ulitsa_27ak2/YEkYdQ9pTU0BQFtsfX1zd3RiZA==/?ll=40" \
               ".389486%2C56.126810&source=wizgeo&utm_medium=maps-desktop&utm_source=serp&z=17.08"
        text = "Концерт состоиться 14 ноября в 18:00\nПо адресу Дворянская улица, 27Ак2, Владимир"
        audio = self.bot.get_audio_massage(self.request, get_path('audio/concert.mp3'))
        self.bot.send_msg(self.request.user_id, attachment=audio)
        self.bot.send_msg(self.request.user_id, f"{site}\n{text}")

    def __sintez(self):
        audio = self.bot.get_audio_massage(self.request, get_path('audio/sintez.mp3'))
        self.bot.send_msg(self.request.user_id, attachment=audio)

    def __authors(self):
        self.bot.send_msg(self.request.user_id, f'{self.__cashed_authors}\nВведите номер артиста:', Keyboards.back)
        self.db.set_user_state(self.request.user_id, StateIndex.authors)

    def __get_authors(self):
        artists_text = ''
        for i, artist in enumerate(self.db.get_authors):
            artists_text += f'{i + 1}. {artist.name}\n'
        return artists_text

    def __close(self):
        self.bot.send_msg(self.request.user_id, 'Чтобы снова открыть меню, напишите "Меню"', Keyboards.empty)
        self.db.set_user_state(self.request.user_id, StateIndex.menu)
