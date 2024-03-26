import unittest
from calculator.mehr.calculator import Calculator

class TestCalculator(unittest.TestCase):

    def test_addition(self):
        calc = Calculator()
        self.assertEqual(calc.add(2), 2)

    def test_subtraction(self):
        calc = Calculator()
        calc.add(10)  # Set memory to 10
        self.assertEqual(calc.subtract(5), 5)

    # Include tests for multiply, divide, root, reset

if __name__ == '__main__':
    unittest.main()
