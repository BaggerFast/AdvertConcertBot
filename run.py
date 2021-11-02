#!/usr/bin/env python3
import traceback
from bot import Bot
from misc import Settings
from misc.addition import write_log_file


def main():
    bot = Bot()
    try:
        bot.run()
    except Exception:
        print(Settings.debug, type(Settings.debug))
        if Settings.debug:
            print(traceback.format_exc())
        else:
            write_log_file(bot)
            main()


if __name__ == "__main__":
    main()
