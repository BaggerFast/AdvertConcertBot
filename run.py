import vk_api
from vk_api.keyboard import VkKeyboard
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from keyboards import Keyboards
from stages import StageMenu


class Bot:

    def __init__(self):
        token = "ff8d21d2ec05262976bb5df59d6d2ef18b71ae7419fda1ad53305cc4f4451d705daf646700927e978156a"
        group_id = 80176390

        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk, group_id)
        self.stage = StageMenu
        self.cashed_kb = Keyboards()

    def run(self):
        print("Bot запущен...")
        for event in self.longpoll.listen():
            # Если вступил в сообщество
            if event.type == VkBotEventType.GROUP_JOIN:
                keyboard = VkKeyboard(one_time=False)
                user_id = event.obj.user_id
                self.write_msg(user_id, "ГС\n"
                                        'Чтобы узнать больше, напиши "Меню"', keyboard.get_empty_keyboard(), True)

            # Если появилось новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.obj['message']
                user_id = message['peer_id']
                request = message['text'].lower()

                if request in ("привет", "здарова", "добрый день", "хай", "здравствуйте", "ку", "здорово"):
                    keyboard = self.cashed_kb.menu
                    self.write_msg(user_id, "Команда SINTEZ приветствует тебя!\n"
                                            "В меню ты можешь найти самую важную информацию:", keyboard)
                    self.stage = StageMenu

                elif request in ("menu", "меню", "назад"):
                    keyboard = self.cashed_kb.menu
                    self.write_msg(user_id, "Выберите пункт из меню:", keyboard)
                    self.stage = StageMenu

                else:
                    self.stage(self, event).action()
                    # self.write_msg(user_id, 'Для входа в меню напишите "Меню"')

    def write_msg(self, user_id, msg, keyboard=None, is_empty_msg=False) -> None:
        methodinfo = {
            'user_id': user_id,
            'message': msg,
            'random_id': get_random_id()
        }

        if is_empty_msg == True:
            methodinfo['keyboard'] = keyboard

        elif keyboard is not None:
            methodinfo['keyboard'] = keyboard.get_keyboard()

        else:
            methodinfo = methodinfo

        self.vk.method('messages.send', methodinfo)

        # Функция отправки фото

    def send_attachment(self, peer_id, attachment) -> None:
        methodinfo = {
            'peer_id': peer_id,
            'attachment': attachment,
            'random_id': get_random_id(),
            'message': ''
        }

        self.vk.method('messages.send', methodinfo)

        # Создание главного меню


def main():
    outOfList = False
    number = 0
    floor = StageMenu

    artist = [["BLEESWOOD", "photo-113648808_457242960", 'audio-2001711953_93711953', 'audio-2001071838_87071838',
               'audio-2001741800_91741800'],
              ["Паша Фан", "photo244947953_457274119", 'audio-2001701202_96701202', 'audio-2001695040_96695040',
               'audio-2001724521_94724521'],
              ["4Trip", "photo-169379061_457239525", 'audio-2001968073_90968073', 'audio-2001378959_63378959',
               'audio-2001318207_81318207'],
              ["гл666к", "photo354611290_457254089", 'audio-2001574279_59574279', 'audio-2001494144_88494144',
               'audio-2001169641_82169641'],
              ["МИЛФХАНТЕР", "photo-171338486_457239717", 'audio-2001696903_95696903', None, None],
              ["Evans", "photo-177016468_457239063", 'audio-2001254014_94254014', 'audio-2001254018_94254018',
               'audio-2001254015_94254015'],
              ["chupi-boy", "photo-195687269_457239161", 'audio-2001113886_94113886', 'audio-2001057697_95057697',
               'audio-2001045953_90045953'],
              ["Voskresensky", "photo236319600_457297270", 'audio2000477959_456243947', 'audio2000325901_456244044',
               'audio2000091028_456244989'],
              ]

    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
