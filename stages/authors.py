from stages import Stage


class StageAuthors(Stage):
    numbers = 0

    def number_action(self, number):
        author = self.bot.db.get_authors_by_id(number - 1)
        if author:
            attach = [author.photo]+[music.track for music in author.music]
            self.bot.send_msg(self.event.user_id, f"{author.name}", attachment=attach, keyboard=self.bot.cashed_kb.artists)
        else:
            self.bot.send_msg(self.event.user_id, "Артиста с таким номером не существует")

    def action(self):
        if self.event.command.isdigit():
            self.number_action(int(self.event.command))
            self.numbers = int(self.event.command)
            self.bot.stage = StageAuthors2(self.bot, self.event)
        else:
            return False
        return True


class StageAuthors2(StageAuthors):

    def action(self):
        if self.event.command == 'следующий':
            self.numbers += 1
            self.number_action(self.numbers)
        elif self.event.command == 'предыдущий':
            self.numbers -= 1
            self.number_action(self.numbers)
        elif self.event.command == 'назад':
            self.bot.stage = self.bot.Stage.menu(self.bot, self.event)
            self.bot.send_msg(self.event.user_id,  "Выберите пункт из меню:", self.bot.cashed_kb.menu)
        else:
            return False
        return True
