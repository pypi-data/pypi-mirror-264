class Position:
    def __init__(self, idx: int, ln: int, col: int, fn: str, ftxt: str):
        """
        Represents a position in the source code.

        Args:
            idx (int): The index of the position.
            ln (int): The line number of the position.
            col (int): The column number of the position.
            fn (str): The name of the file.
            ftxt (str): The full text of the file.
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None) -> 'Position':
        """
        Advances the position to the next character.

        Args:
            current_char (str, optional): The current character. Defaults to None.

        Returns:
            Position: The updated Position object.
        """
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self) -> 'Position':
        """
        Creates a copy of the current position.

        Returns:
            Position: The copied Position object.
        """
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
