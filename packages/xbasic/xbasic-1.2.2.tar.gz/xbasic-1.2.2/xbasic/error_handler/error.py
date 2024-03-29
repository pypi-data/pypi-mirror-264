class Error:
    """
        Represents an error that occurred during code execution.

        Attributes:
            pos_start (Position): The starting position of the error.
            pos_end (Position): The ending position of the error.
            error_name (str): The name of the error.
            details (str): Details about the error.
    """

    def __init__(self, pos_start, pos_end, error_name: str, details: str):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self) -> str:
        """
            Returns a string representation of the error.

            Returns:
                str: A formatted string containing information about the error.
        """

        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'

        from .string_with_arrows import string_with_arrows
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    """
        Represents an error raised when encountering an illegal character.

        Inherits from Error class.
    """

    def __init__(self, pos_start, pos_end, details: str):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    """
        Represents an error raised when an expected character is missing.

        Inherits from Error class.
    """

    def __init__(self, pos_start, pos_end, details: str):
        super().__init__(pos_start, pos_end, 'Expected Character', details)


class InvalidSyntaxError(Error):
    """
        Represents an error raised due to invalid syntax.

        Inherits from Error class.
    """

    def __init__(self, pos_start, pos_end, details: str = ''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
