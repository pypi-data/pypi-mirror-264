import inspect
import os

from datetime import datetime
from icecream import ic


DEFAULT_PREFIX = "tl| "

# ANSI escape codes for Solarized Dark colors
SOLARIZED_BASE03 = "\033[0;30m"
SOLARIZED_BLUE = "\033[0;34m"
SOLARIZED_BASE1 = "\033[0;36m"
SOLARIZED_BASE2 = "\033[0;37m"
SOLARIZED_GREEN = "\033[0;32m"
DARK_YELLOW = "\033[0;93m"  # Dark Yellow
END_COLOR = SOLARIZED_BASE03  # Reset color to default


class Debugger(type):
    def __repr__(self) -> str:
        return "<class 'Debugger'>"


class ToreLibDebugger(metaclass=Debugger):

    def __init__(
        self,
        prefix=DEFAULT_PREFIX,
    ) -> None:
        self.__prefix = prefix

    def __call__(self, *args):
        result = f"{self.__prefix}"
        callFrame = inspect.stack()[1]

        if not args:  # E.g. tl().
            line = callFrame.lineno
            filename = os.path.basename(os.path.abspath(callFrame.filename))
            nl = ""
            for char in filename[::-1]:
                if char != "\\":
                    nl += char
                else:
                    break
            ns = nl[::-1]
            del nl
            blue = ""
            white = ""
            for char in ns:
                if char == ".":
                    white += char
                    break
                else:
                    blue += char
            dummy = ""
            for char in ns[::-1]:
                if char != ".":
                    dummy += char
                else:
                    break
            white += dummy[::-1]
            result += f"\033[34m{blue}{END_COLOR}{white}:{SOLARIZED_GREEN}{line} {DARK_YELLOW}in {END_COLOR}<module>{self.__formatTime()}{END_COLOR}"
        elif len(args) == 1:  # E.g. tl(1).
            passthrough = args[0]
            callFrame.
        else:  # E.g. tl(1, 2, 3).
            passthrough = args

        print(SOLARIZED_BASE03 + result)

    def __formatTime(self):
        output = " at "
        now = datetime.now()
        formatted = now.strftime("%H:%M:%S.%f")[:-3]
        for char in formatted:
            if char != ":":
                output += SOLARIZED_GREEN + char
            else:
                output += END_COLOR + char
        return "%s" % output


tl: ToreLibDebugger = ToreLibDebugger()
s = "Hello, world!"
t = "Torrez"
tl(s)
ic(s, t)
