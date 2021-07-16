from values.value import Value
from errors import *
from runTimeResult import RunTimeResult
import math

class Number(Value):

    def __init__(self, value):
        super().__init__()
        self.value = float(value)

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                    )

            return Number(self.value / other.value).set_context(self.context), None

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(self.value == other.value).set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(self.value != other.value).set_context(self.context), None

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(self.value < other.value).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(self.value > other.value).set_context(self.context), None

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(self.value <= other.value).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(self.value >= other.value).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(self.value and other.value).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(self.value or other.value).set_context(self.context), None

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return f"{self.value}"

Number.null    = Number(0)
Number.false   = Number(0)
Number.true    = Number(1)
Number.math_PI = Number(math.pi)


