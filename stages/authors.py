from stages import Stage


class StageAuthors(Stage):

    def action(self):
        if self.command.isdigit() or self.command in ('следующий', 'предыдущий'):
            if self.command.isdigit():
                number = int(self.command)
                if self.bot.db.get_authors_by_id(number-1):
                    id, name, photo = self.bot.db.get_authors_by_id(number-1)
                    self.bot.send_msg(self.user_id, f"{number}. {name}", attachment=photo)
                    for music in self.bot.db.get_music_by_author_id(id):
                        self.bot.send_msg(self.user_id, msg='', attachment=music)
                else:
                    self.bot.send_msg(self.user_id, "Артиста с таким номером не существует")
        else:
            return False
        return True
