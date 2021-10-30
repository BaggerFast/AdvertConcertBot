from states import BaseState
from misc import StateIndex, Keyboards


class StateAuthors(BaseState):

    def switch_author(self, number):
        author = self.db.get_authors_by_id(number - 1)
        if author:
            self.show_author(author, number-1)
        else:
            self.bot.send_msg(self.request.user_id, "Ошибка\nАртиста с таким номером не существует", kb=Keyboards.menu)
            self.db.set_user_state(self.request.user_id, StateIndex.menu)

    def show_author(self, author, number):
        attach = [author.photo] + [music.track for music in author.music]
        self.bot.send_msg(self.request.user_id, f"{author.id + 1}. {author.name}", attachment=attach,
                          kb=Keyboards.artists)
        self.db.set_user_selected_author(self.request.user_id, number)
        self.db.set_user_state(self.request.user_id, StateIndex.state_manager)

    def go_menu(self):
        self.db.set_user_state(self.request.user_id, StateIndex.menu)
        self.bot.send_msg(self.request.user_id, "Выберите пункт из меню:", Keyboards.menu)

    def set_error(self):
        self.bot.send_msg(self.request.user_id, "Некорректный ввод", kb=Keyboards.menu)
        self.db.set_user_state(self.request.user_id, StateIndex.menu)

    def run(self):
        if self.request.command.isdigit():
            self.switch_author(int(self.request.command))
        elif self.request.command == 'назад':
            self.go_menu()
        else:
            self.set_error()
        return True


class StateAuthors2(StateAuthors):

    def __init__(self, bot, request):
        super().__init__(bot, request)
        self.__messages = {
            'следующий': lambda: self.switch_author(self.db.get_user_selected_author(self.request.user_id)+1),
            'предыдущий': lambda: self.switch_author(self.db.get_user_selected_author(self.request.user_id)-1),
            'назад': self.go_menu,
        }

    def switch_author(self, number):
        number = number % len(self.db.get_authors)
        author = self.db.get_authors_by_id(number)
        if author:
            self.show_author(author, number)

    def run(self):
        if self.request.command in self.__messages.keys():
            self.__messages[self.request.command]()
        else:
            self.set_error()
        return True
