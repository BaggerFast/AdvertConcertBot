from states import BaseState
from misc import EventInfo, StateIndex, Keyboards, get_path


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
        text = "Концерт состоиться 14 ноября в 18:00\nПо адресу Дворянская улица, 27Ак2, Владимир " \
               "([public206661662|БАР ЦЕХ]) \nЗапуск людей в 17:00\nБИЛЕТЫ ВЛАДИМИР КОНЦЕРТ" \
               "\nP.S. При себе иметь маску"
        audio = self.bot.get_audio_massage(self.request, get_path('audio/concert.mp3'))
        self.bot.send_msg(self.request.user_id, msg=text, attachment=audio,
                          pos={'lat': 56.126930, "long": 40.389273})

    def __sintez(self):
        audio = self.bot.get_audio_massage(self.request, get_path('audio/sintez.mp3'))
        attach = ['photo-207855282_457239126', audio]
        self.bot.send_msg(self.request.user_id, msg='[public205043643|CООБЩЕСТВО SINTEZ]', attachment=attach)

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
