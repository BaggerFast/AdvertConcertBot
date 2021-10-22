from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboards:
    def __init__(self):
        self.menu = self.create_kb_menu()
        self.artists = self.create_kb_artists()
        self.empty = self.create_kb_empty()

    @staticmethod
    def create_kb_empty() -> VkKeyboard:
        keyboard = VkKeyboard(one_time=False)
        return keyboard.get_empty_keyboard()

    @staticmethod
    def create_kb_menu() -> VkKeyboard:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("SINTEZ", VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button("Концерт", VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button("Артисты", VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button("Закрыть", VkKeyboardColor.NEGATIVE)

        return keyboard

    @staticmethod
    def create_kb_artists() -> VkKeyboard:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Предыдущий", VkKeyboardColor.PRIMARY)
        keyboard.add_button("Следующий", VkKeyboardColor.PRIMARY)

        keyboard.add_line()
        keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)

        return keyboard
