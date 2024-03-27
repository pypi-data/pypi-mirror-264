import time
class ProgressBar:
    def __init__(self, task: str, total_length: int = 20, *, finish_msg: str = None) -> None:
        self.__task = task
        self.__tl = total_length
        self.__progress = 0

        self.__fm = finish_msg

    def __update_progress(self, percentage):
        self.__progress = percentage

    def __display(self):
        num_filled = int(self.__progress / 100 * self.__tl)
        num_empty = self.__tl - num_filled
        bar = "\033[34m[\033[37m" + "\033[32m|" * num_filled + " " * num_empty + "\033[34m]\033[37m " + str(self.__progress) + "%"
        if self.__progress < 100:
            return f"{self.__task}: {bar}"
        else:
            return f"{self.__task}: {bar} - Done!\n" if self.__fm is None else f"{self.__task}: {bar} - {self.__fm}\n"

    def __call__(self):
        for i in range(101):
            self.__update_progress(i)
            print(self.__display(), end='\r')
            time.sleep(0.1)  # Simulating progress, you can remove this line in actual usage

