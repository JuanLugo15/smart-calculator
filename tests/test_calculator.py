import unittest

from src.calculator import CalculationError, Calculator, evaluate_expression


class CalculatorTests(unittest.TestCase):
    def test_supports_parentheses_and_operator_precedence(self):
        self.assertEqual(evaluate_expression("(12 + 8) / 4"), 5)
        self.assertEqual(evaluate_expression("2 ** 3 + 4"), 12)

    def test_rejects_unsafe_syntax(self):
        with self.assertRaises(CalculationError):
            evaluate_expression("__import__('os').system('echo unsafe')")

    def test_reports_division_by_zero(self):
        with self.assertRaises(CalculationError):
            evaluate_expression("10 / 0")

    def test_keeps_immutable_history_and_memory(self):
        calculator = Calculator()
        self.assertEqual(calculator.calculate("4 * 5"), 20)
        calculator.memory_add(20)
        calculator.memory_subtract(5)
        self.assertEqual(calculator.memory_recall(), 15)
        self.assertEqual(len(calculator.history()), 1)


if __name__ == "__main__":
    unittest.main()
