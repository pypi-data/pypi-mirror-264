import argparse

from pytube import YouTube
import time
import os

import asyncio


class _ProgressBar:
    def __init__(
        self,
        task: str,
        total_length: int = 20,
        *,
        finish_msg: str = None,
    ) -> None:
        self.__task = task
        self.__tl = total_length
        self.progress = 0
        self.__fm = finish_msg

    def __update_progress(self, percentage):
        self.progress = percentage

    def __display(self):
        num_filled = int(self.progress / 100 * self.__tl)
        num_empty = self.__tl - num_filled
        bar = (
            "\033[34m[\033[37m"
            + "\033[32m|" * num_filled
            + " " * num_empty
            + "\033[34m]\033[37m "
            + str(self.progress)
            + "%"
        )
        if self.progress < 100:
            return f"{self.__task}: {bar}"
        else:
            return (
                f"{self.__task}: {bar} - Done!\n"
                if self.__fm is None
                else f"{self.__task}: {bar} - {self.__fm}\n"
            )

    async def __start_async(self):
        for i in range(101):
            self.__update_progress(i)
            print(self.__display(), end="\r")
            # Simulating progress, you can remove this line in actual usage
            await asyncio.sleep(0.1)

    def __start_sync(self):
        for i in range(101):
            self.__update_progress(i)
            print(self.__display(), end="\r")
            # Simulating progress, you can remove this line in actual usage
            time.sleep(0.1)

    def start(self, *, asynchronous: bool = False) -> None:
        if asynchronous:
            asyncio.run(self.__start_async())
        else:
            self.__start_sync()


def download() -> None:
    url = input("YouTube Link: ")
    yt = YouTube(url)

    _ProgressBar("Finding video on YouTube", finish_msg="Found video").start()

    print(f"Title:  {yt.title}")
    print(f"Views:  {yt.views}")
    print(f"Length: {yt.length}")

    where_to_save = input("Enter download path: ")
    if os.path.exists(where_to_save):
        _ProgressBar("Downloading video").start(asynchronous=True)
        yd = yt.streams.get_highest_resolution()
        yd.download(where_to_save)
    else:
        print(
            f"Oops! It looks like the path {where_to_save} doesn't exist. Do you want to create that directory and download the video there instead?"
        )
        print("\033[33m[Y] Yes\033[37m  [N] No, (default 'yes'): ", end="")
        _new_dir = input().lower()
        if _new_dir in ["yes", "y"]:
            try:
                os.mkdir(_new_dir)
            except FileExistsError as e:
                print(f"Error: {e.__class__.__name__}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PyVidFetcher Command Line Interface")
    parser.add_argument(
        "--download", "-d", action="store_true", help="Start the download process"
    )
    args = parser.parse_args()

    if args.download:
        download()


if __name__ == "__main__":
    main()
