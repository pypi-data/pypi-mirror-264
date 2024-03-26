class Calculator:
  """
  A simple calculator class that can perform basic arithmetic operations, 
  nth root, and has memory functionality.
  """
  def __init__(self):
    self.memory = 0

  def add(self, num):
    """
    Adds a number to the calculator's memory.

    Args:
      num: The number to add.

    Returns:
      The sum of the current memory and the added number.
    """
    self.memory += num
    return self.memory

  def subtract(self, num):
    """
    Subtracts a number from the calculator's memory.

    Args:
      num: The number to subtract.

    Returns:
      The difference of the current memory and the subtracted number.
    """
    self.memory -= num
    return self.memory

  def multiply(self, num):
    """
    Multiplies the calculator's memory by a number.

    Args:
      num: The number to multiply.

    Returns:
      The product of the current memory and the multiplied number.
    """
    self.memory *= num
    return self.memory

  def divide(self, num):
    """
    Divides the calculator's memory by a number (handles division by zero).

    Args:
      num: The number to divide by.

    Returns:
      The quotient of the current memory and the divided number, 
      or None if division by zero occurs.
    """
    if num == 0:
      return None
    self.memory /= num
    return self.memory

  def nth_root(self, n):
    """
    Calculates the nth root of the calculator's memory.

    Args:
      n: The root to be calculated.

    Returns:
      The nth root of the current memory.
    """
    import math
    self.memory = math.pow(self.memory, 1/n)
    return self.memory

  def reset(self):
    """
    Resets the calculator's memory to 0.
    """
    self.memory = 0

