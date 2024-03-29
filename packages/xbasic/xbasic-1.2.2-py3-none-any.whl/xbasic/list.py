from .value import Value
from .number import Number
from .error_handler.rterror import RTError


class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        """
        Add an element to the list.

        Args:
        - other (Any): The element to be added.

        Returns:
        - Tuple[Union['List', None], Union[RTError, None]]: A tuple containing the new list and any potential error.
        """
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        """
        Remove an element from the list.

        Args:
        - other (Any): The element to be removed.

        Returns:
        - Tuple[Union['List', None], Union[RTError, None]]: A tuple containing the new list and any potential error.
        """
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        """
        Concatenate the list with another list.

        Args:
        - other (Any): The list to concatenate.

        Returns:
        - Tuple[Union['List', None], Union[RTError, None]]: A tuple containing the new list and any potential error.
        """
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        """
        Retrieve an element from the list.

        Args:
        - other (Any): The index of the element to retrieve.

        Returns:
        - Tuple[Union[Any, None], Union[RTError, None]]: A tuple containing the retrieved element and any potential error.
        """
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self) -> 'List':
        """
        Create a copy of the list.

        Returns:
        - 'List': A copy of the list.
        """
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self) -> str:
        """
        Convert the list to a string.

        Returns:
        - str: The string representation of the list.
        """
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self) -> str:
        """
        Get the string representation of the list.

        Returns:
        - str: The string representation of the list.
        """
        return f'[{", ".join([repr(x) for x in self.elements])}]'
