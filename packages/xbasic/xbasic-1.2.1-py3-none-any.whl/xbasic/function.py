from .value import Value
from .error_handler.rterror import RTError
from .error_handler.rtresult import RTResult


class BaseFunction(Value):
    def __init__(self, name: str):
        """
        Initialize a BaseFunction object with a name.

        Args:
            name (str): The name of the function.
        """
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        """
        Generate a new context for the function.

        Returns:
            Context: The newly generated context.
        """
        from .context_handler.context import Context
        from .context_handler.symbol_table import SymbolTable

        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names: list, args: list):
        """
        Check if the correct number of arguments are passed.

        Args:
            arg_names (List[str]): List of argument names.
            args (List[Value]): List of arguments.

        Returns:
            RTResult: The result of the argument check.
        """
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))

        return res.success(None)

    @staticmethod
    def populate_args(arg_names: list, args: list, exec_ctx):
        """
        Populate the arguments in the symbol table of the execution context.

        Args:
            arg_names (List[str]): List of argument names.
            args (List[Value]): List of arguments.
            exec_ctx (Context): The execution context.
        """
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names: list, args: list, exec_ctx):
        """
        Check the arguments and populate them in the symbol table of the execution context.

        Args:
            arg_names (List[str]): List of argument names.
            args (List[Value]): List of arguments.
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of checking and populating arguments.
        """
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return():
            return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)


class Function(BaseFunction):
    def __init__(self, name: str, body_node, arg_names: list, should_auto_return: bool):
        """
        Initialize a Function object with name, body node, argument names, and auto return flag.

        Args:
            name (str): The name of the function.
            body_node: The body node of the function.
            arg_names (List[str]): List of argument names.
            should_auto_return (bool): Whether the function should automatically return.
        """
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args: list):
        """
        Execute the function with the given arguments.

        Args:
            args (List[Value]): The arguments to pass to the function.

        Returns:
            RTResult: The result of executing the function.
        """
        res = RTResult()

        from .Interpreter import Interpreter
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value is None:
            return res

        from .number import Number
        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)

    def copy(self) -> 'Function':
        """
        Create a copy of the function.

        Returns:
            Function: The copy of the function.
        """
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self) -> str:
        """
        Get the string representation of the function.

        Returns:
            str: The string representation of the function.
        """
        return f"<function {self.name}>"
