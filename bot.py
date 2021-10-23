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
from states import StateMenu, StateAuthors, BaseState, StateAuthors2
from fuzzywuzzy import fuzz
from states import StatesManager


def words_compare(command, words):
    for word in words:
        if fuzz.ratio(command, word) > 75:
            return True
    return False


class Bot:
    class State:
        menu = StateMenu
        authors = StateAuthors
        authors2 = StateAuthors2

    def __init__(self):
        token = "ff8d21d2ec05262976bb5df59d6d2ef18b71ae7419fda1ad53305cc4f4451d705daf646700927e978156a"
        group_id = 80176390
        self.__state: BaseState = None
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk, group_id)
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
        self.create_user_if_not_exists(event.obj.user_id)
        self.send_msg(event.obj.user_id, 'ГС\nЧтобы узнать больше, напиши "Меню"', Keyboards.empty)

    def create_user_if_not_exists(self, vk_id):
        if not self.db.get_users_by_id(vk_id):
            user = Database.Users(vk_id=vk_id, state_id=0)
            self.db.session.add(user)
            self.db.session.commit()

    def change_state(self, user, state_id):
        if type(user) == int:
            user = self.db.get_users_by_id(user)
        user.state = state_id
        self.db.session.commit()

    def new_msg_action(self, event):
        msg = event.obj['message']["text"].strip().lower().split()[-1]
        request = EventInfo(event.obj['message'], event.obj['message']['peer_id'], msg)
        self.create_user_if_not_exists(request.user_id)
        current_user = self.db.get_users_by_id(request.user_id)
        if self.open_menu_commands(request):
            self.change_state(current_user, 1)
        else:
            if not current_user.state_id:
                return
            state = StatesManager.get_state(current_user.state_id)(self, request)
            if not state.run():
                self.send_msg(request.user_id, 'Неизвестная ошибка, напишите "Меню"')

    def open_menu_commands(self, request):
        if words_compare(request.command, ("привет", "здарова", "добрый день", "хай", "здравствуйте", "ку")):
            self.send_msg(request.user_id, "Команда SINTEZ приветствует тебя!\n"
                                           "В меню ты можешь найти самую важную информацию:", Keyboards.menu)
        elif words_compare(request.command, ("menu", "меню")):
            self.send_msg(request.user_id, "Выберите пункт из меню:", Keyboards.menu)
        else:
            return False
        return True

    def send_msg(self, user_id, msg, keyboard: vk_api.keyboard = None, attachment: Union[str, list] = None) -> None:
        method_info = {
            'user_id': user_id,
            'message': msg,
            'random_id': get_random_id(),
        }
        if keyboard and keyboard != Keyboards.empty:
            method_info['keyboard'] = keyboard.get_keyboard()
        else:
            method_info['keyboard'] = keyboard

        if attachment:
            method_info['attachment'] = attachment if type(attachment) != list else ','.join(attachment)

        self.vk.method('messages.send', method_info)
