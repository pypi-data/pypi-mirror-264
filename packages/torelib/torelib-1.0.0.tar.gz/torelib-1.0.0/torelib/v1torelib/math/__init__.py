from typing import Any, _Final, Union, _tp_cache
from icecream import ic


class ises:
    def __init__(self, __obj: object):
        self.__obj = __obj

    @property
    def obj_type(self):
        return type(self.__obj)

    @obj_type.setter
    def obj_type(self, value):
        raise PermissionError("can't set obj_type")

    def is_int(self) -> bool:
        return isinstance(self.__obj, int)

    def is_float(self) -> bool:
        return isinstance(self.__obj, float)

    def is_str(self) -> bool:
        return isinstance(self.__obj, str)

    def is_tuple(self) -> bool:
        return isinstance(self.__obj, tuple)

    def is_dict(self) -> bool:
        return isinstance(self.__obj, dict)

    def is_set(self) -> bool:
        return isinstance(self.__obj, set)

    def is_bool(self) -> bool:
        return isinstance(self.__obj, bool)

    def is_none(self) -> bool:
        return self.__obj is None

    def is_bytes(self) -> bool:
        return isinstance(self.__obj, bytes)

    def is_bytearray(self) -> bool:
        return isinstance(self.__obj, bytearray)

    def is_memoryview(self) -> bool:
        return isinstance(self.__obj, memoryview)

    def is_map(self) -> bool:
        return isinstance(self.__obj, map)


class none:
    def __repr__(self) -> str:
        return "None"

    def __str__(self) -> str:
        return "None"


class Null:
    __value = "null"

    def __init__(self, value: Any | None = None) -> None: ...

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        raise ValueError("'null' object cannot be set to a value like {}".format(value))

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return "null"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


null: Null = Null()()


class Expr:
    r"""
    # Expr
    ## Usage

    If you want to solve for x, type in one of the following:
    >>> print(Expr("x**2", value=4)(solve=True))
    or:
    >>> print(Expr(("x**2", 4))(solve=True))
    """

    def __init__(
        self,
        expr: str | tuple[str, str | int | float],
        *,
        value: int | float | None = None,
        **kwds: Any,
    ) -> None:
        if type(expr) == str:
            self.__expr = expr
        elif type(expr) == tuple:
            if len(expr) == 2:
                self.__expr = expr[0]
                self.__val = expr[1]
            else:
                raise
        if (
            kwds.get("value", None) is not None
            and ises(kwds.get("value", None)).is_bool()
            and value == None
        ):
            self.__val = kwds.get("value", None)
        else:
            self.__val = value
        self.__call = False

    @property
    def expr(self):
        return self.__expr

    @expr.setter
    def expr(self, value):
        raise ValueError("Cannot change the expression given.")

    @property
    def value(self):
        """The value property."""
        return self.__val

    @value.setter
    def value(self, value):
        raise ValueError("Cannot change the value of the expression given.")

    def __repr__(self) -> str:
        if not self.__call:
            return f"{self.__expr} = {self.__val}"

    def __str__(self) -> str:
        if not self.__call:
            if self.__val != None:
                return f"{self.__expr} = {self.__val}"
            else:

    def __eval__(self):
        return self.__call__()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        def evaluate(expression: list):
            # Evaluate expression
            result = expression.pop(0)
            while expression:
                operator = expression.pop(0)
                operand = expression.pop(0)
                temp_result = 0
                if operator == "+":
                    temp_result = result + operand
                elif operator == "-":
                    temp_result = result - operand
                elif operator == "*":
                    if operand == "*":
                        operand = expression.pop(0)
                        temp_result = result**operand
                    else:
                        temp_result = result * operand
                elif operator == "/":
                    temp_result = result / operand
                result = temp_result
            return result

        if (
            kwds.get("solve", None) is not None
            and ises(kwds.get("solve", None)).is_bool()
        ):
            if kwds["solve"] == True:

                # Split the expression into individual characters
                elements: list[str] = []
                current_element = ""
                for char in self.expr:
                    if char.isdigit() or char == ".":
                        current_element += char
                    elif char in {"+", "-", "*", "/", "(", ")"}:
                        if current_element:
                            elements.append(current_element)
                            current_element = ""
                        elements.append(char)
                if current_element:
                    elements.append(current_element)

                # Stack to store numbers and operators within brackets
                stack = []
                # Iterate over the elements
                for element in elements:
                    if element.isdigit() or "." in element:
                        stack.append(float(element))
                    elif element in {"+", "-", "*", "/"}:
                        stack.append(element)
                    elif element == "(":
                        stack.append(element)
                    elif element == ")":
                        # Evaluate expressions within brackets
                        temp = []
                        while stack[-1] != "(":
                            temp.append(stack.pop())
                        stack.pop()  # Remove '('
                        temp.reverse()
                        stack.append(evaluate(temp))

                # Evaluate the remaining expression
                return evaluate(stack)


print(Expr("2**3*2"))
