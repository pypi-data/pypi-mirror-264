
# Mehr Calculator Package

The Mehr Calculator Package provides a simple yet powerful calculator class capable of performing basic arithmetic operations, taking nth roots, and maintaining a memory state. Designed with ease of use and extensibility in mind, it's perfect for educational purposes, quick mathematical operations within Python projects, and as a base for more complex calculator applications.

## Installation

To install Mehr Calculator, use pip:

```bash
pip install mehrcalculator
```

Ensure that you have Python 3.6 or newer installed.

## Usage

Here's how to use the Mehr Calculator:

```python
from mehrcalculator.mehrcalculator import Calculator

calc = Calculator()
print(calc.add(5))  # Adds 5 to the memory
print(calc.multiply(2))  # Multiplies the memory by 2
print(calc.nth_root(2))  # Calculates the square root of the memory
calc.reset()  # Resets the memory to 0
```

## Features

- Perform basic arithmetic operations: Addition, Subtraction, Multiplication, Division.
- Calculate the nth root of a number.
- Memory functionality for sequential calculations.


## License

Distributed under the MIT License. See `LICENSE` for more information.

## Support

For support, email ramin.mehr@gmail.com or open an issue on GitHub.
```
