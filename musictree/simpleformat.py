from musictree import Midi, Chord
import copy

from util import dToX, xToD


class SimpleFormat(object):
    """
    It is useful tool to generate list of chords and also do some simple algorithmic changes to it if needed.
    """

    def __init__(self, quarter_durations=None, midis=None, default_midi=71, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_midi = None
        self._quarter_durations = None
        self._midis = None
        self._set_quarter_durations(quarter_durations)
        self._set_midis(midis)
        self._chords = None

        self.default_midi = default_midi

    # //private methods
    @staticmethod
    def _check_quarter_duration(quarter_durations):
        for quarter_duration in quarter_durations:
            if quarter_duration < 0:
                raise ValueError('SimpleFormat(): wrong duration {}'.format(quarter_duration))

    def _generate_chords(self):
        self._chords = []
        if self._quarter_durations == [] and self._midis == []:
            pass
        else:
            self._chords = []
            for i in range(len(self._quarter_durations) - len(self._midis)):
                self._midis.append(copy.deepcopy(self.default_midi))

            for i in range(len(self._midis) - len(self._quarter_durations)):
                self._quarter_durations.append(1)

            for d, m in zip(self._quarter_durations, self._midis):
                self._chords.append(Chord(m, d))

    def _set_midis(self, midis):
        def _is_value(x):
            try:
                float(x)
                return True
            except (ValueError, TypeError):
                return False

        def _is_midi(x):
            if isinstance(x, Midi):
                return True
            else:
                return False

        if midis is None:
            midis = []
        else:
            try:
                midis = list(midis)
            except TypeError:
                midis = [midis]

        self._midis = []
        for m in midis:
            if _is_midi(m):
                self._midis.append(m)
            elif _is_value(m):
                self._midis.append(Midi(m))
            elif isinstance(m, list) or isinstance(m, tuple):
                tmp = []

                for midi in m:
                    if _is_midi(midi):
                        tmp.append(midi)
                    elif _is_value(midi):
                        tmp.append(Midi(midi))
                    else:
                        raise TypeError
                self._midis.append(tmp)
            else:
                raise TypeError

    def _set_quarter_durations(self, quarter_durations):
        if quarter_durations is None:
            quarter_durations = []
        else:
            try:
                quarter_durations = list(quarter_durations)
            except TypeError:
                quarter_durations = [quarter_durations]

        self._check_quarter_duration(quarter_durations)

        self._quarter_durations = quarter_durations

    # //public properties
    @property
    def chords(self):
        if self._chords is None:
            self._generate_chords()
        return self._chords

    @property
    def default_midi(self):
        """
        If only quarter_durations are provided the midi of chord will be set to default_midi. Default value is 71.
        """
        return self._default_midi

    @default_midi.setter
    def default_midi(self, val):
        if isinstance(val, Midi):
            self._default_midi = val
        else:
            self._default_midi = Midi(val)

    @property
    def quarter_duration(self):
        return sum([chord.quarter_duration for chord in self.chords])

    @property
    def midis(self):
        return [chord.midis for chord in self.chords]

    # //public methods

    # add
    def add_chord(self, chord):
        # generate chords if needed
        self.chords
        self._chords.append(chord)
        return chord

    # get

    def get_midis(self):
        return [chord.midis for chord in self.chords]

    def get_quarter_durations(self):
        return [chord.quarter_duration for chord in self.chords]

    def get_quarter_positions(self):
        return dToX(self.get_quarter_durations())

    # //other

    def change_chords(self, function):
        """
        The given function will be applied to all chords.
        """
        for chord in self.chords:
            function(chord)

    def extend(self, simple_format):
        """
        Chords of another SimpleFormat will be added at the end of self.chords.
        """
        for chord in simple_format.chords:
            self.add_chord(chord)

    def mirror(self, pivot=None):
        """
        Chords will be changed to get a mirrored version of the original. Pivot is a midi value that will be used as mirror axis. If not set the first midi will be the axis.
        """
        if pivot is None:
            pivot = self.chords[0].midis[0]
        elif not isinstance(pivot, Midi):
            pivot = Midi(pivot)
        else:
            pass

        for midi in [m for ch in self.chords for m in ch.midis]:
            transposition_interval = (pivot.value - midi.value) * 2
            midi.transpose(transposition_interval)

    def multiply_quarter_durations(self, factor):
        for chord in self.chords:
            chord.quarter_duration *= factor

    # @staticmethod
    # def sum(*simple_formats, no_doubles=False):
    #     """
    #     A static method for combining two SimpleFormats.
    #     """
    #     def _copied_position_dict(sf):
    #         output = {}
    #         for chord, position in zip(sf.chords, sf.get_quarter_positions()):
    #             output[position] = chord.__deepcopy__()
    #         return output
    #
    #     def _key_sorted_dict(dict):
    #         output = {}
    #         for key in sorted(dict.keys()):
    #             output[key] = dict[key]
    #         return output
    #
    #     def _trim_quarter_durations():
    #         quarter_durations = xToD(list(all_positioned_chords.keys()))
    #         chords = all_positioned_chords.values()
    #         for quarter_duration, chord in zip(quarter_durations, chords):
    #             chord.quarter_duration = quarter_duration
    #
    #     all_positioned_chords = _copied_position_dict(simple_formats[0])
    #     for sf in simple_formats[1:]:
    #         other_positioned_chords = _copied_position_dict(sf)
    #         for other_position, other_chord in other_positioned_chords.items():
    #             if other_position in all_positioned_chords.keys():
    #                 chord = all_positioned_chords[other_position]
    #                 if chord.is_rest:
    #                     all_positioned_chords[other_position] = chord
    #                 elif not other_chord.is_rest:
    #                     for midi in other_chord.midis:
    #                         if not no_doubles or midi.value not in [m.value for m in chord.midis]:
    #                             chord.add_midi(midi)
    #                 else:
    #                     pass
    #             else:
    #                 all_positioned_chords[other_position] = other_chord
    #     all_positioned_chords = _key_sorted_dict(all_positioned_chords)
    #     _trim_quarter_durations()
    #     output = SimpleFormat()
    #     for chord in all_positioned_chords.values():
    #         output.add_chord(chord)
    #     return output

    def retrograde(self):
        self._chords = list(reversed(self.chords))

    def transpose(self, interval_midi):
        if isinstance(interval_midi, Midi):
            interval = interval_midi.value - self.chords[0].midis[0].value
        else:
            interval = interval_midi
        for ch in self.chords:
            ch.transpose(interval)
