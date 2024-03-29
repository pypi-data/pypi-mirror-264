from typing import Optional, Dict, Any


class Context:
    """
    Represents the context in which a piece of code is executed.

    Attributes:
        display_name (str): The name to display for the context, usually indicating the name of the code block.
        parent (Context, optional): The parent context in the hierarchy, if any.
        parent_entry_pos (Position, optional): The position where the parent context was entered.
        symbol_table (dict, optional): The symbol table containing variable names and their corresponding values.
    """

    def __init__(self, display_name: str, parent: Optional['Context'] = None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: Optional[Dict[str, Any]] = None
