from random import random
from time import perf_counter, sleep
import traceback
from typing import Callable


class LazyMain:
    def __init__(
        self,
        main: Callable[..., bool],
        error_handler: Callable[[Exception], None] = None,  # type: ignore
        print_logs: bool = True,
        sleep_min=3,
        sleep_max=5,
        loop_count=-1,
    ):
        """
        main: The function that will be called every loop.
        error_handler: If the `main` function throws an error, this will be called.
        print_logs: If it should print logs.
        sleep_min: Minimum sleep time, in seconds.
        sleep_max: Maximum sleep time, in seconds.
        loop_count: How many times this will loop. If -1, it will infinitely loop.
        """
        self.main = main
        self.error_handler = error_handler
        self.print_logs = print_logs
        self.sleep_min = sleep_min
        self.sleep_max = sleep_max
        self.loop_count = loop_count

    def __get_sleep_time(self):
        return random() * self.sleep_min + self.sleep_max - self.sleep_min

    def run(self, *args, **kwargs):
        """
        Starts the loop.
        """
        while True:
            ok = False
            t1 = perf_counter()

            try:
                ok = self.main(*args, **kwargs)
            except Exception as e:
                if self.print_logs:
                    print("An error ocurred.", e)
                traceback.print_exc()

                if self.error_handler != None:
                    self.error_handler(e)

            sleep_time = self.__get_sleep_time()

            if self.loop_count > 0:
                self.loop_count -= 1

            if ok:
                t2 = perf_counter()

                if self.print_logs:
                    print(f"Done in {t2 - t1:.2f}s.")

                if self.loop_count > 0 and self.print_logs:
                    print(f"Sleeping for {sleep_time:.2f}s...")

            if self.loop_count == 0:
                break

            sleep(sleep_time)
