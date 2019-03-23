from musicscore.musictree.midi import Midi
from musicscore.musictree.treenote import TreeNote
from musicscore.musicxml.elements.fullnote import Chord


class TreeChord(object):
    """"""

    def __init__(self, *midis, quarter_duration=1, **kwargs):
        super().__init__(**kwargs)
        self._quarter_duration = None
        self.quarter_duration = quarter_duration
        self._midis = None
        self.midis = midis

    @property
    def midis(self):
        return self._midis

    @midis.setter
    def midis(self, values):
        if values:
            output = []
            for midi in values:
                if not isinstance(midi, Midi):
                    output.append(Midi(midi))
                else:
                    output.append(midi)

            for midi in output:
                if midi.value == 0 and len(values) > 1:
                    raise ValueError('midi with value must be alone.')
        else:
            output = None

        self._midis = output

    @property
    def tree_notes(self):
        output = []
        for index, midi in enumerate(self.midis):
            note = TreeNote(event=midi.get_pitch_rest(), quarter_duration=self.quarter_duration)
            if index > 0:
                note.add_child(Chord())
            output.append(note)
        return output
