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
        self.send_msg(event.obj.user_id, 'ГС\nЧтобы узнать больше, напиши "Меню"', self.cashed_kb.empty)

    def new_msg_action(self, event):
        message = event.obj['message']
        user_id = message['peer_id']
        command = message['text'].strip().lower()

        if command in ("привет", "здарова", "добрый день", "хай", "здравствуйте", "ку", "здорово"):
            self.send_msg(user_id, "Команда SINTEZ приветствует тебя!\n"
                                   "В меню ты можешь найти самую важную информацию:", self.cashed_kb.menu)
            self.stage = StageMenu
        elif command in ("menu", "меню", "назад"):
            self.send_msg(user_id, "Выберите пункт из меню:", self.cashed_kb.menu)
            self.stage = StageMenu
        else:
            if not self.stage(self, event).action():
                self.send_msg(user_id, 'Ошибка ввода. Напишите "Меню"')

    def send_msg(self, user_id, msg, keyboard: vk_api.keyboard = None, attachment: str = None) -> None:
        method_info = {
            'user_id': user_id,
            'message': msg,
            'random_id': get_random_id(),
        }
        if keyboard and keyboard != self.cashed_kb.empty:
            method_info['keyboard'] = keyboard.get_keyboard()
        else:
            method_info['keyboard'] = keyboard

        if attachment:
            method_info['attachment'] = attachment

        self.vk.method('messages.send', method_info)
