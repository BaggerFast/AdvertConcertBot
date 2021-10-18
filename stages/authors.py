from stages import Stage


class StageAuthors(Stage):

    def action(self):
        if self.command.isdigit() or self.command in ('следующий', 'предыдущий'):
            if self.command.isdigit():
                number = int(self.command)
                id, name, photo = self.bot.db.get_authors_by_id(number-1)
                self.bot.send_attachment(self.user_id, photo, f"{number}. {name}")
                for music in self.bot.db.get_music_by_author_id(id):
                    self.bot.send_attachment(self.user_id, music)
            else:
                self.bot.write_msg(self.user_id, "Артиста с таким номером не существует")
        else:
            return False
        return True
