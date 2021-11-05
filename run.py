#!/usr/bin/env python3
import sys
import traceback
from bot import Bot
from misc import Settings
from misc.addition import write_log_file


def main():
    bot = Bot()
    try:
        bot.run()
    except Exception as error:
        if Settings.debug:
            traceback.print_exc()
        else:
            if sys.exc_info()[1] != "[901] Can't send messages for users without permission":
                write_log_file(bot, error)
            main()


if __name__ == "__main__":
    main()
