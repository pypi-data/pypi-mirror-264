class ParseResult:
    def __init__(self):
        """
        Represents the result of a parsing operation.

        Attributes:
            error (Error): The error encountered during parsing, if any.
            node: The resulting node of the parsing operation.
            last_registered_advance_count (int): The count of advances registered during the last parsing step.
            advance_count (int): The total count of advances registered during parsing.
            to_reverse_count (int): The count of advances to reverse in case of failure.
        """
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        """Registers an advancement in parsing."""
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        """
        Registers the result of a parsing operation.

        Args:
            res (ParseResult): The result of the parsing operation to register.

        Returns:
            The resulting node of the parsing operation.
        """
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        """
        Tries to register the result of a parsing operation, handling errors.

        Args:
            res (ParseResult): The result of the parsing operation to try to register.

        Returns:
            The resulting node of the parsing operation if successful, otherwise None.
        """
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node) -> 'ParseResult':
        """
        Marks the parsing operation as successful.

        Args:
            node: The resulting node of the successful parsing operation.

        Returns:
            The current ParseResult instance.
        """
        self.node = node
        return self

    def failure(self, error) -> 'ParseResult':
        """
        Marks the parsing operation as failed.

        Args:
            error (Error): The error encountered during parsing.

        Returns:
            The current ParseResult instance.
        """
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self
