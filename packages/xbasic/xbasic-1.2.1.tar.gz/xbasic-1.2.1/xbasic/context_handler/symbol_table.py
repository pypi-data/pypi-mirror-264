from typing import Optional, Dict, Any


class SymbolTable:
    """
    Represents a symbol table that stores variables and their values.

    Attributes:
        symbols (dict): A dictionary mapping variable names to their values.
        parent (SymbolTable, optional): The parent symbol table in the scope hierarchy.
    """

    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.symbols: Dict[str, Any] = {}
        self.parent: Optional['SymbolTable'] = parent

    def get(self, name: str) -> Any:
        """
        Retrieves the value associated with a variable name from the symbol table.

        Args:
            name (str): The name of the variable.

        Returns:
            Any: The value associated with the variable, or None if not found.
        """

        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name: str, value: Any):
        """
        Sets the value of a variable in the symbol table.

        Args:
            name (str): The name of the variable.
            value (Any): The value to assign to the variable.
        """

        self.symbols[name] = value

    def remove(self, name: str):
        """
        Removes a variable from the symbol table.

        Args:
            name (str): The name of the variable to remove.
        """

        del self.symbols[name]
