import traceback
from datetime import datetime
from typing import Union
import vk_api
from vk_api.keyboard import VkKeyboard
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from database import Database
from keyboards import Keyboards
from misc import EventInfo, Settings
from stages import StageMenu, StageAuthors
from fuzzywuzzy import fuzz


class Bot:
    class Stage:
        menu = StageMenu
        authors = StageAuthors

    def __init__(self):
        token = "ff8d21d2ec05262976bb5df59d6d2ef18b71ae7419fda1ad53305cc4f4451d705daf646700927e978156a"
        group_id = 80176390
        self.stage = None
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk, group_id)
        self.cashed_kb = Keyboards()
        self.db = Database()

    def run(self):
        print("Bot запущен...")
        try:
            event_data = {
                VkBotEventType.GROUP_JOIN: self.group_join_action,
                VkBotEventType.MESSAGE_NEW: self.new_msg_action,
            }
            for event in self.longpoll.listen():
                if event.type in event_data.keys():
                    event_data[event.type](event)
        except Exception:
            self.__logger()

    def __logger(self):
        if not Settings.debug:
            with open(f"exception-{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}", "w") as file:
                file.write(traceback.format_exc())
                self.run()
        else:
            raise BaseException

    def group_join_action(self, event):
        self.send_msg(event.obj.user_id, 'ГС\nЧтобы узнать больше, напиши "Меню"', self.cashed_kb.empty)

    def cheacker(self, command, words):
        for word in words:
            if fuzz.ratio(command, word) > 75:
                return True
        else:
            return False

    def new_msg_action(self, event):
        request = EventInfo(event.obj['message'], event.obj['message']['peer_id'],
                            event.obj['message']['text'].strip().lower())
        if self.cheacker(request.command, ("привет", "здарова", "добрый день", "хай", "здравствуйте", "ку", "здорово")):
            self.send_msg(request.user_id, "Команда SINTEZ приветствует тебя!\n"
                                           "В меню ты можешь найти самую важную информацию:", self.cashed_kb.menu)
            self.stage = self.Stage.menu(self, request)
        elif self.cheacker(request.command, ("menu", "меню")):
            self.send_msg(request.user_id, "Выберите пункт из меню:", self.cashed_kb.menu)
            self.stage = self.Stage.menu(self, request)
        else:
            if not self.stage:
                return
            self.stage.event = request
            if not self.stage.action():
                self.send_msg(request.user_id, 'Ошибка ввода. Напишите "Меню"')

    def send_msg(self, user_id, msg, keyboard: vk_api.keyboard = None, attachment: Union[str, list] = None) -> None:
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
            method_info['attachment'] = attachment if type(attachment) != list else ','.join(attachment)

        self.vk.method('messages.send', method_info)
