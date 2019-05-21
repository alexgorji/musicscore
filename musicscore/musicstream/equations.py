import math


class EquationError(Exception):
    def __init__(self, msg=''):
        super().__init__(msg)


class NoFrequencyError(EquationError):
    def __init__(self):
        super().__init__(msg='set frequency first')


class AGEquation(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_y(self, x):
        raise EquationError('get_y must be overridden by subclass')


class AGLinear(AGEquation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._a = None
        self._b = None
        self._c = None

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value == 0:
            raise ValueError()
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value == 0:
            raise ValueError()
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = value


class AGCos(AGEquation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._frequency = None
        self._a = 1
        self._b = 0
        self._c = 0

    # @property
    # def frequency_formula(self):
    #     return self._frequency_formula
    #
    # @frequency_formula.setter
    # def frequency_formula(self, value):
    #     if not isinstance(value, AGEquation):
    #         raise TypeError()
    #     self._frequency_formula = value

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value == 0:
            raise ValueError()
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = value

    def get_y(self, x):
        if not self.frequency:
            raise NoFrequencyError()

        y = self.a * math.cos(self.frequency * 2 * math.pi * (x - self.b)) + self.c
        return y
