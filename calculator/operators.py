#!/usr/bin/env python3
"""
Simple operator module
Provides basic mathematical operations
"""


class Operators:
    """Calculator class with basic mathematical operations"""

    @staticmethod
    def add(a, b):
        """Addition operation"""
        return a + b

    @staticmethod
    def subtract(a, b):
        """Subtraction operation"""
        return a - b

    @staticmethod
    def multiply(a, b):
        """Multiplication operation"""
        return a * b

    @staticmethod
    def divide(a, b):
        """Division operation"""
        if b == 0:
            raise ValueError("Divisor cannot be zero")
        return a / b
