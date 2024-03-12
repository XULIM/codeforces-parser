import colorama
import time


class loading:
    @staticmethod
    def spinner(flag) -> None:
        sp = "-\\|/"
        i: int = 0
        while flag:
            i = (i + 1) % 4
            print(sp[i], end="\r")
            time.sleep(0.5)
