from typing import Any
from .error import Error

class RTResult:
    """
    Represents the result of an operation during runtime.

    Attributes:
        value (any): The value produced by the operation.
        error (Error): The error, if any, that occurred during the operation.
        func_return_value (any): The value to be returned from a function, if applicable.
        loop_should_continue (bool): Indicates whether the loop should continue.
        loop_should_break (bool): Indicates whether the loop should break.
    """

    def __init__(self):
        """Initializes an RTResult object with default values."""
        self.reset()

    def reset(self):
        """Resets the RTResult object to its default state."""
        self.value: Any = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue: bool = False
        self.loop_should_break: bool = False

    def register(self, res: 'RTResult') -> Any:
        """
        Registers the result of another RTResult object.

        Args:
            res (RTResult): The RTResult object whose values are to be registered.

        Returns:
            any: The value from the registered RTResult object.
        """
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value: Any) -> 'RTResult':
        """
        Sets the result as successful with a specified value.

        Args:
            value (any): The value produced by the operation.

        Returns:
            RTResult: The RTResult object indicating success with the provided value.
        """
        self.reset()
        self.value = value
        return self

    def success_return(self, value: Any) -> 'RTResult':
        """
        Sets the result as successful with a specified return value.

        Args:
            value (any): The value to be returned from a function.

        Returns:
            RTResult: The RTResult object indicating success with the provided return value.
        """
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self) -> 'RTResult':
        """
        Sets the result as successful with a continue signal.

        Returns:
            RTResult: The RTResult object indicating success with a continue signal.
        """
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self) -> 'RTResult':
        """
        Sets the result as successful with a break signal.

        Returns:
            RTResult: The RTResult object indicating success with a break signal.
        """
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self, error) -> 'RTResult':
        """
        Sets the result as a failure with the specified error.

        Args:
            error (Error): The error that occurred during the operation.

        Returns:
            RTResult: The RTResult object indicating failure with the provided error.
        """
        self.reset()
        self.error = error
        return self

    def should_return(self) -> bool:
        """
        Checks if the operation should return.

        Returns:
            bool: True if the operation should return, False otherwise.
        """
        return (
                self.error or
                self.func_return_value or
                self.loop_should_continue or
                self.loop_should_break
        )
