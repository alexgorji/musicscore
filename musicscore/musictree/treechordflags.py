from musicscore.musicxml.elements.note import Notehead


class TreeChordFlag(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement_percussion_notation(self, chord):
        if chord.is_tied_to_next:
            chord.remove_tie('start')
        output = None
        if chord.is_tied_to_previous:
            chord.to_rest()
            output = [chord]
        elif chord.position_in_beat == 0:
            output = [chord]
            if chord.quarter_duration == 1:
                output = chord.split(1, 1)
            elif chord.quarter_duration == 2:
                output = chord.split(1, 3)
            elif chord.quarter_duration == 3:
                output = chord.split(1, 5)
            elif chord.quarter_duration == 4:
                output = chord.split(1, 7)
            elif chord.quarter_duration == 6:
                output = chord.split(1, 11)
            else:
                pass
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

    def implement(self, chord):
        output = self.implement_percussion_notation(chord)
        for ch in output:
            if not ch.is_rest:
                ch.add_words('pizz.')
        return output


class PercussionFlag(TreeChordFlag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        output = self.implement_percussion_notation(chord)
        return output


class NoiseFlag(TreeChordFlag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def implement(self, chord):
        chord.add_child(Notehead('square'))
        return [chord]
