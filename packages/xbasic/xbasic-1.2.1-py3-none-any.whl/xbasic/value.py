from typing import Optional
from .utils.position import Position
from .context_handler.context import Context
from .error_handler.rterror import RTError


class Value:
    def __init__(self) -> None:
        """
        Represents a generic value in the interpreter.
        """
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start: Optional[Position] = None, pos_end: Optional[Position] = None) -> 'Value':
        """
        Sets the position of the value.

        Args:
            pos_start (Optional[Position]): The start position of the value.
            pos_end (Optional[Position]): The end position of the value.

        Returns:
            Value: The instance of the value.
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context: Optional[Context] = None) -> 'Value':
        """
        Sets the context of the value.

        Args:
            context (Optional[Context]): The context of the value.

        Returns:
            Value: The instance of the value.
        """
        self.context = context
        return self

    def added_to(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def subbed_by(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def multed_by(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def dived_by(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def powed_by(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def anded_by(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def ored_by(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def notted(self, other) -> tuple[Optional['Value'], RTError]:
        return None, self.illegal_operation(other)

    def execute(self, args: list):
        """
        Executes the value with the given arguments.

        Args:
            args (list): The arguments to be passed to the value.

        Returns:
            RTResult: The result of the execution.
        """
        from .error_handler.rtresult import RTResult
        return RTResult().failure(self.illegal_operation())

    def copy(self) -> None:
        """
        Raises an exception indicating that no copy method is defined for the value.
        """
        raise Exception('No copy method defined')

    def is_true(self) -> bool:
        """
        Check if the value is considered true.

        Returns:
            bool: True if the value is considered true, False otherwise.
        """
        return False

    def illegal_operation(self, other: Optional['Value'] = None) -> RTError:
        """
        Raises an error for an illegal operation.

        Args:
            other (Optional[Value]): Another value involved in the operation.

        Returns:
            RTError: The runtime error indicating the illegal operation.
        """
        if not other:
            other = self

        from .error_handler.rterror import RTError
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )
