#!/usr/bin/env python3
import socket
import traceback
from bot import Bot
from misc import Settings
from misc.addition import write_log_file


def main():
    bot = Bot()
    try:
        bot.run()
    except socket.timeout:
        main()
    except Exception as error:
        if Settings.debug:
            traceback.print_exc()
        else:
            write_log_file(bot, error)
            main()


if __name__ == "__main__":
    main()
