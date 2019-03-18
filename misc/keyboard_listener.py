import threading
import msvcrt


class KeyEventThread(threading.Thread):
    key = ""

    def run(self):
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                print(key)  # just to show the result
