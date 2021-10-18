import vk_api
from vk_api.keyboard import VkKeyboard
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from database import Database
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
        self.db = Database()

    def run(self):
        print("Bot запущен...")
        event_data = {
            VkBotEventType.GROUP_JOIN: self.group_join_action,
            VkBotEventType.MESSAGE_NEW: self.new_msg_action,
        }
        for event in self.longpoll.listen():
            if event.type in event_data.keys():
                event_data[event.type](event)

    def group_join_action(self, event):
        keyboard = VkKeyboard(one_time=False)
        user_id = event.obj.user_id
        self.write_msg(user_id, "ГС\n"
                                'Чтобы узнать больше, напиши "Меню"', keyboard.get_empty_keyboard(), True)

    def new_msg_action(self, event):
        message = event.obj['message']
        user_id = message['peer_id']
        command = message['text'].strip().lower()

        if command in ("привет", "здарова", "добрый день", "хай", "здравствуйте", "ку", "здорово"):
            keyboard = self.cashed_kb.menu
            self.write_msg(user_id, "Команда SINTEZ приветствует тебя!\n"
                                    "В меню ты можешь найти самую важную информацию:", keyboard)
            self.stage = StageMenu
        elif command in ("menu", "меню", "назад"):
            keyboard = self.cashed_kb.menu
            self.write_msg(user_id, "Выберите пункт из меню:", keyboard)
            self.stage = StageMenu
        else:
            if not self.stage(self, event).action():
                self.write_msg(user_id, 'Ошибка ввода. Напишите "Меню"')

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

    def send_attachment(self, peer_id, attachment, message=''):
        methodinfo = {
            'peer_id': peer_id,
            'attachment': attachment,
            'random_id': get_random_id(),
            'message': message,
        }

        self.vk.method('messages.send', methodinfo)

