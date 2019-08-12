from musicscore.musicxml.elements.note import Notehead


class TreeChordFlag(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_split_ratios(self, beat, chord):
        quarter_beat = {1.5: [2, 1], 2: [1, 1], 3: [1, 2], 4: [1, 3], 6: [1, 5]}
        eighth_beat = {1: [1, 1], 1.5: [1, 2], 2: [1, 3], 3: [1, 5], 4: [1, 7], 6: [1, 11]}
        if beat.duration == 1:
            try:
                return chord.split(*quarter_beat[chord.quarter_duration])
            except KeyError:
                return [chord]
        elif beat.duration == 0.5:
            try:
                return chord.split(*eighth_beat[chord.quarter_duration])
            except KeyError:
                return [chord]

    def implement_percussion_notation(self, chord, beat):
        if chord.is_tied_to_next:
            chord.remove_tie('start')
        output = None
        if chord.is_tied_to_previous:
            chord.to_rest()
            output = [chord]
        elif chord.position_in_beat == 0:
            output = self.get_split_ratios(beat, chord)
            try:
                output[1].to_rest()
            except IndexError:
                pass
        else:
            output = [chord]
        return output


class PizzFlag(TreeChordFlag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord, beat):
        output = self.implement_percussion_notation(chord, beat)
        for ch in output:
            if not ch.is_rest:
                ch.add_words('pizz.')
        return output


class PercussionFlag(TreeChordFlag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord, beat):
        output = self.implement_percussion_notation(chord, beat)
        return output


class NoiseFlag(TreeChordFlag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        chord.add_child(Notehead('square'))
        return [chord]
