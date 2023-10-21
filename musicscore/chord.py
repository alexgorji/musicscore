import copy
from fractions import Fraction
from typing import Union, List, Optional, Any, Dict

from musicscore.clef import Clef
from musicscore.musictree import MusicTree
from musicscore.dynamics import Dynamics
from musicscore.exceptions import ChordAlreadySplitError, ChordCannotSplitError, ChordHasNoParentError, \
    ChordQuarterDurationAlreadySetError, AlreadyFinalizedError, DeepCopyException, ChordNotesAreAlreadyCreatedError, \
    ChordException, NotationException, ChordAddXException, ChordAddXPlacementException, RestCannotSetMidiError, \
    RestWithDisplayStepHasNoDisplayOctave, RestWithDisplayOctaveHasNoDisplayStep, GraceChordCannotHaveGraceNotes
from musicscore.finalize import FinalizeMixin
from musicscore.midi import Midi
from musicscore.note import Note
from musicscore.quarterduration import QuarterDuration, QuarterDurationMixin
from musicscore.util import XML_ARTICULATION_CLASSES, XML_TECHNICAL_CLASSES, XML_ORNAMENT_CLASSES, XML_DYNAMIC_CLASSES, \
    XML_OTHER_NOTATIONS, XML_DIRECTION_TYPE_CLASSES, XML_ORNAMENT_AND_OTHER_NOTATIONS, \
    XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS, isinstance_as_string
from musicxml.xmlelement.xmlelement import *

__all__ = ['Chord', 'Rest', 'GraceChord']

from musicxml.xmlelement.xmlelement import XMLElement

_all_articulations = Union[
    'XMLAccent', 'XMLStrongAccent', 'XMLStaccato', 'XMLTenuto', 'XMLDetachedLegato', 'XMLStaccatissimo',
    'XMLSpiccato', 'XMLScoop', 'XMLPlop', 'XMLDoit', 'XMLFalloff', 'XMLBreathMark', 'XMLCaesura', 'XMLStress',
    'XMLUnstress']

_all_technicals = Union[
    "XMLUpBow", "XMLDownBow", "XMLHarmonic", "XMLOpenString", "XMLThumbPosition", "XMLFingering", "XMLPluck", "XMLDoubleTongue",
    "XMLTripleTongue", "XMLStopped", "XMLSnapPizzicato", "XMLFret", "XMLString", "XMLHammerOn", "XMLPullOff", "XMLBend", "XMLTap",
    "XMLHeel", "XMLToe", "XMLFingernails", "XMLHole", "XMLArrow", "XMLHandbell", "XMLBrassBend", "XMLFlip", "XMLSmear", "XMLOpen",
    "XMLHalfMuted", "XMLHarmonMute", "XMLGolpe", "XMLOtherTechnical"]

_all_ornaments = Union[
    "XMLDelayedInvertedTurn", "XMLDelayedTurn", "XMLHaydn", "XMLInvertedMordent", "XMLInvertedTurn",
    "XMLInvertedVerticalTurn", "XMLMordent", "XMLOtherOrnament", "XMLSchleifer", "XMLShake", "XMLTremolo", "XMLTrillMark", "XMLTurn",
    "XMLVerticalTurn", "XMLWavyLine"
]

_all_dynamics = Union[
    "XMLF", "XMLFf", "XMLFff", "XMLFfff", "XMLFffff", "XMLFfffff", "XMLFp", "XMLFz", "XMLMf", "XMLMp", "XMLP", "XMLPf", "XMLPp", "XMLPpp", "XMLPppp",
    "XMLPpppp", "XMLPppppp", "XMLRf", "XMLRfz", "XMLSf", "XMLSffz", "XMLSfp", "XMLSfpp", "XMLSfz", "XMLSfzp"
]

_all_other_notations = Union[
    "XMLArpeggiate", "XMLFermata", "XMLFootnote", "XMLGlissando", "XMLLevel", "XMLNonArpeggiate", "XMLOtherNotation", "XMLSlide",
    "XMLSlur", "XMLAccidentalMark"
]


class Chord(MusicTree, QuarterDurationMixin, FinalizeMixin):
    """
    Chord is a sequence of one or more :obj:`~musicxml.xmlelement.xmlelement.XMLNote` s which occur at the same time in a :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure` of a :obj:`~musicxml.xmlelement.xmlelement.XMLPart`.

    :param midis: :obj:`~musicscore.midi.Midi`, Midi.value, [Midi, Midi.value], 0 or [0] for a rest.
    :param quarter_duration: int, float, Fraction, :obj:`~musicscore.quarterduration.QuarterDuration` for duration counted in quarters (crotchets). 0 for grace note (or chord).
    """
    _ATTRIBUTES = {'midis', 'quarter_duration', 'notes', 'offset', 'split', 'voice', 'clef', 'metronome', 'arpeggio'}

    def __init__(self, midis: Optional[Union[List[Union[float, int]], List[Midi], float, int, Midi]] = None,
                 quarter_duration: Optional[Union[float, int, 'Fraction', QuarterDuration]] = None, **kwargs):
        self._midis = None
        self._xml_direction_types = {'above': [], 'below': []}

        self._xml_directions = []
        self._xml_lyrics = []
        self._xml_articulations = []
        self._xml_technicals = []
        self._xml_ornaments = []
        self._xml_dynamics = []
        self._xml_other_notations = []
        self._note_attributes = kwargs
        self._notes_are_set = False
        self._clef = None
        self._metronome = None
        self._grace_chords = {'before': [], 'after': []}
        self._arpeggio = None
        self._after_notes_xml_objects = []
        super().__init__(quarter_duration=quarter_duration)
        self._set_midis(midis)
        self.split = False
        self._original_starting_ties = None

    def _add_articulation(self, articulation, placement=None):
        if articulation.__class__ not in XML_ARTICULATION_CLASSES:
            raise ChordAddXException(f'{articulation} is not an articulation object.')
        if placement:
            try:
                articulation.placement = placement
            except AttributeError:
                raise ChordAddXPlacementException(f'{articulation} has to placement attribute.')
        self._xml_articulations.append(articulation)
        if self.notes:
            self._update_xml_articulations()

    def _add_child(self, child: Note) -> Note:
        """
        Check and add child to list of children. Child's parent is set to self.

        :param child: :obj:`~musicscore.note.Note`
        :return: child
        :rtype: :obj:`~musicscore.note.Note`
        """
        return super().add_child(child)

    def _add_direction_type(self, direction_type, placement=None):
        if direction_type.__class__ in XML_DYNAMIC_CLASSES:
            d = XMLDynamics()
            d.add_child(direction_type)
            direction_type = d
        if direction_type.__class__ not in XML_DIRECTION_TYPE_CLASSES + XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS:
            raise ChordAddXException(f'{direction_type} is not a direction type object.')
        if placement:
            self.add_direction_type(direction_type, placement=placement)
        else:
            self.add_direction_type(direction_type)

    def _add_notation(self, notation, placement=None):
        if notation.__class__ in XML_DYNAMIC_CLASSES:
            d = XMLDynamics(placement=placement)
            d.add_child(notation)
            notation = d
        elif isinstance(notation, XMLFermata):
            if placement == 'above':
                notation.type = 'upright'
            elif placement == 'below':
                notation.type = 'inverted'
        elif notation.__class__ not in XML_OTHER_NOTATIONS + XML_ORNAMENT_AND_OTHER_NOTATIONS + XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS:
            raise ChordAddXException(f'{notation} is not a notation type object.')
        elif placement:
            raise ChordAddXPlacementException(
                f'Chord.add_x({notation}) of parent_type notations cannot have a placement argument.')

        self._xml_other_notations.append(notation)
        if self.notes:
            self._update_xml_other_notations()

    def _add_ornament(self, ornament, placement=None):
        if ornament.__class__ not in XML_ORNAMENT_CLASSES + XML_ORNAMENT_AND_OTHER_NOTATIONS:
            raise ChordAddXException(f'{ornament} is not an ornament type object.')
        if placement:
            try:
                ornament.placement = placement
            except AttributeError:
                raise ChordAddXPlacementException(f'{ornament} has to placement attribute.')
        self._xml_ornaments.append(ornament)
        if self.notes:
            self._update_xml_ornaments()

    def _add_technical(self, technical, placement=None):
        if technical.__class__ not in XML_TECHNICAL_CLASSES:
            raise ChordAddXException(f'{technical} is not a technical object.')
        if placement:
            try:
                technical.placement = placement
            except AttributeError:
                raise ChordAddXPlacementException(f'{technical} has to placement attribute.')
        self._xml_technicals.append(technical)
        if self.notes:
            self._update_xml_technicals()

    def _set_original_starting_ties(self, original_chord):
        self._original_starting_ties = [copy.copy(midi._ties) for midi in original_chord.midis]

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
            raise ValueError(
                'Chord cannot accept a mixed list of midis of rests and pitches or a list of more than one rests.')

        if 0 in midis and self.quarter_duration == 0:
            raise ValueError('A rest cannot be a grace note')
        self._midis = [Midi(v) if not isinstance(v, Midi) else v for v in midis]
        self._sort_midis()
        for midi in self._midis:
            midi._set_parent_chord(self)
        self._update_notes_pitch_or_rest()

    def _sort_midis(self):
        self._midis = sorted(self._midis)

    def _update_notes(self):
        if self._notes_are_set:
            raise ChordNotesAreAlreadyCreatedError()
        for index, midi in enumerate(self.midis):
            try:
                self.get_children()[index].midi = midi
            except IndexError:
                self._add_child(Note(midi=midi, **self._note_attributes))
        self._notes_are_set = True

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
                    new_note = Note(midi=m, quarter_duration=self.quarter_duration)
                    self._add_child(new_note)

    def _update_notes_quarter_duration(self):
        for note in self.notes:
            note.quarter_duration = self.quarter_duration

    def _update_ties(self):
        # _update ties of already created notes
        for note in self.notes:
            note._update_ties()

    def _update_xml_notations_arpeggiate(self):
        if self.arpeggio:
            for n in self.notes:
                if not n.xml_notations:
                    n.xml_notations = XMLNotations()
                if self.arpeggio != 'none':
                    n.xml_notations.xml_arpeggiate = XMLArpeggiate()
                    if self.arpeggio != 'normal' and n == self.notes[0]:
                        n.xml_notations.xml_arpeggiate.direction = self.arpeggio
                else:
                    if n == self.notes[0]:
                        n.xml_notations.xml_non_arpeggiate = XMLNonArpeggiate(type='bottom')
                    elif n == self.notes[-1]:
                        n.xml_notations.xml_non_arpeggiate = XMLNonArpeggiate(type='top')

    def _update_xml_articulations(self):
        def _get_note_xml_articulations():
            try:
                return n.xml_notations.xml_articulations.get_children(ordered=False)
            except AttributeError:
                return []

        n = self.notes[0]

        note_articulations_not_in_chord = [art for art in _get_note_xml_articulations() if art not in
                                           self._xml_articulations]
        chord_articulations_not_in_note = [art for art in self._xml_articulations if
                                           art not in _get_note_xml_articulations()]

        if chord_articulations_not_in_note:
            n.get_or_create_xml_notations()
            if not n.xml_notations.xml_articulations:
                n.xml_notations.xml_articulations = XMLArticulations()

            for xml_articulation in chord_articulations_not_in_note:
                n.xml_notations.xml_articulations.add_child(xml_articulation)

        for art in note_articulations_not_in_chord:
            n.xml_notations.xml_articulations.remove(art)
        n._update_xml_notations()

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
                if hasattr(direction_type, '__iter__') and direction_type[0] == 'dynamics':
                    _add_dynamics(list_of_dynamics=direction_type[1], xml_direction=d)
                else:
                    dt = d.add_child(XMLDirectionType())
                    dt.add_child(direction_type)

    def _update_xml_dynamics(self):
        def _get_note_xml_dynamics():
            try:
                return n.xml_notations.xml_dynamics.get_children(ordered=False)
            except AttributeError:
                return []

        n = self.notes[0]

        note_dynamics_not_in_chord = [art for art in _get_note_xml_dynamics() if art not in
                                      self._xml_dynamics]
        chord_dynamics_not_in_note = [art for art in self._xml_dynamics if art not in _get_note_xml_dynamics()]

        if chord_dynamics_not_in_note:
            n.get_or_create_xml_notations()
            if not n.xml_notations.xml_dynamics:
                n.xml_notations.xml_dynamics = XMLDynamics(**self._xml_dynamics_kwargs)

            for xml_dynamic in chord_dynamics_not_in_note:
                n.xml_notations.xml_dynamics.add_child(xml_dynamic)

        for d in note_dynamics_not_in_chord:
            n.xml_notations.xml_dynamics.remove(d)

        n._update_xml_notations()

    def _update_xml_metronome(self):
        if self.metronome:
            d = XMLDirection(placement='above')
            self._xml_directions.append(d)
            dt = d.add_child(XMLDirectionType())
            dt.add_child(self.metronome.xml_object)
            if self.metronome.sound:
                d.add_child(self.metronome.sound)

    def _update_xml_ornaments(self):
        def _get_note_xml_ornaments():
            try:
                return n.xml_notations.xml_ornaments.get_children(ordered=False)
            except AttributeError:
                return []

        n = self.notes[0]

        note_ornaments_not_in_chord = [o for o in _get_note_xml_ornaments() if o not in
                                       self._xml_ornaments]
        chord_ornaments_not_in_note = [o for o in self._xml_ornaments if o not in _get_note_xml_ornaments()]

        if chord_ornaments_not_in_note:
            n.get_or_create_xml_notations()
            if not n.xml_notations.xml_ornaments:
                n.xml_notations.xml_ornaments = XMLOrnaments()

            for xml_ornament in chord_ornaments_not_in_note:
                n.xml_notations.xml_ornaments.add_child(xml_ornament)

        for o in note_ornaments_not_in_chord:
            n.xml_notations.xml_ornaments.remove(o)

        n._update_xml_notations()

    def _update_xml_other_notations(self):
        def _get_note_xml_other_notations():
            try:
                return [ch for ch in n.xml_notations.get_children(ordered=False) if ch.__class__ in XML_OTHER_NOTATIONS]
            except AttributeError:
                return []

        n = self.notes[0]

        note_other_notations_not_in_chord = [on for on in _get_note_xml_other_notations() if on not in
                                             self._xml_other_notations]
        chord_other_notations_not_in_note = [on for on in self._xml_other_notations if
                                             on not in _get_note_xml_other_notations()]

        if chord_other_notations_not_in_note:
            n.get_or_create_xml_notations()
            for xml_other_notation in chord_other_notations_not_in_note:
                n.xml_notations.add_child(xml_other_notation)

        for on in note_other_notations_not_in_chord:
            n.xml_notations.remove(on)

        n._update_xml_notations()

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

        n._update_xml_notations()

    def _update_xml_lyrics(self):

        n = self.notes[0]

        note_lyrics_not_in_chord = [lyric for lyric in n.xml_object.find_children('XMLLyric') if lyric not in
                                    self._xml_lyrics]
        chord_lyrics_not_in_note = [lyric for lyric in self._xml_lyrics if
                                    lyric not in n.xml_object.find_children('XMLLyric')]

        if chord_lyrics_not_in_note:

            for xml_lyric in chord_lyrics_not_in_note:
                n.xml_object.add_child(xml_lyric)

        for lyric in note_lyrics_not_in_chord:
            n.xml_object.remove(lyric)

    def _update_xml_chord(self):
        for n in self.notes[1:]:
            if not n.xml_object.xml_chord:
                n.xml_object.add_child(XMLChord())

    # public properties
    @property
    def all_midis_are_tied_to_next(self):
        if set([m.is_tied_to_next for m in self.midis]) == {True}:
            return True
        else:
            return False

    @property
    def all_midis_are_tied_to_previous(self):
        if set([m.is_tied_to_previous for m in self.midis]) == {True}:
            return True
        else:
            return False

    @property
    def arpeggio(self):
        return self._arpeggio

    @arpeggio.setter
    def arpeggio(self, val):
        permitted = [None, 'normal', 'up', 'down', 'none']
        if val not in permitted:
            raise ValueError(f'arpeggio value {val} must be in permitted list: {permitted}')
        if self._finalized:
            raise AlreadyFinalizedError(self, 'arpeggio.setter')
        self._arpeggio = val

    @property
    def clef(self):
        return self._clef

    @clef.setter
    def clef(self, val):
        if not isinstance(val, Clef):
            raise TypeError
        self._clef = val

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
    def is_tied_to_previous(self):
        return self.all_midis_are_tied_to_previous

    @property
    def is_tied_to_next(self):
        return self.all_midis_are_tied_to_next

    @property
    def metronome(self):
        return self._metronome

    @metronome.setter
    def metronome(self, val):
        if not isinstance_as_string(val, 'Metronome'):
            raise TypeError
        self._metronome = val

    @property
    def midis(self) -> List['Midi']:
        """
        :return: list of midis

        >>> ch = Chord(midis=60)
        >>> [type(m) for m in ch.midis]
        [<class 'musicscore.midi.Midi'>]
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
        :return: :obj:`musicscore.chord.get_children` which are of type :obj:`musicscore.note.Note`.
        :rtype: List[:obj:`~musicscore.note.Note`]
        """
        return self.get_children()

    @property
    def offset(self) -> QuarterDuration:
        """
        :return: Offset in Chord's parent :obj:`~musicscore.beat.Beat`
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
            raise ChordQuarterDurationAlreadySetError(
                'Chord is already attached to a Beat. Quarter Duration cannot be changed any more.')
        if val is not None:
            if self.midis and self.is_rest and val == 0:
                raise ValueError('A rest cannot be a grace note')
            self._set_quarter_duration(val)
            if self._notes_are_set:
                self._update_notes_quarter_duration()

    @property
    def voice_number(self) -> int:
        """
        :return: Number of parent :obj:`~musicscore.voice.Voice`
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

    # public methods
    def add_after_note_xml_objects(self, xml_object):
        self._after_notes_xml_objects.append(xml_object)

    def add_direction_type(self, direction_type: XMLElement, placement: Optional[str] = None):
        if not placement:
            if isinstance(direction_type, XMLPedal) or isinstance(direction_type, XMLWedge):
                placement = 'below'
            else:
                placement = 'above'

        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_direction_type')
        if direction_type.__class__ not in XML_DIRECTION_TYPE_CLASSES + XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS:
            raise TypeError(
                f'Wrong type {direction_type}. Possible classes: {XML_DIRECTION_TYPE_CLASSES + XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS}')
        self._xml_direction_types[placement].append(direction_type)
        return direction_type

    def add_dynamics(self, dynamics: Union[List['Dynamics'], List['str'], 'Dynamics', str], placement: str = 'below') -> \
            List['Dynamics']:

        """
        This method is used to add one or more :obj:`musicscore.dynamics.Dynamics` objects to chord's private dictionary _xml_direction_types
        This list is used to create or _update directions of the first :obj:`~musicscore.note.Note` object of chord`s notes
        which are to be or are already created .

        :param dynamics: str, Dynamics of a list of Dynamics to be added to directions
        :param placement: above or below
        :return: List[:obj:`~musicscore.dynamics.Dynamics`]
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_dynamics')
        dynamics_list = [dynamics] if isinstance(dynamics, str) or not hasattr(dynamics, '__iter__') else list(
            dynamics)
        dynamics_object_list = [d if isinstance(d, Dynamics) else Dynamics(d) for d in dynamics_list]
        self._xml_direction_types[placement].append(('dynamics', dynamics_object_list))
        return dynamics_object_list

    def add_grace_chord(self, midis_or_grace_chord, type_=None, *, position=None):
        if self.up:
            raise ChordException(f'Chord {self} is already added to a measure. No grace chords can be added anymore.')
        if isinstance(midis_or_grace_chord, GraceChord):
            if type_:
                raise ValueError(f'Use GraceNote.type_ to set the type.')
            if position:
                raise ValueError(f'Use GraceNote.position to set the position.')
            gch = midis_or_grace_chord
        else:
            if not position:
                position = 'before'
            gch = GraceChord(midis_or_grace_chord, type_=type_, position=position)

        if gch.position == 'before':
            self._grace_chords['before'].append(gch)
        elif gch.position == 'after':
            self._grace_chords['after'].append(gch)
        gch.parent_chord = self
        return gch

    def add_tie(self, type_: str) -> None:
        """
        Chord's tie list is used to add ties to or _update ties of all midis and consequently :obj:`musicscore.note.Note`
        objects which are to be or are already created.

        :param type_: 'start' or 'stop'
        :return: None
        """

        for midi in self.midis:
            midi.add_tie(type_=type_)
        self._update_ties()

    def add_lyric(self, text: Union[Any, XMLLyric], **kwargs):
        """
        This method is used to add :obj:`~musicxml.xmlelement.xmlelement.XMLLyric` to chord's private _xml_lyricx list.
        This list is used to add lyrics to or _update lyrics of the first :obj:`~musicscore.note.Note` object of chord`s notes
        which are to be or are already created .

        :param text: if not of type :obj:`~musicxml.xmlelement.xmlelement.XMLLyric` a string conversion will be applied to text.
        :return: :obj:`~musicxml.xmlelement.xmlelement.XMLLyric`
        """
        if isinstance(text, XMLLyric):
            l = text
        else:
            l = XMLLyric(**kwargs)
            l.xml_text = str(text)
        self._xml_lyrics.append(l)
        if self.notes:
            self._update_xml_lyrics()
        return l

    def add_midi(self, midi):
        if self._notes_are_set:
            raise ChordNotesAreAlreadyCreatedError('Chord.add_midi cannot be used after creation of notes.')
        if not isinstance(midi, Midi):
            midi = Midi(midi)
        midi._set_parent_chord(self)
        self._midis.append(midi)
        self._sort_midis()
        return midi

    def add_wedge(self, wedge: Union['XMLWedge', str], placement: str = 'below') -> 'XMLWedge':
        """
        This method is used to add one :obj:`~musicxml.xmlelement.xmlelement.XMLWedge` object to chord's private
        dictionary _xml_direction_types This list is used to create or _update directions of the first
        :obj:`~musicscore.note.Note` object of chord`s notes which are to be or are already created .

        :param wedge: str, XMLWedge to be added to directions
        :param placement: above or below
        :return: :obj:`~musicxml.xmlelement.xmlelement.XMLWedge`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_wedge')
        wedge = XMLWedge(type=wedge) if isinstance(wedge, str) else wedge
        self.add_direction_type(wedge, placement=placement)
        return wedge

    def add_words(self, words: Union['XMLWords', str], placement: str = 'above', **kwargs) -> 'XMLWords':
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_words')

        if not isinstance(words, XMLWords):
            words = XMLWords(words, **kwargs)
        else:
            for key in kwargs:
                setattr(words, key, kwargs[key])
        return self.add_direction_type(words, placement=placement)

    def add_x(self, x: Union[_all_articulations, _all_technicals, _all_ornaments, _all_dynamics, _all_other_notations],
              *, placement=None, parent_type=None):
        """
        This method is used to add one xml object to a chord's private xml object lists (like _xml_articulations, xml_technicals
        etc.). These lists are used to add or _update articulations, technicals etc. of the first :obj:`~musicscore.note.Note` object of
        chord`s notes which are to be or are already created.

        :param x: musicxml articulation element, musicxml technical element, musicxml ornament element, musicxml dynamic element, musicxml other notations

        :return: x
        """
        if parent_type is None:
            if x.__class__ in XML_ARTICULATION_CLASSES:
                parent_type = 'articulation'
            elif x.__class__ in XML_TECHNICAL_CLASSES:
                parent_type = 'technical'
            elif x.__class__ in XML_ORNAMENT_CLASSES:
                parent_type = 'ornament'
            elif x.__class__ in XML_OTHER_NOTATIONS:
                parent_type = 'notation'
            elif x.__class__ in XML_DIRECTION_TYPE_CLASSES:
                parent_type = 'direction_type'
            elif x.__class__ in XML_ORNAMENT_AND_OTHER_NOTATIONS:
                permitted_parent_types = ['notation', 'ornament']
                raise NotationException(f'{x} is ambivalent. Set parent type {permitted_parent_types}.')
            elif x.__class__ in XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS or x.__class__ in XML_DYNAMIC_CLASSES:
                permitted_parent_types = ['notations', 'direction_type']
                raise NotationException(f'{x} is ambivalent. Set parent type {permitted_parent_types}.')
            else:
                raise ValueError(f'parent_type of {x} could not be determined.')

        if parent_type == 'articulation':
            self._add_articulation(x, placement=placement)
        elif parent_type == 'technical':
            self._add_technical(x, placement=placement)
        elif parent_type == 'ornament':
            self._add_ornament(x, placement=placement)
        elif parent_type == 'notation':
            self._add_notation(x, placement=placement)
        elif parent_type == 'direction_type':
            self._add_direction_type(x, placement=placement)
        else:
            raise NotImplementedError(f'parent_type: {parent_type} not implemented.')

        return x

    def finalize(self):
        """
        Finalize can be called only once. All necessary updates and xmlelement object creations will take place and the MusicTree
        object will be prepared for returning a musicxml snippet or a whole musicxml file.

        - Check if parent :obj:`~musicscore.beat.Beat` exists.
        - Ancestor :obj:`~musicscore.measure.Measure._update_divisions()` is called to _update :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure`'s :obj:`~musicxml.xmlelement.xmlelement.XMLDivisions` attribute.
        - Following updates are triggered: update_notes, update_xml_chord, update_notes_quarter_durations, update_xml_lyrics,
          update_xml_directions, update_xml_articulations, update_technicals
        """
        if self._finalized:
            raise AlreadyFinalizedError(self)

        if not self.up:
            raise ChordHasNoParentError('Chord needs a parent Beat to create notes.')

        self._update_notes()
        self._update_xml_chord()

        self._update_notes_quarter_duration()
        self._update_xml_lyrics()
        self._update_ties()
        self._update_xml_directions()
        self._update_xml_metronome()
        self._update_xml_articulations()
        self._update_xml_technicals()
        self._update_xml_ornaments()
        self._update_xml_dynamics()
        self._update_xml_other_notations()
        self._update_xml_notations_arpeggiate()
        self._finalized = True

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
            #     if m1.accidental.show != m2.accidental.show:
            #         return False
            if m1.accidental.get_pitch_parameters() != m2.accidental.get_pitch_parameters():
                return False
        return True

    def get_brackets(self):
        return self.get_x(XMLBracket)

    def get_children(self) -> List[Note]:
        """
        :return: list of added children.
        :rtype: List[:obj:`~musicscore.note.Note`]
        """
        return super().get_children()

    def get_grace_chords(self, position='before'):
        return self._grace_chords[position]

    def get_x(self, type_):
        if type_ == XMLDynamics:
            raise NotImplementedError(f'get_x of type_ {type_} not Implemented.')
        elif type_ in XML_DIRECTION_TYPE_CLASSES:
            output = []
            output += [x for x in self._xml_direction_types['above'] if isinstance(x, type_)]
            output += [x for x in self._xml_direction_types['below'] if isinstance(x, type_)]
            return output
        elif type_ in XML_ORNAMENT_CLASSES:
            return [x for x in self._xml_ornaments if isinstance(x, type_)]
        elif type_ in XML_TECHNICAL_CLASSES:
            return [x for x in self._xml_technicals if isinstance(x, type_)]
        elif type_ in XML_ARTICULATION_CLASSES:
            return [x for x in self._xml_articulations if isinstance(x, type_)]
        elif type_ in XML_OTHER_NOTATIONS:
            return [x for x in self._xml_other_notations if isinstance(x, type_)]
        elif type_ in XML_ORNAMENT_AND_OTHER_NOTATIONS:
            return [x for x in self._xml_ornaments if isinstance(x, type_)] + [x for x in
                                                                               self._xml_other_notations if
                                                                               isinstance(x, type_)]
        else:
            raise NotImplementedError(f'get_x of type_ {type_} not Implemented.')

    def get_parent(self) -> 'Beat':
        """
        :return: parent
        :rtype: :obj:`~musicscore.beat.Beat`
        """
        return super().get_parent()

    def get_parent_measure(self) -> 'Measure':
        """
        :return: parent measure
        """
        return self.up.up.up.up

    def get_slurs(self):
        return self.get_x(XMLSlur)

    def get_staff_number(self):
        try:
            return self.up.up.up.number
        except AttributeError:
            return None

    def get_voice(self):
        raise TypeError

    def get_voice_number(self) -> int:
        """
        :return: parent voice number
        :rtype: positive int
        """
        try:
            return self.up.up.number
        except AttributeError:
            return None

    def get_wedges(self):
        return self.get_x(XMLWedge)

    def get_words(self):
        return self.get_x(XMLWords)

    def set_possible_subdivisions(self):
        raise TypeError

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

        if voice.get_children()[
           voice.get_children().index(beats[0]): voice.get_children().index(beats[-1]) + 1] != beats:
            raise ChordCannotSplitError("Beats as Voice's children has another order as input list of beats")

        if beats[0] != voice.get_current_beat():
            raise ChordAlreadySplitError('First beat must be the next beat in voice which can accept chords.')
        if beats[-1] != voice.get_children()[-1]:
            raise ChordAlreadySplitError('Last beat must be the last beat in voice.')
        quarter_durations = self.quarter_duration.get_beatwise_sections(
            offset=beats[0].filled_quarter_duration, beats=beats)
        self.quarter_duration = quarter_durations[0][0]
        self.split = True

        if self._original_starting_ties is None:
            self._set_original_starting_ties(self)
        voice.get_current_beat().add_child(self)
        current_chord = self
        output = [self]
        for qd in quarter_durations[0][1:]:
            copied = _split_copy(self, qd)
            copied.split = True
            voice.get_current_beat().add_child(copied)

            current_chord.add_tie('start')
            copied.add_tie('stop')
            for midi in copied.midis:
                midi.accidental.show = False
            current_chord = copied
            output.append(current_chord)
        if quarter_durations[1]:
            # left over
            leftover_chord = _split_copy(self, quarter_durations[1])
            current_chord.add_tie('start')
            leftover_chord.add_tie('stop')
            for midi in leftover_chord.midis:
                midi.accidental.show = False
        else:
            leftover_chord = None
        self.up.up.leftover_chord = leftover_chord
        if not leftover_chord and output[-1]._original_starting_ties:
            for ties, midi in zip(output[-1]._original_starting_ties, output[-1].midis):
                if 'start' in ties:
                    midi.add_tie('start')
        if leftover_chord and leftover_chord._original_starting_ties:
            for ties, midi in zip(leftover_chord._original_starting_ties, leftover_chord.midis):
                if 'start' in ties:
                    midi.add_tie('start')
        return output

    def to_rest(self) -> None:
        """
        Set self.midis to [0]

        :return: None
        """
        self.midis = [0]

    def __setattr__(self, key, value):
        if key[0] != '_' and key not in self._ATTRIBUTES.union(self._TREE_ATTRIBUTES) and key not in self.__dict__:
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

    def __deepcopy__(self, memodict={}):
        '''
        Only midi and quarter_duration are deepcopied. _ties are copied.
        Not included in deepcopy at the moment:
        self._xml_direction_types
        self._xml_directions = []
        self._xml_lyrics = []
        self._xml_articulations = []
        self._xml_technicals = []
        self._xml_ornaments = []
        self._xml_dynamics = []
        self._xml_articulations_kwargs = {}
        self._xml_technicals_kwargs = {}
        self._xml_ornaments_kwargs = {}
        self._xml_dynamics_kwargs = {}
        self._xml_other_notations = []
        self._note_attributes = kwargs
        self.split
        '''
        if self._notes_are_set:
            raise DeepCopyException("After setting notes, Midi cannot be deepcopied anymore. ")
        copied = self.__class__(midis=[midi.__deepcopy__() for midi in self.midis],
                                quarter_duration=self.quarter_duration.__deepcopy__())
        return copied


class GraceChord(Chord):
    _ATTRIBUTES = Chord._ATTRIBUTES.union({'type_', 'parent_chord', 'position'})

    def __init__(self, midis: Optional[Union[List[Union[float, int]], List[Midi], float, int, Midi]] = None, *,
                 type_=None, position='before', **kwargs):
        super().__init__(midis=midis, quarter_duration=0, **kwargs)
        self._type = None
        self._position = None
        self.type_ = type_
        self.position = position

    @Chord.quarter_duration.setter
    def quarter_duration(self, val):
        if val != 0:
            raise ChordException('quarter_duration of a GraceChord is always 0 and cannot be set')
        else:
            self._quarter_duration = 0

    def _update_xml_type(self):
        for n in self.notes:
            n.xml_object.xml_type = self.type_

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        permitted = ['before', 'after']
        if val not in permitted:
            raise ValueError(f'Wrong position. Permitted are: {permitted}')
        else:
            self._position = val

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, val):
        if val is None:
            self._type = None
        else:
            if not isinstance(val, XMLType):
                self._type = XMLType(val)
            else:
                self._type = val

    def add_grace_chord(self, midis_or_grace_chord, type_=None, *, position=None):
        raise GraceChordCannotHaveGraceNotes

    def get_grace_chords(self, position='before'):
        raise GraceChordCannotHaveGraceNotes

    def finalize(self):
        super().finalize()
        self._update_xml_type()


class Rest(Chord):
    _ATTRIBUTES = Chord._ATTRIBUTES.union({'display_step', 'display_octave', 'measure'})

    def __init__(self, quarter_duration, display_step=None, display_octave=None, measure=None, **kwargs):
        if 'midis' in kwargs.keys():
            raise RestCannotSetMidiError
        super().__init__(midis=0, quarter_duration=quarter_duration, **kwargs)
        self._display_step = None
        self._display_octave = None
        self.display_step = display_step
        self.display_octave = display_octave
        self._measure = None
        self.measure = measure

    @property
    def display_step(self):
        return self._display_step

    @display_step.setter
    def display_step(self, val):
        permitted = [None, 'A', 'B', 'C', 'D', 'E', 'F', 'G']
        if val not in permitted:
            raise TypeError(f'display_step value {val} not in permitted list {permitted}')
        self._display_step = val

    @property
    def display_octave(self):
        return self._display_octave

    @display_octave.setter
    def display_octave(self, val):
        if val and (not isinstance(val, int) or val < 1):
            raise TypeError(f'display_octave value {val} can only be None or a positive integer. ')
        self._display_octave = val

    @property
    def measure(self):
        return self._measure

    @measure.setter
    def measure(self, val):
        self._measure = val

    def finalize(self):
        if self.display_step and not self.display_octave:
            raise RestWithDisplayStepHasNoDisplayOctave({self.display_step})

        if self.display_octave and not self.display_step:
            raise RestWithDisplayOctaveHasNoDisplayStep({self.display_octave})

        super().finalize()
        if self.display_step and self.display_octave:
            self.notes[0].xml_rest.xml_display_step = self.display_step
            self.notes[0].xml_rest.xml_display_octave = self.display_octave
        if self.measure:
            self.notes[0].xml_rest.measure = self.measure


def _split_copy(chord: Chord, new_quarter_duration: Union[QuarterDuration, Fraction, int, float] = None) -> Chord:
    """
    This function is used when a chord needs to be split. It creates a copy of the chord with a new quarter_duration object. All midis
    will be deepcopied. No attributes like lyrics, articulations etc. will be added to the copy.

    :param chord:
    :param new_quarter_duration: quarter_duration of copied chord. If None a shallow copy of chord.quarter_duration is created.
    :return: copied chord
    """
    if new_quarter_duration is None:
        new_quarter_duration = chord.quarter_duration.__copy__()
    new_chord = Chord(midis=[m._copy_for_split() for m in chord.midis], quarter_duration=new_quarter_duration)
    new_chord._original_starting_ties = chord._original_starting_ties
    return new_chord


def _group_chords(chords: List[Chord], quarter_durations: List[Union[QuarterDuration, Fraction, int, float]]) -> \
        Optional[List[List[Chord]]]:
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
