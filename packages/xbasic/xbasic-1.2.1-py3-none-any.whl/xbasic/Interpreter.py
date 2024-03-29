import xbasic.string_value
from .error_handler.rtresult import RTResult
from .utils.token_list import *
from .number import Number
from .list import List


class Interpreter:
    def visit(self, node, context):
        """
        Visit a node and execute it in the provided context.

        Args:
            node: The node to visit.
            context: The context in which to execute the node.

        Returns:
            RTResult: The result of executing the node.
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        """
        Handle cases where a visit method is not defined for a node.

        Args:
            node: The node for which the visit method is not defined.
            context: The context in which the node was being executed.

        Returns:
            RTResult: An RTResult with a failure indicating the lack of defined visit method.
        """
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    @staticmethod
    def visit_NumberNode(node, context):
        """
        Visit a NumberNode and evaluate its value.

        Args:
            node (NumberNode): The NumberNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the NumberNode.
        """
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    @staticmethod
    def visit_StringNode(node, context):
        """
        Visit a StringNode and evaluate its value.

        Args:
            node (StringNode): The StringNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the StringNode.
        """
        from .string_value import String
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        """
        Visit a ListNode and evaluate its elements.

        Args:
            node (ListNode): The ListNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the ListNode.
        """
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    @staticmethod
    def visit_VarAccessNode(node, context):
        """
        Visit a VarAccessNode and retrieve its value from the symbol table.

        Args:
            node (VarAccessNode): The VarAccessNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the VarAccessNode.
        """
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            from .error_handler.rterror import RTError
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        """
        Visit a VarAssignNode and assign a value to a variable in the symbol table.

        Args:
            node (VarAssignNode): The VarAssignNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the VarAssignNode.
        """
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return():
            return res

        from .lexer import Lexer
        obj = Lexer("fn", str(value))

        a = str(obj.make_tokens()).lower()
        if (("int" in a or "float" in a or "minus" in a) and "comma" not in a) and (str(node.dtype).lower() == "num"):
            context.symbol_table.set(var_name, value)
            return res.success(value)
        if isinstance(value, xbasic.string_value.String) and "comma" not in a:
            if str(node.dtype).lower() == "text":
                context.symbol_table.set(var_name, value)
                return res.success(value)
        if str(node.dtype).lower() == "list":
            if "comma" in a:
                context.symbol_table.set(var_name, value)
                return res.success(value)

        from .error_handler.rterror import RTError
        return res.failure(RTError(
            node.pos_start, node.pos_end,
            f"Error: no viable conversion from '{a}' to '{str(node.dtype).lower()}'",
            context
        ))

    def visit_BinOpNode(self, node, context):
        """
        Visit a BinOpNode and perform a binary operation.

        Args:
            node (BinOpNode): The BinOpNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the BinOpNode.
        """
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return():
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return():
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        """
        Visit a UnaryOpNode and perform a unary operation.

        Args:
            node (UnaryOpNode): The UnaryOpNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the UnaryOpNode.
        """
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return():
            return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        """
        Visit an IfNode and execute the corresponding block based on conditions.

        Args:
            node (IfNode): The IfNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the IfNode.
        """
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return():
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return():
                    return res
                return res.success(Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return():
                return res
            return res.success(Number.null if should_return_null else expr_value)

        return res.success(Number.null)

    def visit_ForNode(self, node, context):
        """
        Visit a ForNode and execute a loop over a range of values.

        Args:
            node (ForNode): The ForNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the ForNode.
        """
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return():
            return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return():
            return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return():
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue is False and res.loop_should_break is False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node, context):
        """
        Visit a WhileNode and execute a loop while a condition is true.

        Args:
            node (WhileNode): The WhileNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the WhileNode.
        """
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return():
                return res

            if not condition.is_true():
                break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue is False and res.loop_should_break is False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    @staticmethod
    def visit_FuncDefNode(node, context):
        """
        Visit a FuncDefNode and define a new function in the symbol table.

        Args:
            node (FuncDefNode): The FuncDefNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the FuncDefNode.
        """
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]

        from .function import Function
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(
            node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        """
        Visit a CallNode and execute a function call.

        Args:
            node (CallNode): The CallNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the CallNode.
        """
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return():
            return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return():
            return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        """
        Visit a ReturnNode and return a value from a function.

        Args:
            node (ReturnNode): The ReturnNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: The result of evaluating the ReturnNode.
        """
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Number.null

        return res.success_return(value)

    @staticmethod
    def visit_ContinueNode(node, context):
        """
        Visit a ContinueNode and signal a continue in a loop.

        Args:
            node (ContinueNode): The ContinueNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: An RTResult indicating a loop should continue.
        """
        return RTResult().success_continue()

    @staticmethod
    def visit_BreakNode(node, context):
        """
        Visit a BreakNode and signal a break in a loop.

        Args:
            node (BreakNode): The BreakNode to visit.
            context (Context): The context in which to execute the node.

        Returns:
            RTResult: An RTResult indicating a loop should break.
        """
        return RTResult().success_break()
