from contextlib import contextmanager
from time import perf_counter
from colorama import Fore, Back, Style

from collections import deque
from typing import TypeVar, List

SelfTag = TypeVar("SelfTag", bound="Tag")


# ==========================================================
class TimerStoppedException(Exception):
    pass


# ==========================================================
class Tag:
    def __init__(self, id: int, text: str, status: int = 1):
        self._id = id
        self._sons = []
        self._elapsed_time = 0.0
        self._iterations = 0
        self._text = text
        self._status = status

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value

    @property
    def sons(self) -> List[SelfTag]:
        return self._sons

    @sons.setter
    def sons(self, value: List[SelfTag]) -> None:
        self._sons = value

    @property
    def elapsed_time(self) -> float:
        return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, value: float) -> None:
        self._elapsed_time = value

    def update_elapsed_time(self, value: float) -> None:
        self._elapsed_time += value
        self._iterations += 1
        self._status = 0

    @property
    def iterations(self) -> int:
        return self._iterations

    @iterations.setter
    def iterations(self, value: int) -> None:
        self._iterations = value

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int) -> None:
        self._status = value
        if value == 0:
            self.iterations += 1

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    def add_son(self, tag: SelfTag) -> None:
        self._sons.append(tag)

    def __str__(self) -> str:
        return f"Tag {self._id} - Status: {self._status} - Nb iterations: {self._iterations}"


# ==========================================================
class SingletonTimeMyCode(type):
    """
    A metaclass that implements the Singleton design pattern.
    Only one instance of the class can exist at a time.

    Usage:
    class MyClass(metaclass=SingletonTimeMyCode):
        pass
    """

    _instances = {}

    # ----------------------------------------------------------------
    def __call__(cls, *args, **kwargs):
        if (
            cls not in cls._instances
            or ("reinit" in kwargs and kwargs["reinit"] is True)
            or cls._instances[cls]._start == None
        ):
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# ==========================================================
class TimeMyCode(metaclass=SingletonTimeMyCode):

    _root_tag = None
    _debug = None
    _start = None

    # ----------------------------------------------------------------
    def __init__(self, reinit: bool = False, debug: bool = True) -> None:
        """
        Initializes a new instance of the Timeit class.

        Args:
            reinit (bool, optional): Indicates whether to reinitialize the Timeit instance. Defaults to False.
            debug (bool, optional): Indicates whether to enable debug mode. Defaults to True.
        """
        self._debug = debug
        self.reinit()

    # ----------------------------------------------------------------
    def reinit(self) -> None:
        """
        Reinitializes the Timeit object by resetting the current ID, total execution time,
        and clearing the tags dictionary. It then resumes the timer by calling the play method.
        """
        self._current_id = 0
        self._total_exectime = 0
        self._root_tag = Tag(id=0, text="root")
        self.play()

    # ----------------------------------------------------------------
    @contextmanager
    def tag(self, text: str, color: str = Fore.WHITE):
        """
        Measures the elapsed time and number of iterations for a specific tag.

        Args:
            tag (str): The tag to identify the measurement.

        Yields:
            None: This function is a generator and yields nothing.

        """
        if self._debug:
            if self._start == None:
                self.play()

            # If tag does not exist, create it
            if text not in [tag.text for tag in self.tags_list]:
                new_tag = Tag(id=self.new_id, text=text)
                self.last_running_tag.add_son(new_tag)
                current_tag = new_tag

            else:
                current_tag = self.get_tag_by_text(text)

            start = perf_counter()

            yield

            current_tag.update_elapsed_time(perf_counter() - start)

    # ----------------------------------------------------------------
    @property
    def last_running_tag(self) -> Tag:
        """
        Returns the last running tag from the tags list.

        If there are no running tags, it returns the root tag.

        Returns:
            The last running tag from the tags list, or the root tag if there are no running tags.
        """
        try:
            return [tag for tag in self.tags_list if tag.status == 1][-1]
        except:
            return self._root_tag

    # ----------------------------------------------------------------
    @property
    def tags_list(self) -> list:
        """
        Returns a list of all tags in the tree.

        This method performs a breadth-first search on the tree starting from the root tag.
        It collects all the tags encountered during the search and returns them as a list.

        Returns:
            A list of all tags in the tree.
        """
        tags = []

        queue = deque([self._root_tag])

        while len(queue) > 0:
            tag_obj = queue.popleft()
            tags.append(tag_obj)

            if len(tag_obj.sons) > 0:
                queue.extendleft(tag_obj.sons[::-1])

        return tags

    # ----------------------------------------------------------------
    @property
    def current_exectime(self) -> float:
        """
        Returns the current execution time in seconds.

        Returns:
            float: The current execution time.
        """
        if self._start == None:
            return 0.0

        return perf_counter() - self._start

    # ----------------------------------------------------------------
    @property
    def new_id(self) -> int:
        """
        Generates a new ID and increments the current ID by 1.

        Returns:
            int: The newly generated ID.
        """
        return max([tag.id for tag in self.tags_list]) + 1

    # ----------------------------------------------------------------
    @property
    def depth(self) -> int:
        """
        Calculate the maximum depth of the tree starting from the root tag.

        Returns:
            The maximum depth of the tree as an integer.
        """
        if len(self._root_tag.sons) == 0:
            return 0

        max_depth = 0
        current_depth = 0

        queue = deque([self._root_tag])

        while len(queue) > 0:
            tag_obj = queue.popleft()

            if len(tag_obj.sons) > 0:
                current_depth += 1
                max_depth = max(max_depth, current_depth)
                queue.extendleft(tag_obj.sons[::-1])
            else:
                current_depth -= 1

        return max_depth

    # ----------------------------------------------------------------
    @property
    def leaves(self) -> list:
        """
        Returns a list of tags that have no sons.

        Returns:
            list: A list of tags with no sons.
        """
        return [tag for tag in self.tags_list if len(tag.sons) == 0]

    # ----------------------------------------------------------------
    @property
    def longest_exectime_tags(self) -> list:
        """
        Returns a list of leaf tags with the longest execution time.

        Returns:
            list: A list of leaf tags with the longest execution time.
        """
        return [
            tag
            for tag in self.leaves
            if round(tag.elapsed_time, 2)
            == round(max([tag.elapsed_time for tag in self.leaves]), 2)
        ]

    # ----------------------------------------------------------------
    def get_tag_by_text(self, text: str) -> Tag:
        tag = [tag for tag in self.tags_list if tag.text == text][0]
        tag.status = 1
        return tag

    # ----------------------------------------------------------------
    def stop(self) -> float:
        """
        Stops the timer and returns the total execution time.

        Returns:
            float: The total execution time in seconds.
        """
        try:
            self._total_exectime += perf_counter() - self._start
            self._start = None
            return self._total_exectime
        except:
            raise TimerStoppedException("The timer is not started.")

    # ----------------------------------------------------------------
    def play(self) -> None:
        """
        Start the timer for the play operation.
        """
        self._start = perf_counter()

    # ----------------------------------------------------------------
    def summary(self, colored: bool = False, stop_timer: bool = True) -> str:
        """
        Returns a formatted time log containing information about the elapsed time and iterations for each tag.

        Args:
            stop_timer (bool, optional): Indicates whether to stop the timer before generating the log. Defaults to True.

        Returns:
            str: The formatted time log.

        Raises:
            None
        """
        if self._debug:
            print(Style.RESET_ALL)

            time_log = "\nTime log:\n"

            if stop_timer and self._start != None:
                total_exectime = self.stop()
            else:
                total_exectime = self.current_exectime

            if len(self.tags_list) > 0:
                max_size_tag = (
                    max([len(tag.text) for tag in self.tags_list]) + self.depth * 2 + 1
                )
                max_size_elapsed_time = max(
                    [len(f"{tag.elapsed_time:.2f}") for tag in self.tags_list]
                )
                max_size_iterations = max(
                    [len(str(tag.iterations)) for tag in self.tags_list]
                )

                queue = deque([(self._root_tag, 0)])

                while len(queue) > 0:
                    tag_obj, level = queue.pop()

                    if tag_obj.id > 0:
                        color = Style.RESET_ALL
                        if tag_obj in self.longest_exectime_tags and colored:
                            color = Fore.RED

                        if tag_obj.iterations == 0:
                            time_log += f"{color}{'   '*level + '- ' + tag_obj.text + ' ':.<{max_size_tag}}... {'0':>{max_size_elapsed_time}}s -> {'0':>{max_size_iterations}} it [0.0 s/it]\n"
                        else:
                            time_log += f"{color}{'   '*level + '- ' + tag_obj.text + ' ':.<{max_size_tag}}... {round(tag_obj.elapsed_time,2):>{max_size_elapsed_time}}s -> {str(tag_obj.iterations):>{max_size_iterations}} it [{(tag_obj.elapsed_time / tag_obj.iterations):.4f} s/it]\n"

                    if len(tag_obj.sons) > 0:
                        for son in tag_obj.sons[::-1]:
                            queue.append((son, level + 1))

            else:
                time_log += "  - No tags registered."

            time_log += f"\nTotal time: {total_exectime:.2f}s"

            return time_log

        return "Time log is disabled. Set debug=True to enable it."

    # ----------------------------------------------------------------
    def __str__(self) -> str:
        return f"Current execution time: {self.current_exectime:.2f} s"
