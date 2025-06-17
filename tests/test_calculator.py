import pytest
from calculator.operators import Operators


class TestOperators:
    def setup_method(self):
        self.ops = Operators()

    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 5),
        (10, 15, 25),
        (-1, 1, 0),
        (-5, -3, -8),
        (0, 0, 0),
        (100, -50, 50)
    ])
    def test_add_parametrized(self, a, b, expected):
        assert Operators.add(a, b) == expected

    @pytest.mark.parametrize("a, b, expected", [
        (5, 3, 2),
        (10, 7, 3),
        (0, 5, -5),
        (-3, -2, -1),
        (100, 100, 0)
    ])
    def test_subtract_parametrized(self, a, b, expected):
        assert Operators.subtract(a, b) == expected

    @pytest.mark.parametrize("a, b, expected", [
        (4, 3, 12),
        (2, 5, 10),
        (5, 0, 0),
        (0, 3, 0),
        (-2, 3, -6),
        (-2, -3, 6)
    ])
    def test_multiply_parametrized(self, a, b, expected):
        assert Operators.multiply(a, b) == expected

    @pytest.mark.parametrize("a, b, expected", [
        (10, 2, 5.0),
        (15, 3, 5.0),
        (-10, 2, -5.0),
        (10, -2, -5.0),
        (7, 2, 3.5),
        (1, 3, 0.3333333333333333)
    ])
    def test_divide_parametrized(self, a, b, expected):
        assert Operators.divide(a, b) == expected

    def test_divide_by_zero_raises_exception(self):
        with pytest.raises(ValueError) as excinfo:
            Operators.divide(10, 0)
        assert str(excinfo.value) == "Divisor cannot be zero"
        with pytest.raises(ValueError):
            Operators.divide(-5, 0)

    @pytest.mark.parametrize("divisor", [0, 0.0])
    def test_divide_by_zero_parametrized(self, divisor):
        with pytest.raises(ValueError, match="Divisor cannot be zero"):
            Operators.divide(10, divisor)


def test_multiple_operations():
    add_result = Operators.add(5, 3)
    assert add_result == 8

    sub_result = Operators.subtract(10, 4)
    assert sub_result == 6

    mul_result = Operators.multiply(add_result, sub_result)
    assert mul_result == 48  # 8 * 6

    div_result = Operators.divide(mul_result, 4)
    assert div_result == 12.0
