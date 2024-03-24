from calculator import Calculator
import sys


class CalculatorCLI:
    def __init__(self, args, channel=sys.stdout):
        self._args = args
        self._calc = Calculator()
        self._channel = channel

    def _print(self, *args, **kwargs):
        print(*args, **kwargs, file=self._channel)

    def run(self):
        if not self._args:
            self._print("Usage: python -m calculator.ui.cli <expression>")
            return
        self._calc.expression = " ".join(self._args)
        try:
            result = self._calc.compute_result()
            self._print(result)
        except ValueError as e:
            self._print(e)


def start_app():
    CalculatorCLI(sys.argv[1:]).run()


if __name__ == '__main__':
    start_app()
