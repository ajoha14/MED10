import threading
import msvcrt


####NOT WORKING####
class KeyEventThread(threading.Thread):
    key = ""

    def __init__(self):
        print("Class KeyEventThread is not working")

    def run(self):
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                print(key)  # just to show the result



