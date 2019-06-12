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

    def __call__(self, x):
        raise EquationError('__call__ must be overridden by subclass')


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

    def __call__(self, x):
        return (self.a * x) + self.b


class AGCos(AGEquation):
    def __init__(self, frequency=0.1, a=1, b=0, c=0, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._frequency = None
        self._a = None
        self._b = None
        self._c = None

        self.frequency = frequency
        self.a = a
        self.b = b
        self.c = c

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value

    def get_frequency(self, x):
        if not callable(self.frequency):
            return self.frequency
        return self.frequency(x)

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    def get_a(self, x):
        if not callable(self.a):
            return self.a
        return self.a(x)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value

    def get_b(self, x):
        if not callable(self.b):
            return self.b
        return self.b(x)

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = value

    def get_c(self, x):
        if not callable(self.c):
            return self.c
        return self.c(x)

    def __call__(self, x):
        frequency = self.get_frequency(x)
        a = self.get_a(x)
        b = self.get_b(x)
        c = self.get_c(x)

        y = a * math.cos(frequency * 2 * math.pi * (x - b)) + c
        # y = a * math.cos(frequency * (x - b)) + c
        return y
