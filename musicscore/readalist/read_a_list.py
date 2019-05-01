class MyRandom(object):
    import random
    current_random = random

    def __init__(self, pool=None, periodicity=None, forbidden_list=None, seed=None):
        self._pool = None
        self._periodicity = None
        self._forbidden_list = None
        self._seed = None
        self._counter = 0
        self._result = None

        self.pool = pool
        self.periodicity = periodicity
        self.forbidden_list = forbidden_list
        self.seed = seed

    # periodicity None will sets the periodicity always to len(pool)-2
    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, values):
        if values is not None:
            try:
                self._pool = list(set(values))
            except:
                self._pool = [values]

    @property
    def periodicity(self):
        return self._periodicity

    @periodicity.setter
    def periodicity(self, value):
        if value is not None:
            if isinstance(value, int) and value >= 0:
                self._periodicity = value
            else:
                raise ValueError()

    @property
    def forbidden_list(self):
        if not self._forbidden_list:
            self._forbidden_list = []
        return self._forbidden_list

    @forbidden_list.setter
    def forbidden_list(self, values):
        self._forbidden_list = values

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        self.current_random.seed(value)

    @property
    def counter(self):
        return self._counter

    @property
    def result(self):
        if self._result is None:
            self._result = []
        return self._result

    @property
    def iterator(self):

        if not self.pool:
            raise AttributeError('set pool')

        while True:
            periodicity = self.periodicity
            if self.periodicity is None:
                periodicity = len(self.pool) - 2

            elif self.periodicity >= len(self.pool):
                periodicity = len(self.pool) - 1

            if periodicity < 0: periodicity = 0

            def check(x):

                def forbid_element(x):
                    if len(self.forbidden_list) >= periodicity:
                        self.forbidden_list.pop(0)
                    self.forbidden_list.append(x)

                if periodicity != 0:
                    if x in self.forbidden_list:
                        return False
                    else:
                        forbid_element(x)
                        return True
                else:
                    return True

            if len(self.forbidden_list) > periodicity:
                # print "self.periodicity", self.periodicity
                self.forbidden_list = self.forbidden_list[(-1 * periodicity):]

            random_element = self.pool[self.current_random.randrange(len(self.pool))]
            while check(random_element) is False:
                random_element = self.pool[self.current_random.randrange(len(self.pool))]

            yield random_element

    def next(self):
        next_el = self.iterator.__next__()
        self._counter += 1
        # self._sum+=next_el
        self.result.append(next_el)

        return next_el


class ReadAList(object):
    ##mode in forwards, backwards, zickzack, random
    def __init__(self, pool=None, mode='random', seed=None):
        self._pool = None
        self._mode = None
        self._random = None
        self._index = None
        self._direction = 1
        self._next_index = None

        self.pool = pool
        self.mode = mode
        self.seed = seed

    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, values):
        if values is not None:
            try:
                self._pool = list(values)
            except:
                self._pool = [values]
        self.random.pool = self.pool

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in ['forwards', 'backwards', 'zickzack', 'random']:
            err = 'mode can only be forwards, backwards, zickzack or random'
            raise ValueError(err)
        self._mode = value

    @property
    def random(self):
        if self._random is None:
            self._random = MyRandom()
        return self._random

    @property
    def seed(self):
        return self.random.seed

    @seed.setter
    def seed(self, value):
        self.random.seed = value

    @property
    def next_index(self):
        err = 'next_index can only be set'
        raise AttributeError(err)

    @next_index.setter
    def next_index(self, value):
        self._next_index = value

    def _set_next_index(self):

        if self.mode == 'forwards':
            self._direction = 1

        elif self.mode == 'backwards':
            self._direction = -1

        elif self.mode == 'zickzack':
            pass

        self._index += self._direction

    def _check_index(self):
        if self.mode == 'forwards':
            if self._index >= len(self.pool):
                self._index = 0

        elif self.mode == 'backwards':
            if self._index >= len(self.pool):
                self._index = len(self.pool) - 1
            elif self._index < 0:
                self._index = len(self.pool) - 1

        elif self.mode == 'zickzack':
            if self._index == len(self.pool) - 1:
                self._direction = -1

            elif self._index > len(self.pool) - 1:
                self._index = len(self.pool) - 1
                self._direction = -1

            elif self._index == 0:
                self._direction = 1

            elif self._index < 0:
                self._index = 1
                self._direction = 1

    def next(self):
        if self.pool is None:
            err = 'pool can not be None'
            raise AttributeError(err)

        if self.mode != 'random':
            # print 'read_a_list.next(): self.mode=',self.mode
            # print 'read_a_list.next(): self._next_index=',self._next_index

            if self._next_index is None and self._index is None:
                if self.mode == 'backwards':
                    self._next_index = len(self.pool) - 1
                else:
                    self._next_index = 0

            if self._next_index is None:
                self._set_next_index()
            else:
                self._index = self._next_index
                self._next_index = None

            self._check_index()
            # print 'read_a_list.next(): self._index after check=',self._index
            # print 'read_a_list.next(): self.pool', self.pool
            return self.pool[self._index]

        else:
            return self.random.next()



