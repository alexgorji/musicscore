import itertools

from musicscore.readalist.read_a_list import MyRandom

from musicscore import basic_functions


class MidiGenerator(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def next(self):
        err = str(type(self)) + ' should override next()'
        raise ImportWarning(err)

    def copy(self):
        err = str(type(self)) + ' should override copy()'
        raise ImportWarning(err)


class RelativeMidi(MidiGenerator):
    def __init__(self, midi_range=None, proportions=None, directions=None, microtone=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._midi_range = None
        self._proportions = None
        self._directions = None
        self._microtone = None
        self._iterator = None
        self._direction_iterator = None

        self.midi_range = midi_range
        self.proportions = proportions
        self.directions = directions
        self.microtone = microtone

    @property
    def midi_range(self):
        return self._midi_range

    @midi_range.setter
    def midi_range(self, values):
        if values:
            try:
                if not hasattr(values, '__iter__'):
                    values = [values, values]
                if len(values) == 1:
                    value = values[0]
                    values = [value, value]

                if len(values) != 2:
                    raise ValueError('wrong length for midi_range')
            except:
                raise TypeError('wrong type for midi_range')

            if min(values) < 18:
                raise ValueError('midi cannot be smaller than 18')

            self._midi_range = values
        else:
            self._midi_range = None

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if values:
            self._proportions = [value / sum(values) * 100 for value in values]
        else:
            self._proportions = None

    @property
    def directions(self):
        return self._directions

    @directions.setter
    def directions(self, values):
        if values:
            for value in values:
                if value not in [-1, 1]:
                    raise ValueError('directions can only be 1 or -1')

            self._directions = values
            self._direction_iterator = itertools.cycle(self._directions)
        else:
            self._directions = None
            self._direction_iterator = None

    @property
    def direction_iterator(self):
        return self._direction_iterator

    @property
    def microtone(self):
        return self._microtone

    @microtone.setter
    def microtone(self, value):
        if value and value not in [2, 4, 8]:
            raise ValueError('microtone can only be 2,4,8 or None')
        self._microtone = value

    @property
    def iterator(self):
        if self._iterator is None:
            def scale(old_value, old_lower_limit, old_higher_limit, new_lower_limit, new_higher_limit):
                old_range = float(old_higher_limit - old_lower_limit)
                if old_range == 0:
                    new_value = new_lower_limit
                else:
                    new_range = (new_higher_limit - new_lower_limit)
                    new_value = (((old_value - old_lower_limit) * new_range) / old_range) + new_lower_limit
                return new_value

            if not self.directions:
                raise AttributeError('set directions')
            if not self.proportions:
                raise AttributeError('set proportions')
            if not self.midi_range:
                raise AttributeError('set midi_range')
            if not self.microtone:
                raise AttributeError('set microtone')
            intervals = map(lambda proportion: proportion * self.direction_iterator.next(), self.proportions)
            midis = basic_functions.dToX(intervals)
            midis = map(lambda midi: scale(midi, min(midis), max(midis), self.midi_range[0], self.midi_range[1]), midis)
            factor = self.microtone / 2.0
            midis = map(lambda midi: round(midi * factor) / factor, midis)

            self._iterator = iter(midis)

        return self._iterator

    def next(self):
        return self.iterator.__next__()

    def copy(self):
        # print 'copying midi_generator: ReltaiveMidi'
        return self.__class__(midi_range=None, proportions=self.proportions, directions=self.directions,
                              microtone=self.microtone)


class RandomMidi(MidiGenerator):
    def __init__(self, pool=None, periodicity=None, seed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_random = MyRandom()

        self.pool = pool
        self.periodicity = periodicity
        self.seed = seed

    @property
    def my_random(self):
        return self._my_random

    @property
    def seed(self):
        return self.my_random.seed

    @seed.setter
    def seed(self, value):
        self.my_random.seed = value

    @property
    def pool(self):
        return self._my_random.pool

    @pool.setter
    def pool(self, values):
        if values is not None:
            if min(values) < 18:
                raise ValueError('midi cannot be smaller than 18')

            self._my_random.pool = list(set(values))
        else:
            self._my_random.pool = None

    @property
    def periodicity(self):
        return self._my_random.periodicity

    @periodicity.setter
    def periodicity(self, value):
        self._my_random.periodicity = value

    @property
    def iterator(self):
        return self.my_random

    def next(self):
        return self.my_random.next()

    def copy(self):
        return self.__class__(pool=self.pool, seed=self.seed, periodicity=self.periodicity)
