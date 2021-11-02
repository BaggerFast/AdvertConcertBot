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
        if not Settings.debug:
            write_log_file(bot)
            main()
        else:
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
