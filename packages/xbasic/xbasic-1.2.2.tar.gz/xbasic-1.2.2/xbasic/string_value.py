from .value import Value
from .number import Number


class String(Value):
    def __init__(self, value: str):
        """
        Represents a string value in the interpreter.

        Args:
            value (str): The string value.
        """
        super().__init__()
        self.value = value

    def added_to(self, other: 'String'):
        """
        Adds this string to another string.

        Args:
            other (String): The other string to add.

        Returns:
            tuple: A tuple containing the result of the addition and None.
        """
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def multed_by(self, other: Number):
        """
        Multiplies this string by a number.

        Args:
            other (Number): The number to multiply.

        Returns:
            tuple: A tuple containing the result of the multiplication and None.
        """
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def is_true(self) -> bool:
        """
        Checks if the string is considered as True.

        Returns:
            bool: True if the string is not empty, False otherwise.
        """
        return len(self.value) > 0

    def copy(self) -> 'String':
        """
        Creates a copy of this string.

        Returns:
            String: The copied string.
        """
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self) -> str:
        """
        Returns the string representation of this string.

        Returns:
            str: The string value.
        """
        return self.value

    def __repr__(self) -> str:
        """
        Returns the representation of this string.

        Returns:
            str: The representation of the string.
        """
        return f'"{self.value}"'
