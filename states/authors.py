from keyboards import Keyboards
from misc import StateIndex
from states import BaseState


class StateAuthors(BaseState):

    def number_action(self, number):
        author = self.bot.db.get_authors_by_id(number - 1)
        if author:
            attach = [author.photo] + [music.track for music in author.music]
            self.bot.send_msg(self.request.user_id, f"{author.name}", attachment=attach,
                              keyboard=Keyboards.artists)
            self.bot.db.change_user_state(self.request.user_id, StateIndex.authors2)
        else:
            self.bot.send_msg(self.request.user_id, "Ошибка\nАртиста с таким номером не существует",
                              keyboard=Keyboards.menu)
            self.bot.db.change_user_state(self.request.user_id, StateIndex.menu)

    def run(self):
        if self.request.command.isdigit():
            self.number_action(int(self.request.command))
        elif self.request.command == 'назад':
            self.bot.db.change_user_state(self.request.user_id, StateIndex.menu)
            self.bot.send_msg(self.request.user_id, "Выберите пункт из меню:", Keyboards.menu)
        else:
            self.bot.send_msg(self.request.user_id, "Некорректный ввод", keyboard=Keyboards.menu)
            self.bot.db.change_user_state(self.request.user_id, StateIndex.menu)
        return True


class StateAuthors2(StateAuthors):

    def run(self):
        if self.request.command == 'следующий':
            pass
            # self.numbers += 1
            # self.number_action(self.numbers)
        elif self.request.command == 'предыдущий':
            pass
            # self.numbers -= 1
            # self.number_action(self.numbers)
        elif self.request.command == 'назад':
            self.bot.db.change_user_state(self.request.user_id, StateIndex.menu)
            self.bot.send_msg(self.request.user_id, "Выберите пункт из меню:", Keyboards.menu)
        else:
            self.bot.send_msg(self.request.user_id, "Некорректный ввод", keyboard=Keyboards.menu)
            self.bot.db.change_user_state(self.request.user_id, StateIndex.menu)
        return True
