import os

import vk_api
import requests
import traceback
from typing import Union
from datetime import datetime
from states import StatesManager
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from misc import Keyboards, Database, EventInfo, Settings, StateIndex, words_compare, get_path


class Bot:

    def __init__(self):
        self.group_id = Settings.group_id
        self.__state = None
        self.vk = vk_api.VkApi(token=Settings.token)
        self.longpoll = VkBotLongPoll(self.vk, self.group_id)
        self.upload = vk_api.VkUpload(self.vk)
        self.vk_methods = self.vk.get_api()
        self.db = Database()

    def run(self) -> None:
        print("Bot запущен...")
        try:
            event_data = {
                VkBotEventType.GROUP_JOIN: self.__group_join_action,
                VkBotEventType.MESSAGE_NEW: self.__new_msg_action,
            }
            for event in self.longpoll.listen():
                if event.type in event_data.keys():
                    event_data[event.type](events)
        except Exception:
            self.__logger()

    def __logger(self) -> None:
        if not Settings.debug:
            if not os.path.exists(get_path(f"/exceptions/")):
                os.mkdir(get_path(f"/exceptions/"))
            name = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
            file_path = get_path(f"/exceptions/{name}.txt")
            with open(file_path, "w") as file:
                file.write(traceback.format_exc())
            self.__send_log_to_admin(name)
            self.run()
        else:
            raise BaseException

    def __send_log_to_admin(self, file_name: str) -> None:
        data = self.vk.method('groups.getMembers', {'group_id': self.group_id, 'filter': 'managers'})
        for admin in data['items']:
            if admin['role'] == 'administrator':
                upload_file = self.upload.document_message(doc=get_path(f'exceptions/{file_name}.txt'), title=file_name,
                                                           peer_id=admin['id'])["doc"]
                attach = f'doc{upload_file["owner_id"]}_{upload_file["id"]}'
                self.send_msg(user_id=admin['id'], msg='Произошла ошибка, лови logfile', attachment=attach)

    def __group_join_action(self, event) -> None:
        self.db.create_user_if_not_exists(event.obj.user_id)
        self.send_msg(event.obj.user_id, 'ГС\nЧтобы узнать больше, напиши "Меню"', Keyboards.empty)

    def __new_msg_action(self, event) -> None:
        msg = event.obj['message']["text"].strip().lower().split()[-1]
        request = EventInfo(event.obj['message'], event.obj['message']['peer_id'], msg)
        current_user = self.db.create_user_if_not_exists(request.user_id)
        if self.__open_menu_commands(request):
            self.db.set_user_state(current_user, StateIndex.menu)
        else:
            if not current_user.state_id:
                return
            state = StatesManager.get_state(current_user.state_id)(self, request)
            if not state.run():
                self.send_msg(request.user_id, 'Неизвестная ошибка, напишите "Меню"')

    def __open_menu_commands(self, request: EventInfo) -> bool:
        if words_compare(request.command, ("привет", "начать", "start", "здарова", "добрый день", "хай",
                                           "здравствуйте", "ку")):
            self.send_msg(user_id=request.user_id,
                          kb=Keyboards.menu, attachment=self.get_audio_massage(request, get_path('audio/hello.mp3')))

        elif words_compare(request.command, ("menu", "меню")):
            self.send_msg(request.user_id, "Выберите пункт из меню:", Keyboards.menu)
        else:
            return False
        return True

    def get_audio_massage(self, request: EventInfo, audio_path: str) -> str:
        vk_url = self.vk.method("docs.getMessagesUploadServer", {"type": "audio_message", "peer_id": request.user_id})
        file = requests.post(vk_url['upload_url'], files={'file': open(audio_path, 'rb')}).json()["file"]
        audio_info = self.vk.method("docs.save", {"file": file})['audio_message']
        audio_vk_path = f"doc{audio_info['owner_id']}_{audio_info['id']}"
        return audio_vk_path

    def send_msg(self, user_id: int, msg: str = ' ', kb: vk_api.keyboard = None, attachment: Union[str, list] = None) -> None:
        method_info = {
            'user_id': user_id,
            'message': msg,
            'random_id': get_random_id(),
            'keyboard': kb.get_keyboard() if kb and kb != Keyboards.empty else kb,
        }

        if attachment:
            method_info['attachment'] = ','.join(attachment) if isinstance(attachment, list) else attachment

        self.vk.method('messages.send', method_info)
