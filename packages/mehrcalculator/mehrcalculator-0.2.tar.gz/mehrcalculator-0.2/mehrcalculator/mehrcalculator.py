import math
from typing import Union

class Calculator:
  """
  A simple calculator class that can perform basic arithmetic operations, 
  nth root, and has memory functionality.
  """
  def __init__(self) -> None:
    self.memory: float = 0

  def add(self, num: float) -> float:
    """
    Adds a number to the calculator's memory.
    """
    self.memory += num
    return self.memory

  def subtract(self, num: float) -> float:
    """
    Subtracts a number from the calculator's memory.
    """
    self.memory -= num
    return self.memory

  def multiply(self, num: Union[int, float]) -> float:
    """
    Multiplies the calculator's memory by a number. Raises TypeError if num is not a number.
    """
    if not isinstance(num, (int, float)):
        raise TypeError("num must be an integer or float")
    self.memory *= num
    return self.memory

  def divide(self, num: float) -> float:
    """
    Divides the calculator's memory by a number (handles division by zero).
    """
    if num == 0:
      raise ValueError("division by zero is not supported")
    self.memory /= num
    return self.memory

  def nth_root(self, n: float) -> float:
    """
    Calculates the nth root of the calculator's memory. Handles negative values for even roots.
    """
    if self.memory < 0 and n % 2 == 0:
      raise ValueError("Cannot calculate an even root for negative numbers.")
    self.memory = math.pow(self.memory, 1/n)
    return self.memory

  def reset(self) -> None:
    """
    Resets the calculator's memory to 0.
    """
    self.memory = 0
    