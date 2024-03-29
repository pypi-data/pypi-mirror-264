from .error import Error


class RTError(Error):
    """
    Represents a runtime error that occurs during code execution.

    Attributes:
        pos_start (Position): The start position of the error.
        pos_end (Position): The end position of the error.
        details (str): Details about the error.
        context (Context): The context in which the error occurred.
    """

    def __init__(self, pos_start, pos_end, details: str, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self) -> str:
        """
        Returns a string representation of the error.

        Returns:
            str: The string representation of the error.
        """

        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'

        from .string_with_arrows import string_with_arrows
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self) -> str:
        """
        Generates a traceback for the error.

        Returns:
            str: The generated traceback.
        """

        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result
