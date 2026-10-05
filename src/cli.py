from __future__ import annotations

import argparse

from .calculator import CalculationError, Calculator


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a safe arithmetic expression")
    parser.add_argument("expression", nargs="?", help='Example: "(12 + 8) / 4"')
    args = parser.parse_args()
    calculator = Calculator()
    expression = args.expression or input("Expression: ")
    try:
        print(calculator.calculate(expression))
    except CalculationError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
