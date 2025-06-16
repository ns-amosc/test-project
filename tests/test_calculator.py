import unittest

from calculator.main import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):
    """Test cases for calculator functions"""
    def test_add_positive_numbers(self):
        """Test addition with positive numbers"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(10, 15), 25)
    def test_add_negative_numbers(self):
        """Test addition with negative numbers"""
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-5, -3), -8)
    def test_add_decimal_numbers(self):
        """Test addition with decimal numbers"""
        self.assertAlmostEqual(add(2.5, 3.7), 6.2)
        self.assertAlmostEqual(add(-1.5, 3.8), 2.3)
    def test_subtract_basic(self):
        """Test basic subtraction"""
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(10, 7), 3)
    def test_multiply_basic(self):
        """Test basic multiplication"""
        self.assertEqual(multiply(4, 3), 12)
        self.assertEqual(multiply(2, 5), 10)
    def test_multiply_with_zero(self):
        """Test multiplication with zero"""
        self.assertEqual(multiply(5, 0), 0)
        self.assertEqual(multiply(0, 3), 0)
    def test_divide_basic(self):
        """Test basic division"""
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(divide(15, 3), 5.0)
    def test_divide_by_zero_raises_exception(self):
        """Test that division by zero raises ValueError"""
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Divisor cannot be zero")
    def test_divide_negative_numbers(self):
        """Test division with negative numbers"""
        self.assertEqual(divide(-10, 2), -5.0)
        self.assertEqual(divide(10, -2), -5.0)

if __name__ == '__main__':
    unittest.main()
