from typing import List, Optional, Union, TYPE_CHECKING
from .position import Position
from .token import Token

class NumberNode:
    def __init__(self, tok):
        """
        Represents a number node in the abstract syntax tree (AST).

        Args:
            tok (Token): The token representing the number.
        """
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class StringNode:
    def __init__(self, tok):
        """
        Represents a string node in the abstract syntax tree (AST).

        Args:
            tok (Token): The token representing the string.
        """
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class ListNode:
    def __init__(self, element_nodes: List[Union[NumberNode, StringNode]], pos_start: Position, pos_end: Position):
        """
        Represents a list node in the abstract syntax tree (AST).

        Args:
            element_nodes (list): List of element nodes.
            pos_start (Position): The start position of the list.
            pos_end (Position): The end position of the list.
        """
        self.element_nodes: List[Union[NumberNode, StringNode]] = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end


class VarAccessNode:
    def __init__(self, var_name_tok):
        """
        Represents a variable access node in the abstract syntax tree (AST).

        Args:
            var_name_tok (Token): The token representing the variable name.
        """
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarAssignNode:
    def __init__(self, var_name_tok, value_node: Union[NumberNode, StringNode, ListNode], dtype: str):
        """
        Represents a variable assignment node in the abstract syntax tree (AST).

        Args:
            var_name_tok (Token): The token representing the variable name.
            value_node: The value assigned to the variable.
            dtype: The data type of the variable.
        """
        self.var_name_tok = var_name_tok
        self.value_node: Union[NumberNode, StringNode, ListNode] = value_node
        self.dtype: str = dtype

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


class BinOpNode:
    def __init__(self, left_node: Union[NumberNode, StringNode], op_tok, right_node: Union[NumberNode, StringNode]):
        """
        Represents a binary operation node in the abstract syntax tree (AST).

        Args:
            left_node: The left operand node.
            op_tok (Token): The token representing the operator.
            right_node: The right operand node.
        """
        self.left_node: Union[NumberNode, StringNode] = left_node
        self.op_tok = op_tok
        self.right_node: Union[NumberNode, StringNode] = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        """
        Represents a unary operation node in the abstract syntax tree (AST).

        Args:
            op_tok (Token): The token representing the operator.
            node: The operand node.
        """
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class IfNode:
    def __init__(self, cases, else_case):
        """
        Represents an if statement node in the abstract syntax tree (AST).

        Args:
            cases (list): List of if-else case tuples.
            else_case: The else case node.
        """
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end


class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node,
                 should_return_null: bool):
        """
        Represents a for loop node in the abstract syntax tree (AST).

        Args:
            var_name_tok (Token): The token representing the loop variable name.
            start_value_node: The start value node of the loop.
            end_value_node: The end value node of the loop.
            step_value_node: The step value node of the loop.
            body_node: The body node of the loop.
            should_return_null (bool): Whether the loop should return null.
        """
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end


class WhileNode:
    def __init__(self, condition_node, body_node, should_return_null: bool):
        """
        Represents a while loop node in the abstract syntax tree (AST).

        Args:
            condition_node: The condition node of the loop.
            body_node: The body node of the loop.
            should_return_null (bool): Whether the loop should return null.
        """
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end


class FuncDefNode:
    def __init__(self, var_name_tok: Token, arg_name_toks: list, body_node, should_auto_return: bool):
        """
        Represents a function definition node in the abstract syntax tree (AST).

        Args:
            var_name_tok (Token): The token representing the function name.
            arg_name_toks (list): List of tokens representing argument names.
            body_node: The body node of the function.
            should_auto_return (bool): Whether the function should auto return.
        """
        self.var_name_tok: Token = var_name_tok
        self.arg_name_toks: list = arg_name_toks
        self.body_node = body_node
        self.should_auto_return: bool = should_auto_return
        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end


class CallNode:
    def __init__(self, node_to_call, arg_nodes: list):
        """
        Represents a function call node in the abstract syntax tree (AST).

        Args:
            node_to_call: The node representing the function to call.
            arg_nodes (list): List of argument nodes.
        """
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start
        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end


class ReturnNode:
    def __init__(self, node_to_return, pos_start: Position, pos_end: Position):
        """
        Represents a return statement node in the abstract syntax tree (AST).

        Args:
            node_to_return: The node to return.
            pos_start (Position): The start position of the return statement.
            pos_end (Position): The end position of the return statement.
        """
        self.node_to_return = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end


class ContinueNode:
    def __init__(self, pos_start: Position, pos_end: Position):
        """
        Represents a continue statement node in the abstract syntax tree (AST).

        Args:
            pos_start (Position): The start position of the continue statement.
            pos_end (Position): The end position of the continue statement.
        """
        self.pos_start = pos_start
        self.pos_end = pos_end


class BreakNode:
    def __init__(self, pos_start: Position, pos_end: Position):
        """
        Represents a break statement node in the abstract syntax tree (AST).

        Args:
            pos_start (Position): The start position of the break statement.
            pos_end (Position): The end position of the break statement.
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
