import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


def main():
    token = "ff8d21d2ec05262976bb5df59d6d2ef18b71ae7419fda1ad53305cc4f4451d705daf646700927e978156a"
    group_id = 80176390

    vk = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk, group_id)

    outOfList = False
    number = 0
    floor = 2

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

    # Функция отправки сообщения с keyboard
    def write_msg(user_id, msg, keyboard=None, is_empty_msg=False) -> None:
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

        vk.method('messages.send', methodinfo)

    # Функция отправки фото
    def send_attachment(peer_id, attachment) -> None:
        methodinfo = {
            'peer_id': peer_id,
            'attachment': attachment,
            'random_id': get_random_id(),
            'message': ' '
        }

        vk.method('messages.send', methodinfo)

    # Создание главного меню
    def create_keyboard_menu() -> VkKeyboard:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("SINTEZ", VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button("Концерт", VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button("Артисты", VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button("Закрыть", VkKeyboardColor.NEGATIVE)

        return keyboard

    # Создание отдельного меню с кнопкой назад
    # def create_keyboard_back():
    #     keyboard = VkKeyboard(one_time=False)
    #     keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
    #     write_msg(user_id, "Чтобы вернуться назад нажмите Назад", keyboard)
    #
    #     return keyboard

    # Создание меню переключения артистов
    def create_keyboard_artist() -> VkKeyboard:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Предыдущий", VkKeyboardColor.PRIMARY)
        keyboard.add_button("Следующий", VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
        write_msg(user_id, 'Чтобы вернуться назад нажмите "Назад"', keyboard)

        return keyboard

    # Основной код
    for event in longpoll.listen():

        # Если вступил в сообщество
        if event.type == VkBotEventType.GROUP_JOIN:
            keyboard = VkKeyboard(one_time=False)
            user_id = event.obj.user_id
            write_msg(user_id, "ГС\n"
                               'Чтобы узнать больше, напиши "Меню"', keyboard.get_empty_keyboard(), True)

        # Если появилось новое сообщение
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj['message']
            user_id = message['peer_id']
            request = message['text'].lower()

            if request in ("привет", "здарова", "добрый день", "хай", "здравствуйте", "ку", "здорово"):
                keyboard = create_keyboard_menu()
                write_msg(user_id, "Команда SINTEZ приветствует тебя!\n"
                                   "В меню ты можешь найти самую важную информацию:", keyboard)
                floor = 2

            elif request in ("menu", "меню", "назад"):
                keyboard = create_keyboard_menu()
                write_msg(user_id, "Выберите пункт из меню:", keyboard)
                floor = 2

            if floor == 2:
                if request in ("sintez", "синтез"):
                    write_msg(user_id, '"SINTEZ" - это музакальное объединение '
                                       "Владимирских исполнителей...")

                elif request == "концерт":
                    write_msg(user_id, "http://surl.li/akzwe")
                    write_msg(user_id, "Концерт состоиться 14 ноября в 18:00 \n"
                                       "По адресу Дворянская улица, 27Ак2, Владимир")

                elif request == "артисты":
                    artistList = ''
                    for i in range(len(artist)):
                        artistList += str(i + 1) + '. ' + artist[i][0] + '\n'
                    write_msg(user_id, artistList)
                    write_msg(user_id, "Введите номер артиста:")
                    floor = 3

                elif request == 'закрыть':
                    keyboard = VkKeyboard(one_time=False)
                    write_msg(user_id, 'Чтобы снова открыть меню, напишите "Меню"', keyboard.get_empty_keyboard(), True)

            elif floor == 3:
                if request == 'предыдущий':
                    if number - 1 == 0:
                        write_msg(user_id, "Это первый в списке артист")
                        outOfList = True
                    else:
                        number -= 1

                elif request == 'следующий':
                    if number + 1 > len(artist):
                        write_msg(user_id, "Это последний в списке артист")
                        outOfList = True
                    else:
                        number += 1

                if request.isdigit() or request in ('следующий', 'предыдущий'):
                    if request.isdigit():
                        number = int(request)

                    if outOfList:
                        outOfList = False

                    elif number <= len(artist):
                        artistLabel = str(number) + '. ' + artist[number - 1][0]
                        write_msg(user_id, artistLabel)
                        send_attachment(user_id, artist[number - 1][1])
                        for i in range(2, 5):
                            if artist[number - 1][i] is not None:
                                send_attachment(user_id, artist[number - 1][i])
                        keyboard = create_keyboard_artist()

                    else:
                        write_msg(user_id, "Артиста с таким номером не существует")
                else:
                    write_msg(user_id, 'Ошибка ввода. Напишите "Меню"')

            else:
                write_msg(user_id, 'Для входа в меню напишите "Меню"')


if __name__ == "__main__":
    main()