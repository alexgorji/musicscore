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
    def __init__(self, a=1, b=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._a = None
        self._b = None

        self.a = a
        self.b = b

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value

    def get_y(self, x):
        return (self.a * x) + self.b


class AGCos(AGEquation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._frequency = None
        self._a = 1
        self._b = 0
        self._c = 0

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
        if callable(self.frequency):
            frequency = self.frequency(x)
        else:
            frequency = self.frequency

        y = self.a * math.cos(frequency * 2 * math.pi * (x - self.b)) + self.c
        return y
