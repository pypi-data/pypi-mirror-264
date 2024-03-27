from typing import Callable, Any
from typing_extensions import Self


class Infix:
    def __init__(self, func: Callable[[Any, Any], Any]) -> None:
        self.__f = func

    def __ror__(self, __other: Any) -> Self:
        return Infix(lambda var: self.__f(__other, var))

    def __or__(self, __other: Any) -> Any:
        return self.__f(__other)

    def __rlshift__(self, __other: Any) -> Self:
        return Infix(lambda var, self=self, other=__other: self.__f(other, var))

    def __rshift__(self, __other: Any) -> Any:
        return self.__f(__other)

    def __call__(self, __a: Any, __b: Any) -> Any:
        return self.__f(__a, __b)

sub = Infix(lambda a, b: a - b)
print(-1 |sub| "s")

