from .function import BaseFunction
from .error_handler.rtresult import RTResult
import os
from .number import Number
from .string_value import String
from .list import List
from .error_handler.rterror import RTError


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args: list):
        """
        Execute the built-in function with the given arguments.

        Args:
            args (list): List of arguments passed to the function.

        Returns:
            RTResult: The result of executing the function.
        """
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        """
        Handle cases where no method is defined for the built-in function.

        Args:
            node: The node being visited.
            context: The current context.

        Raises:
            Exception: When no method is defined for the built-in function.
        """
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self) -> 'BuiltInFunction':
        """
        Create a copy of the built-in function.

        Returns:
            BuiltInFunction: The copied built-in function.
        """
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self) -> str:
        """
        Get the string representation of the built-in function.

        Returns:
            str: The string representation of the built-in function.
        """
        return f"<built-in function {self.name}>"

    #####################################

    def execute_print(self, exec_ctx):
        """
        Execute the built-in print function.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the print function.
        """
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)

    execute_print.arg_names = ['value']

    def execute_print_ret(self, exec_ctx):
        """
        Execute the built-in print_ret function.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the print_ret function.
        """
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))

    execute_print_ret.arg_names = ['value']

    def execute_input(self, exec_ctx):
        """
        Execute the built-in input function.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the input function.
        """
        text = input()
        return RTResult().success(String(text))

    execute_input.arg_names = []

    def execute_input_int(self, exec_ctx):
        """
        Execute the built-in input_int function, which prompts the user to enter a number.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the input_int function.
        """
        while True:
            text = input()
            try:
                number = float(text)
                break
            except ValueError:
                print(f"'{text}' must be a number. Try again!")
        return RTResult().success(Number(number))

    execute_input_int.arg_names = []

    def execute_clear(self, exec_ctx):
        """
        Execute the built-in clear function, which clears the console screen.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the clear function.
        """
        os.system('clear' if os.name == 'nt' else 'clear')
        return RTResult().success(Number.null)

    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        """
        Execute the built-in is_number function, which checks if the provided value is a number.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the is_number function.
        """
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)

    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        """
        Execute the built-in is_string function, which checks if the provided value is a string.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the is_string function.
        """
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_string else Number.false)

    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        """
        Execute the built-in is_list function, which checks if the provided value is a list.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the is_list function.
        """
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_list else Number.false)

    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        """
        Execute the built-in is_function function, which checks if the provided value is a function.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the is_function function.
        """
        is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_function else Number.false)

    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        """
        Execute the built-in append function, which appends a value to a list.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the append function.
        """
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        list_.elements.append(value)
        return RTResult().success(Number.null)

    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        """
        Execute the built-in pop function, which removes and returns an element from a list at the specified index.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the pop function.
        """
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)

    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        """
        Execute the built-in extend function, which extends one list by appending all the items from another list.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the extend function.
        """
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(Number.null)

    execute_extend.arg_names = ["listA", "listB"]

    def execute_len(self, exec_ctx):
        """
        Execute the built-in len function, which returns the length of a list.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the len function.
        """
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be list",
                exec_ctx
            ))

        return RTResult().success(Number(len(list_.elements)))

    execute_len.arg_names = ["list"]

    def execute_run(self, exec_ctx):
        """
        Execute the built-in run function, which executes an external XBasic script.

        Args:
            exec_ctx (Context): The execution context.

        Returns:
            RTResult: The result of executing the run function.
        """
        fn = exec_ctx.symbol_table.get("fn")

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\". Error: {str(e)}",
                exec_ctx
            ))

        from .init_interp import run
        _, error = run(fn, script)

        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing script \"{fn}\". Error: {error.as_string()}",
                exec_ctx
            ))

        return RTResult().success(Number.null)

    execute_run.arg_names = ["fn"]


BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.print_ret = BuiltInFunction("print_ret")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.run = BuiltInFunction("run")
