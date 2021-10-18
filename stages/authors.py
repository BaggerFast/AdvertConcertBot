from stages import Stage


class StageAuthors(Stage):

    def action(self):
        if self.request == 'предыдущий':
            if number - 1 == 0:
                self.bot.write_msg(self.user_id, "Это первый в списке артист")
                outOfList = True
            else:
                number -= 1

        elif self.request == 'следующий':
            if number + 1 > len(artist):
                self.bot.write_msg(self.user_id, "Это последний в списке артист")
                outOfList = True
            else:
                number += 1

        if self.request.isdigit() or self.request in ('следующий', 'предыдущий'):
            if self.request.isdigit():
                number = int(self.request)

            if outOfList:
                outOfList = False

            elif number <= len(artist):
                pass
                # artistLabel = str(number) + '. ' + artist[number - 1][0]
                # write_msg(user_id, artistLabel)
                # send_attachment(user_id, artist[number - 1][1])
                # for i in range(2, 5):
                #     if artist[number - 1][i] is not None:
                #         send_attachment(user_id, artist[number - 1][i])
                # keyboard = create_keyboard_artist()

            else:
                self.bot.write_msg(self.user_id, "Артиста с таким номером не существует")
        else:
            self.bot.write_msg(self.user_id, 'Ошибка ввода. Напишите "Меню"')
