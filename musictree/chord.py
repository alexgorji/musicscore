from fractions import Fraction
from typing import Union, List, Optional, Any, Dict

from musicxml.xmlelement.xmlelement import XMLChord, XMLLyric, XMLDirection, XMLDirectionType, XMLDynamics, XMLNotations, \
    XMLArticulations, XMLTechnical

from musictree.dynamics import Dynamics
from musictree.exceptions import ChordAlreadySplitError, ChordCannotSplitError, ChordHasNoParentError, \
    ChordQuarterDurationAlreadySetError, AlreadyFinalUpdated
from musictree.midi import Midi
from musictree.core import MusicTree
from musictree.note import Note
from musictree.quarterduration import QuarterDuration, QuarterDurationMixin
from musictree.util import XML_ARTICULATION_CLASSES, XML_TECHNICAL_CLASSES

__all__ = ['Chord', 'group_chords']

_all_articulations = Union[
    'XMLAccent', 'XMLStrongAccent', 'XMLStaccato', 'XMLTenuto', 'XMLDetachedLegato', 'XMLStaccatissimo',
    'XMLSpiccato', 'XMLScoop', 'XMLPlop', 'XMLDoit', 'XMLFalloff', 'XMLBreathMark', 'XMLCaesura', 'XMLStress',
    'XMLUnstress']

_all_technicals = Union[
    "XMLUpBow", "XMLDownBow", "XMLHarmonic", "XMLOpenString", "XMLThumbPosition", "XMLFingering", "XMLPluck", "XMLDoubleTongue",
    "XMLTripleTongue", "XMLStopped", "XMLSnapPizzicato", "XMLFret", "XMLString", "XMLHammerOn", "XMLPullOff", "XMLBend", "XMLTap",
    "XMLHeel", "XMLToe", "XMLFingernails", "XMLHole", "XMLArrow", "XMLHandbell", "XMLBrassBend", "XMLFlip", "XMLSmear", "XMLOpen",
    "XMLHalfMuted", "XMLHarmonMute", "XMLGolpe", "XMLOtherTechnical"]


class Chord(MusicTree, QuarterDurationMixin):
    """
    Chord is a sequence of one or more :obj:`~musicxml.xmlelement.xmlelement.XMLNote`s which occur at the same time in a :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure` of a :obj:`~musicxml.xmlelement.xmlelement.XMLPart`.
    :param midis: Midi, Midi.value, [Midi, Midi.value] 0 or [0] for a rest.
    :param quarter_duration: int, float, Fraction, QuarterDuration for duration counted in quarters (crotchets). 0 for grace note (or
    chord).
    """
    _ATTRIBUTES = {'midis', 'quarter_duration', 'notes', '_note_attributes', 'offset', 'split', 'voice', '_xml_lyrics', 'ties',
                   '_notes_are_set', '_xml_direction_types', '_xml_directions', '_xml_articulations', '_xml_technicals', '_final_updated'}

    def __init__(self, midis: Optional[Union[List[Union[float, int]], List[Midi], float, int, Midi]] = None,
                 quarter_duration: Optional[Union[float, int, 'Fraction', QuarterDuration]] = None, **kwargs):
        self._midis = None
        self._ties = []
        self._xml_direction_types = {'above': [], 'below': []}

        self._xml_articulations = []
        self._xml_directions = []
        self._xml_lyrics = []
        self._xml_technicals = []

        self._note_attributes = kwargs
        self._notes_are_set = False

        super().__init__(quarter_duration=quarter_duration)
        self._set_midis(midis)
        self.split = False
        self._final_updated = False

    def _set_midis(self, midis):
        if isinstance(midis, str):
            raise TypeError
        if hasattr(midis, '__iter__'):
            pass
        elif midis is None:
            midis = []
        else:
            midis = [midis]
        if len(midis) > 1 and 0 in midis:
            raise ValueError('Chord cannot accept a mixed list of midis of rests and pitches or a list of more than one rests.')

        if 0 in midis and self.quarter_duration == 0:
            raise ValueError('A rest cannot be a grace note')
        self._midis = [Midi(v) if not isinstance(v, Midi) else v for v in midis]
        self._update_notes_pitch_or_rest()

    def _update_xml_directions(self):
        def _add_dynamics(list_of_dynamics, xml_direction):
            for dynamics in list_of_dynamics:
                dt = xml_direction.add_child(XMLDirectionType())
                dyn = dt.xml_dynamics = XMLDynamics()
                dyn.add_child(dynamics.xml_object)

        for placement in self._xml_direction_types:
            direction_types = self._xml_direction_types[placement]
            for direction_type in direction_types:
                d = XMLDirection(placement=placement)
                self._xml_directions.append(d)
                if direction_type[0] == 'dynamics':
                    _add_dynamics(list_of_dynamics=direction_type[1], xml_direction=d)
                else:
                    raise NotImplementedError

    def _update_xml_articulations(self):
        def _get_note_xml_articulations():
            try:
                return n.xml_notations.xml_articulations.get_children(ordered=False)
            except AttributeError:
                return []

        n = self.notes[0]

        note_articulations_not_in_chord = [art for art in _get_note_xml_articulations() if art not in
                                           self._xml_articulations]
        chord_articulations_not_in_note = [art for art in self._xml_articulations if art not in _get_note_xml_articulations()]

        if chord_articulations_not_in_note:
            n.get_or_create_xml_notations()
            if not n.xml_notations.xml_articulations:
                n.xml_notations.xml_articulations = XMLArticulations()

            for xml_articulation in chord_articulations_not_in_note:
                n.xml_notations.xml_articulations.add_child(xml_articulation)

        for art in note_articulations_not_in_chord:
            n.xml_notations.xml_articulations.remove(art)

        n.update_xml_notations()

    def _update_xml_technicals(self):
        def get_note_xml_technical():
            try:
                return n.xml_notations.xml_technical.get_children(ordered=False)
            except AttributeError:
                return []

        n = self.notes[0]

        note_technicals_not_in_chord = [tech for tech in get_note_xml_technical() if tech not in
                                        self._xml_technicals]
        chord_technicals_not_in_note = [tech for tech in self._xml_technicals if tech not in get_note_xml_technical()]

        if chord_technicals_not_in_note:
            n.get_or_create_xml_notations()
            if not n.xml_notations.xml_technical:
                n.xml_notations.xml_technical = XMLTechnical()

            for xml_technical in chord_technicals_not_in_note:
                n.xml_notations.xml_technical.add_child(xml_technical)

        for tech in note_technicals_not_in_chord:
            n.xml_notations.xml_technical.remove(tech)

        n.update_xml_notations()

    def _update_xml_lyrics(self):

        n = self.notes[0]

        note_lyrics_not_in_chord = [lyric for lyric in n.xml_object.find_children('XMLLyric') if lyric not in
                                    self._xml_lyrics]
        chord_lyrics_not_in_note = [lyric for lyric in self._xml_lyrics if lyric not in n.xml_object.find_children('XMLLyric')]

        if chord_lyrics_not_in_note:

            for xml_lyric in chord_lyrics_not_in_note:
                n.xml_object.add_child(xml_lyric)

        for lyric in note_lyrics_not_in_chord:
            n.xml_object.remove(lyric)

    def _update_notes(self):
        for child in self.get_children()[len(self.midis):]:
            self.remove(child)
        for index, midi in enumerate(self.midis):
            try:
                self.get_children()[index].midi = midi
            except IndexError:
                self.add_child(Note(parent_chord=self, midi=midi, **self._note_attributes))
        self._notes_are_set = True

    def _update_xml_chord(self):
        if len(self.notes) > 1:
            if not self.notes[0].xml_object.xml_chord:
                self.notes[0].xml_object.add_child(XMLChord())
        else:
            self.notes[0].xml_object.xml_chord = None

    def final_updates(self):
        """
        Final updates can be called only once. All necessary updates and xmlelement object creations will take place and the MusicTree
        object will be prepared for returning a musicxml snippet or a whole musicxml file.

        - Check if parent :obj:`~musictree.beat.Beat` exists.
        - Ancestor :obj:`~musictree.measure.Measure.update_divisions()` is called to update :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure`'s :obj:`~musicxml.xmlelement.xmlelement.XMLDivisions` attribute.
        - Following updates are triggered: update_notes, update_xml_chord, update_notes_quarter_durations, update_xml_lyrics,
          update_xml_directions, update_xml_articulations, update_technicals
        """
        if self._final_updated:
            raise AlreadyFinalUpdated(self)

        if not self.up:
            raise ChordHasNoParentError('Chord needs a parent Beat to create notes.')

        self._update_notes()
        self._update_xml_chord()

        self._update_notes_quarter_duration()
        self._update_xml_lyrics()
        self._update_tie()
        self._update_xml_directions()
        self._update_xml_articulations()
        self._update_xml_technicals()
        self._final_updated = True

    def _update_notes_quarter_duration(self):
        for note in self.notes:
            note.quarter_duration = self.quarter_duration

    def _update_notes_pitch_or_rest(self):
        if self.notes:
            len_diff = len(self.notes) - len(self.midis)
            if len_diff > 0:
                to_be_removed = self.notes[len_diff:]
                for note in to_be_removed:
                    note.up.remove(note)
                    note.parent_chord = None
                    del note
            for index, m in enumerate(self.midis):
                if index < len(self.notes):
                    self.notes[index].midi = m
                else:
                    new_note = Note(parent_chord=self, midi=m, quarter_duration=self.quarter_duration)
                    self.add_child(new_note)

    def _update_tie(self):
        if not self._ties:
            for note in self.notes:
                note.remove_tie()
        else:
            if 'stop' in self._ties:
                for note in self.notes:
                    note.stop_tie()
            if 'start' in self._ties:
                for note in self.notes:
                    note.start_tie()

    @property
    def is_rest(self) -> bool:
        """
        :return: ``True`` if Chord represents a rest, ``False`` if otherwise.
        :rtype: bool
        """
        if self._midis[0].value == 0:
            return True
        else:
            return False

    @property
    def midis(self) -> List['Midi']:
        """
        :return: list of midis

        >>> ch = Chord(midis=60)
        >>> [type(m) for m in ch.midis]
        [<class 'musictree.midi.Midi'>]
        >>> [m.value for m in ch.midis]
        [60]
        >>> ch = Chord(midis=[60, Midi(40)])
        >>> [m.value for m in ch.midis]
        [60, 40]
        >>> Chord([0, 60])
        Traceback (most recent call last):
        ...
        ValueError: Chord cannot accept a mixed list of midis of rests and pitches or a list of more than one rests.
        """
        return self._midis

    @midis.setter
    def midis(self, val):
        self._set_midis(val)

    @property
    def notes(self) -> List['Note']:
        """
        :return: :obj:`musictree.chord.get_children` which are of type :obj:`musictree.note.Note`.
        :rtype: List[:obj:`~musictree.note.Note`]
        """
        return self.get_children()

    @property
    def offset(self) -> QuarterDuration:
        """
        :return: Offset in Chord's parent :obj:`~musictree.beat.Beat`
        :rtype: QuarterDuration
        """
        if not self.up:
            return None
        elif self.previous is None:
            return 0
        else:
            return self.previous.offset + self.previous.quarter_duration

    @QuarterDurationMixin.quarter_duration.setter
    def quarter_duration(self, val):
        if self._quarter_duration is not None and self.up:
            raise ChordQuarterDurationAlreadySetError('Chord is already attached to a Beat. Quarter Duration cannot be changed any more.')
        if val is not None:
            if self.midis and self.is_rest and val == 0:
                raise ValueError('A rest cannot be a grace note')
            self._set_quarter_duration(val)
            if self._notes_are_set:
                self._update_notes_quarter_duration()

    @property
    def voice_number(self) -> int:
        """
        :return: Number of parent :obj:`~musictree.voice.Voice`
        :rtype: positive int
        """
        if not self.up:
            raise ChordHasNoParentError()
        if self.up and self.up.up:
            return self.up.up.number
        else:
            return 1

    @property
    def xml_articulations(self) -> List[_all_articulations]:
        """
        :return: list of xml articulations to be added to self.notes
        """
        return self._xml_articulations

    @property
    def xml_direction_types(self) -> Dict:
        """
        :return: dict of xml direction types to be added to self.notes.

        .. todo::
           Better documentation. Which types can be added?  Example?
        """
        return self._xml_direction_types

    @property
    def xml_lyrics(self) -> List['XMLLyric']:
        """
        :return: list of xml lyrics to be added to self.notes
        """
        return self._xml_lyrics

    @property
    def xml_technicals(self) -> List[_all_articulations]:
        """
        :return: list of xml technicals to be added to self.notes
        """
        return self._xml_technicals

    def add_xml_articulation(self, xml_articulation_object: _all_articulations) -> 'xml_articulation_object':
        """
        This method is used to add one xml articulation object to chord's private __xml_articulations list.
        This list is used to add or update articulations of the first :obj:`~musictree.note.Note` object of chord`s notes which are to be or are already created .

        :param xml_articulation_object: musicxml articulation element
        :return: xml_articulation_object
        """

        if xml_articulation_object.__class__ not in XML_ARTICULATION_CLASSES:
            raise TypeError
        self._xml_articulations.append(xml_articulation_object)
        if self.notes:
            self._update_xml_articulations()
        return xml_articulation_object

    def add_child(self, child: Note) -> Note:
        """
        Check and add child to list of children. Child's parent is set to self.

        :param child: :obj:`~musictree.note.Note`
        :return: child
        :rtype: :obj:`~musictree.note.Note`
        """
        return super().add_child(child)

    def add_dynamics(self, dynamics: Union[List['Dynamics'], 'Dynamics', str], placement: str = 'below') -> List['Dynamics']:
        """
        This method is used to add one or more :obj:`musictree.dynamics.Dynamics` objects to chord's private dictionary _xml_direction_types
        This list is used to create or update directions of the first :obj:`~musictree.note.Note` object of chord`s notes
        which are to be or are already created .

        :param dynamics: str, Dynamics of a list of Dynamics to be added to directions
        :param placement: above or below
        :return: List[:obj:`~musictree.dynamics.Dynamics`]
        """
        dynamics_list = [dynamics] if isinstance(dynamics, str) or not hasattr(dynamics, '__iter__') else list(dynamics)
        dynamics_object_list = [d if isinstance(d, Dynamics) else Dynamics(d) for d in dynamics_list]
        self._xml_direction_types[placement].append(('dynamics', dynamics_object_list))
        return dynamics_object_list

    def add_xml_technical(self, xml_technical_object: _all_technicals) -> 'xml_technical_object':
        """
        This method is used to add one xml technical object to chord's private __xml_technicals list.
        This list is used to add or update technicals of the first :obj:`~musictree.note.Note` object of chord`s notes which are to be or are already created .

        :param xml_technical_object: musicxml technical element
        :return: xml_technical_object
        """

        if xml_technical_object.__class__ not in XML_TECHNICAL_CLASSES:
            raise TypeError
        self._xml_technicals.append(xml_technical_object)
        if self.notes:
            self._update_xml_technicals()
        return xml_technical_object

    def add_tie(self, val: str) -> None:
        """
        Chord's tie list is used to add ties to or update ties of :obj:`musictree.note.Note` objects which are to be or are already
        created .

        :param val: 'start' or 'stop'
        :return: None
        """
        if val not in ['start', 'stop']:
            raise ValueError
        if val not in self._ties:
            self._ties.append(val)
            self._update_tie()

    def add_lyric(self, text: Union[Any, XMLLyric]):
        """
        This method is used to add :obj:`~musicxml.xmlelement.xmlelement.XMLLyric` to chord's private _xml_lyricx list.
        This list is used to add lyrics to or update lyrics of the first :obj:`~musictree.note.Note` object of chord`s notes
        which are to be or are already created .

        :param text: if not of type :obj:`~musicxml.xmlelement.xmlelement.XMLLyric` a string conversion will be applied to text.
        :return: :obj:`~musicxml.xmlelement.xmlelement.XMLLyric`
        """
        if isinstance(text, XMLLyric):
            l = text
        else:
            l = XMLLyric()
            l.xml_text = str(text)
        self._xml_lyrics.append(l)
        if self.notes:
            self._update_xml_lyrics()
        return l

    def get_children(self) -> List[Note]:
        """
        :return: list of added children.
        :rtype: List[:obj:`~musictree.note.Note`]
        """
        return super().get_children()

    def get_parent(self) -> 'Beat':
        """
        :return: parent
        :rtype: :obj:`~musictree.beat.Beat`
        """
        return super().get_parent()

    def get_parent_measure(self) -> 'Measure':
        """
        :return: parent measure
        """
        return self.up.up.up.up

    def get_staff_number(self):
        return self.up.up.up.number

    def get_voice(self):
        raise TypeError

    def get_voice_number(self) -> int:
        """
        :return: parent voice number
        :rtype: positive int
        """
        return self.up.up.number

    def set_possible_subdivisions(self):
        raise TypeError

    def has_same_pitches(self, other: 'Chord') -> bool:
        """
        Only for chords with pitches. Rest chords cannot use this method.

        :param other: Other chord to which the comparison takes place
        :return: `True` if pitches of self and other chord has the same pitch parameters and accidental values else `False`
        """
        if not isinstance(other, Chord):
            raise TypeError
        if self.is_rest or other.is_rest:
            raise TypeError('Rest cannot use method has_same_pitches.')
        if [m.value for m in self.midis] != [m.value for m in other.midis]:
            return False
        for m1, m2 in zip(self.midis, other.midis):
            if m1.accidental.show != m2.accidental.show:
                return False
            if m1.accidental.get_pitch_parameters() != m2.accidental.get_pitch_parameters():
                return False
        return True

    def split_and_add_beatwise(self, beats: List['Beat']) -> List['Chord']:
        """
        All betas must have a voice parent

        :param beats:
        :return:
        """
        voice_set = {beat.up for beat in beats}
        if len(voice_set) != 1:
            raise ChordCannotSplitError('Beats have must have a single Voice as common ancestor.')

        voice = voice_set.pop()
        if voice is None:
            raise ChordCannotSplitError('Beats have no parent.')

        if voice.get_children()[voice.get_children().index(beats[0]): voice.get_children().index(beats[-1]) + 1] != beats:
            raise ChordCannotSplitError("Beats as Voice's children has another order as input list of beats")

        if beats[0] != voice.get_current_beat():
            raise ChordAlreadySplitError('First beat must be the next beat in voice which can accept chords.')
        if beats[-1] != voice.get_children()[-1]:
            raise ChordAlreadySplitError('Last beat must be the last beat in voice.')
        quarter_durations = self.quarter_duration.get_beatwise_sections(
            offset=beats[0].filled_quarter_duration, beats=beats)
        self.quarter_duration = quarter_durations[0][0]
        self.split = True
        voice.get_current_beat().add_child(self)
        current_chord = self
        output = [self]
        for qd in quarter_durations[0][1:]:
            copied = split_copy(self, qd)
            copied.split = True
            voice.get_current_beat().add_child(copied)
            current_chord.add_tie('start')
            copied.add_tie('stop')
            for midi in copied.midis:
                midi.accidental.show = False
            current_chord = copied
            output.append(current_chord)
        if quarter_durations[1]:
            leftover_chord = split_copy(self, quarter_durations[1])
            current_chord.add_tie('start')
            leftover_chord.add_tie('stop')
            for midi in leftover_chord.midis:
                midi.accidental.show = False
        else:
            leftover_chord = None
        self.up.up.leftover_chord = leftover_chord

        return output

    def to_rest(self) -> None:
        """
        Set self.midis to [0]

        :return: None
        """
        self.midis = [0]

    def __setattr__(self, key, value):
        if key not in self._ATTRIBUTES.union(self._TREE_ATTRIBUTES) and key not in [f'_{attr}' for attr in
                                                                                    self._ATTRIBUTES.union(
                                                                                        self._TREE_ATTRIBUTES)] and key not in self.__dict__:
            if self.notes:
                if isinstance(value, str) or not hasattr(value, '__iter__'):
                    value = [value] * len(self.notes)
                for n, v in zip(self.notes, value):
                    setattr(n, key, v)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        if not self._notes_are_set:
            raise AttributeError(f"AttributeError: 'Chord' object has no attribute '{item}'")
        output = [getattr(n, item) for n in self.notes]
        if output and callable(output[0]):
            raise AttributeError(f"Chord cannot call Note method {item}. Call this method on each note separately")
        return output


def split_copy(chord: Chord, new_quarter_duration: Union[QuarterDuration, Fraction, int, float] = None) -> Chord:
    """
    This function is used when a chord needs to be split. It creates a copy of the chord with a new quarter_duration object. All midis
    will be deepcopied. No attributes like lyrics, articulations etc. will be added to the copy.

    :param chord:
    :param new_quarter_duration: quarter_duration of copied chord. If None a shallow copy of chord.quarter_duration is created.
    :return: copied chord
    """
    if new_quarter_duration is None:
        new_quarter_duration = chord.quarter_duration.__copy__()
    new_chord = Chord(midis=[m.__deepcopy__() for m in chord.midis], quarter_duration=new_quarter_duration)
    return new_chord


def group_chords(chords: List[Chord], quarter_durations: List[Union[QuarterDuration, Fraction, int, float]]) -> Optional[List[List[Chord]]]:
    """
    A creates a nested list of chords. Chords can be divided into groups. Each group has its own specific quarter duration sum.

    :param chords:
    :param quarter_durations:
    :return: Optional[List[List[:obj:`Chord`]]]
    """
    if sum(c.quarter_duration for c in chords) != sum(quarter_durations):
        raise ValueError
    output = []
    for _ in quarter_durations:
        output.append([])
    index = 0
    current_quarter_duration = quarter_durations[0]
    for ch in chords:
        output[index].append(ch)
        current_sum = sum(c.quarter_duration for c in output[index])
        if current_sum < current_quarter_duration:
            pass
        elif current_sum == current_quarter_duration:
            index += 1
            if index == len(quarter_durations):
                pass
            else:
                current_quarter_duration = quarter_durations[index]
        else:
            return None
    return output
