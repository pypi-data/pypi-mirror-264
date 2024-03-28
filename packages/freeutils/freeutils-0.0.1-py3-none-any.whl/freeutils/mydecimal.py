import decimal


class MyDecimal:
    def __init__(self, number) -> None:
        self.number = decimal.Decimal(str(number))

    def __str__(self) -> str:
        return str(self.number)

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other):
        return self.number + other.number

    def __sub__(self, other):
        return self.number - other.number

    def __mul__(self, other):
        return self.number * other.number

    def __truediv__(self, other):
        return self.number / other.number

    def __floordiv__(self, other):
        return self.number // other.number

    def __mod__(self, other):
        return self.number % other.number

    def round(self, digits=0):
        if digits <= 0:
            num_of_digits = decimal.Decimal(str(1))
        else:
            num_of_digits = 1 + decimal.Decimal(str(3) * digits) / (10**digits)

        return self.number.quantize(num_of_digits, decimal.ROUND_HALF_UP)
