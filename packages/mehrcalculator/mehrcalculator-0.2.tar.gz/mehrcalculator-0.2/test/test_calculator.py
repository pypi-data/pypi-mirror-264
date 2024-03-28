import unittest
from mehrcalculator.mehrcalculator import Calculator

class TestCalculator(unittest.TestCase):

    def test_addition(self):
        calc = Calculator()
        self.assertEqual(calc.add(2), 2)

    def test_subtraction(self):
        calc = Calculator()
        calc.add(10)  # Set memory to 10
        self.assertEqual(calc.subtract(5), 5)

    def test_multiplication_with_negative(self):
        calc = Calculator()
        calc.add(5)
        self.assertEqual(calc.multiply(-2), -10)  # Multiply by a negative number

    def test_division_by_zero(self):
        calc = Calculator()
        calc.add(20)
        with self.assertRaises(ValueError):
            calc.divide(0)  # Division by zero should raise ValueError

    def test_nth_root_of_negative(self):
        calc = Calculator()
        calc.add(-8)  # Set memory to -8
        with self.assertRaises(ValueError):
            calc.nth_root(3)  # Cubic root of -8 is allowed and should be -2

    def test_multiply_with_non_numeric(self):
        calc = Calculator()
        with self.assertRaises(TypeError):
            calc.multiply("string")  # Attempt to multiply by a non-numeric type

    def test_reset(self):
        calc = Calculator()
        calc.add(50)  # Set memory to 50
        calc.reset()
        self.assertEqual(calc.memory, 0)  # Memory should be reset to 0

if __name__ == '__main__':
    unittest.main()
