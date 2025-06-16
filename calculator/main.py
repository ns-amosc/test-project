#!/usr/bin/env python3
"""
Simple calculator module
Provides basic mathematical operations
"""


def add(a, b):
    """Addition operation"""
    return a + b


def subtract(a, b):
    """Subtraction operation"""
    return a - b


def multiply(a, b):
    """Multiplication operation"""
    return a * b


def divide(a, b):
    """Division operation"""
    if b == 0:
        raise ValueError("Divisor cannot be zero")
    return a / b


def main():
    """Main program - execute some example calculations"""
    print("🧮 Simple Calculator Example")

    # Execute some example calculations
    result1 = add(10, 5)
    print(f"10 + 5 = {result1}")

    result2 = subtract(10, 3)
    print(f"10 - 3 = {result2}")

    result3 = multiply(4, 6)
    print(f"4 * 6 = {result3}")

    result4 = divide(15, 3)
    print(f"15 / 3 = {result4}")

    print("✅ All calculations completed!")
    return True


if __name__ == "__main__":
    main()