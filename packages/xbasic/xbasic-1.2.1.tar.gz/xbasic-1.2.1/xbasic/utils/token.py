class Token:
    def __init__(self, type_: str, value=None, pos_start=None, pos_end=None):
        """
        Represents a token in the source code.

        Args:
            type_ (str): The type of the token.
            value (str, optional): The value of the token. Defaults to None.
            pos_start (Position, optional): The starting position of the token. Defaults to None.
            pos_end (Position, optional): The ending position of the token. Defaults to None.
        """
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_: str, value) -> bool:
        """
        Checks if the token matches the given type and value.

        Args:
            type_ (str): The type to match.
            value: The value to match.

        Returns:
            bool: True if the token matches, False otherwise.
        """
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        """
        Returns a string representation of the token.

        Returns:
            str: The string representation of the token.
        """
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
