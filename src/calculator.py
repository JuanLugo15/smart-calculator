from __future__ import annotations

import ast
import operator
from dataclasses import dataclass


class CalculationError(ValueError):
    """Raised when an expression cannot be safely calculated."""


_BINARY_OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Mod: operator.mod, ast.Pow: operator.pow}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def evaluate_expression(expression: str) -> float | int:
    """Evaluate arithmetic syntax while rejecting all non-arithmetic AST nodes."""
    if not expression or not expression.strip():
        raise CalculationError("Expression cannot be empty")
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate_node(tree.body)
    except (SyntaxError, TypeError, OverflowError) as exc:
        raise CalculationError("Invalid arithmetic expression") from exc
    if isinstance(result, complex) or not isinstance(result, (int, float)):
        raise CalculationError("Expression must resolve to a real number")
    return result


def _evaluate_node(node: ast.AST) -> float | int:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        if isinstance(node.op, (ast.Div, ast.Mod)) and right == 0:
            raise CalculationError("Cannot divide by zero")
        try:
            return _BINARY_OPERATORS[type(node.op)](left, right)
        except (ZeroDivisionError, OverflowError) as exc:
            raise CalculationError("Arithmetic operation failed") from exc
    raise CalculationError("Only arithmetic operations are allowed")


@dataclass(frozen=True)
class Calculation:
    expression: str
    result: float | int


class Calculator:
    def __init__(self) -> None:
        self._history: list[Calculation] = []
        self._memory: float | int = 0

    def calculate(self, expression: str) -> float | int:
        result = evaluate_expression(expression)
        self._history.append(Calculation(expression.strip(), result))
        return result

    def history(self) -> tuple[Calculation, ...]:
        return tuple(self._history)

    def memory_add(self, value: float | int) -> None:
        self._memory += value

    def memory_subtract(self, value: float | int) -> None:
        self._memory -= value

    def memory_recall(self) -> float | int:
        return self._memory

    def memory_clear(self) -> None:
        self._memory = 0
