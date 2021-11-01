#!/usr/bin/env python3
import os
import traceback
from bot import Bot
from datetime import datetime
from misc import Settings, get_path


def write_log_file(bot: Bot) -> None:
    name = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    exception_path = get_path(f"exceptions")
    if not os.path.exists(exception_path):
        os.mkdir(exception_path)
    file_path = f"{exception_path}/{name}.txt"
    with open(file_path, "w") as file:
        file.write(traceback.format_exc())
    bot.send_log_to_admin(name, file_path)


def main():
    bot = Bot()
    try:
        bot.run()
    except Exception:
        if not Settings.debug:
            write_log_file(bot)
            main()
        else:
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
