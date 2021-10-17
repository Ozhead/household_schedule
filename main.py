from telegram_handler import TelegramHandler
from os import walk
from profile import Profile
import threading
import time


class Main:
    def __init__(self):
        self.thread = None
        self.profiles = []

    def parse_profiles(self):
        # dps = dir paths
        # dns = dir names
        # fns = file names
        for (dps, dns, fns) in walk("profiles"):
            for fn in fns:
                if fn == "example.yml":
                    continue

                self.profiles.append(Profile(fn[0:-4]))
        # end for

        print(self.profiles)
# end main


def th_thread(omain):
    th = TelegramHandler(omain.profiles)
    th.run()


if __name__ == "__main__":
    m = Main()
    m.parse_profiles()
    x = threading.Thread(target=th_thread, args=(m,))
    x.start()

    while True:
        time.sleep(1)