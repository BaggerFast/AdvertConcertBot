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

    def __concert(self) -> None:
        text = """Концерт «VOL ONE» 14.11.21
        
Запуск 17:00 Начало 18:00
[public206661662|Концертный бар ЦЕХ]
Адрес: Дворянская улица 27А к2

Цена: 250р
Билеты можно купить здесь:
https://vladimirkoncert.ru/shows/1172-KONTSERT-VOL-ONE

P.S. При себе иметь маску"""

        audio = self.bot.get_audio_massage(self.request, get_path('audio/concert.mp3'))
        self.bot.send_msg(self.request.user_id, attachment=audio)
        self.bot.send_msg(self.request.user_id, msg=text, pos={'lat': 56.126930, "long": 40.389273})

    def __sintez(self) -> None:
        audio = self.bot.get_audio_massage(self.request, get_path('audio/sintez.mp3'))
        text = """Привет, мы [public205043643|SINTEZ]!

Объединение людей с разнообразным стилем и жанром.
Все мы любим свое дело и имеем одну цель - создать что-то по-настоящему новое и уникальное.

Но мы бы не были нами, если бы не ваша поддержка! 
Мы будем продолжать радовать вас новыми релизами и мероприятиями, а вам лишь остается следить за нами)"""

        attach = ['photo-207855282_457239229', audio]
        self.bot.send_msg(self.request.user_id, msg=text, attachment=attach)

    def __authors(self) -> None:
        self.bot.send_msg(self.request.user_id, f'{self.__cashed_authors}\nВведите номер артиста:', Keyboards.back)
        self.db.set_user_state(self.request.user_id, StateIndex.authors)

    def __get_authors(self) -> str:
        artists_text = ''
        for i, artist in enumerate(self.db.get_authors):
            artists_text += f'{i + 1}. {artist.name}\n'
        return artists_text

    def __close(self):
        self.bot.send_msg(self.request.user_id, 'Чтобы снова открыть меню, напишите "Меню"', Keyboards.empty)
        self.db.set_user_state(self.request.user_id, StateIndex.menu)
