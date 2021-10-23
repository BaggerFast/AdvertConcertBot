from keyboards import Keyboards
from misc import StateIndex
from states import BaseState


class StateAuthors(BaseState):

    def number_action(self, number):
        author = self.db.get_authors_by_id(number - 1)
        if author:
            attach = [author.photo] + [music.track for music in author.music]
            self.bot.send_msg(self.request.user_id, f"{author.name}", attachment=attach, kb=Keyboards.artists)
            self.db.set_user_selected_author(self.request.user_id, number)
            self.db.change_user_state(self.request.user_id, StateIndex.state_manager)
        else:
            self.bot.send_msg(self.request.user_id, "Ошибка\nАртиста с таким номером не существует",
                              kb=Keyboards.menu)
            self.db.change_user_state(self.request.user_id, StateIndex.menu)

    def go_menu(self):
        self.db.change_user_state(self.request.user_id, StateIndex.menu)
        self.bot.send_msg(self.request.user_id, "Выберите пункт из меню:", Keyboards.menu)

    def set_error(self):
        self.bot.send_msg(self.request.user_id, "Некорректный ввод", kb=Keyboards.menu)
        self.db.change_user_state(self.request.user_id, StateIndex.menu)

    def run(self):
        if self.request.command.isdigit():
            self.number_action(int(self.request.command))
        elif self.request.command == 'назад':
            self.go_menu()
        else:
            self.set_error()
        return True


class StateAuthors2(StateAuthors):

    def run(self):
        if self.request.command == 'следующий':
            self.number_action(self.db.get_user_selected_author(self.request.user_id)+1)
        elif self.request.command == 'предыдущий':
            self.number_action(self.db.get_user_selected_author(self.request.user_id)-1)
        elif self.request.command == 'назад':
            self.go_menu()
        else:
            self.set_error()
        return True
