import copy
import warnings
from fractions import Fraction
from typing import Union, List, Optional, Any, Dict

from musicscore.clef import Clef
from musicscore.config import NUMBEROFBEAMS, TYPEDURATION
from musicscore.dynamics import Dynamics
from musicscore.exceptions import ChordAlreadySplitError, ChordCannotSplitError, ChordHasNoParentBeamError, \
    ChordQuarterDurationAlreadySetError, AlreadyFinalizedError, DeepCopyException, ChordException, NotationException, \
    ChordAddXException, ChordAddXPlacementException, RestCannotSetMidiError, \
    RestWithDisplayStepHasNoDisplayOctave, RestWithDisplayOctaveHasNoDisplayStep, GraceChordCannotHaveGraceNotesError, \
    GraceChordCannotSetQuarterDurationError, ChordHasNoNotesError, ChordAlreadyHasNotesError, ChordTestError, \
    ChordTypeNotSetError, ChordNumberOfDotsNotSetError, ChordParentBeamError
from musicscore.finalize import FinalizeMixin
from musicscore.midi import Midi
from musicscore.musictree import MusicTree
from musicscore.note import Note
from musicscore.quarterduration import QuarterDuration, QuarterDurationMixin
from musicscore.tuplet import Tuplet
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

_all_direction_types = Union[
    "XMLRehearsal", "XMLSegno", "XMLCoda", "XMLWords", "XMLSymbol", "XMLWedge", "XMLDashes", "XMLBracket", "XMLPedal",
    "XMLMetronome", "XMLOctaveShift", "XMLHarpPedals", "XMLDamp", "XMLDampAll", "XMLEyeglasses", "XMLStringMute", "XMLScordatura",
    "XMLPrincipalVoice", "XMLPercussion", "XMLAccordionRegistration", "XMLStaffDivide", "XMLOtherDirection"]


class Chord(MusicTree, QuarterDurationMixin, FinalizeMixin):
    """
    Parent type: :obj:`~musicscore.beat.Beat`

    Child type: :obj:`~musicscore.note.Note`

    Chord is a sequence of one or more :obj:`~musicxml.xmlelement.xmlelement.XMLNote`'s which occur at the same time in a :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure` of a :obj:`~musicxml.xmlelement.xmlelement.XMLPart`.

    :param midis: :obj:`~musicscore.midi.Midi`, Midi.value, [Midi, Midi.value], 0 or [0] for a rest.
    :param quarter_duration: int, float, Fraction, :obj:`~musicscore.quarterduration.QuarterDuration` for duration counted in quarters (crotchets). 0 for grace note (or chord).
    """
    _ATTRIBUTES = {'midis', 'quarter_duration', 'notes', 'offset', 'split', 'voice', 'clef', 'metronome', 'arpeggio',
                   'type', 'number_of_dots', 'tuplet', 'beams', 'broken_beam'}

    def __init__(self, midis: Union[List[Union[float, int]], List[Midi], float, int, Midi],
                 quarter_duration: Union[float, int, 'Fraction', QuarterDuration], **kwargs):
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
        self._after_notes_xml_elements = []
        self._beams = {}
        self._broken_beam = False
        self._type = None
        self._number_of_dots = None
        self._tuplet = None
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
                raise ChordAddXPlacementException(f'{articulation} has no placement attribute.')
        self._xml_articulations.append(articulation)
        if self.notes:
            self._update_xml_articulations()

    def _add_child(self, child: Note) -> Note:
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

    def _split_and_add_beatwise(self, beats: List['Beat']) -> List['Chord']:
        """
        This method is used to split the chord into a list of tied chords with proper quarter durations according to ``beats`` All beats must have the same :obj:`~musicscore.voice.Voice` parent and
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
        quarter_durations = self.quarter_duration._get_beatwise_sections(
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

    def _update_notes(self):
        if self._notes_are_set:
            raise ChordAlreadyHasNotesError('updating notes not possible.')
        for index, midi in enumerate(self.midis):
            self._add_child(Note(midi=midi, quarter_duration=self.quarter_duration, **self._note_attributes))
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

    def _update_xml_chord(self):
        for n in self.notes[1:]:
            if not n.xml_object.xml_chord:
                n.xml_object.add_child(XMLChord())

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

    # public properties
    @property
    def all_midis_are_tied_to_next(self) -> bool:
        """
        :return: ``True`` if the property :obj:`~musicscore.midi.Midi.is_tied_to_next` of all midi children of Chord are return ``True``, otherwise ``False``
        """
        if set([m.is_tied_to_next for m in self.midis]) == {True}:
            return True
        else:
            return False

    @property
    def all_midis_are_tied_to_previous(self) -> bool:
        """
        :return: ``True`` if the property :obj:`~musicscore.midi.Midi.is_tied_to_previous` of all midi children of Chord are return ``True``, otherwise ``False``
        """
        if set([m.is_tied_to_previous for m in self.midis]) == {True}:
            return True
        else:
            return False

    @property
    def arpeggio(self) -> str:
        """
        Set and get ``arpeggio`` value. Permitted values are ``None``, ``normal``, ``up``, ``down``, ``none``

        After finalizing:
          - ``none`` adds an :obj:`~musicxml.xmlelement.xmlelement.XMLNonArpeggiate` child to each :obj:`~musicscore.note.Note`'s :obj:`~musicxml.xmlelement.xmlelement.XMLNotations`
          - ``normal`` adds an :obj:`~musicxml.xmlelement.xmlelement.XMLArpeggiate` child to each :obj:`~musicscore.note.Note`'s :obj:`~musicxml.xmlelement.xmlelement.XMLNotations`
          - ``up`` adds an :obj:`~musicxml.xmlelement.xmlelement.XMLArpeggiate` child with direction ``up`` to each :obj:`~musicscore.note.Note`'s :obj:`~musicxml.xmlelement.xmlelement.XMLNotations`
          - ``down`` adds an :obj:`~musicxml.xmlelement.xmlelement.XMLArpeggiate` child with direction ``down`` to each :obj:`~musicscore.note.Note`'s :obj:`~musicxml.xmlelement.xmlelement.XMLNotations`
        """
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
    def beams(self):
        """
        A dictionary like: {1:'continue', 2:'begin'}. Keys are beam numbers. Default is {}. :obj:`~musicscore.beam.Beam._update_chord_beams` sets a beam only if beam is not None and beam is not set manually.
        """
        return self._beams

    @beams.setter
    def beams(self, val):
        self._beams = val

    @property
    def broken_beam(self):
        """
        If true the beam will be broken at this position
        """
        return self._broken_beam
    
    @broken_beam.setter
    def broken_beam(self, val):
        self._broken_beam = val

    @property
    def clef(self) -> 'Clef':
        """
        Set or get :obj:`~musicscore.clef.Clef` object to be added to :obj:`~musicscore.measure.Measure` before this :obj:`~musicscore.chord.Chord`
        """
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
        """
        Same as :obj:`~all_midis_are_tied_to_previous`
        """
        return self.all_midis_are_tied_to_previous

    @property
    def is_tied_to_next(self):
        """
        Same as :obj:`~all_midis_are_tied_to_next`
        """
        return self.all_midis_are_tied_to_next

    @property
    def metronome(self):
        """
        Get and set the :obj:`~musicscore.metronome.Metronome` object associated with this :obj:`~musicscore.chord.Chord`
        """
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

        >>> ch = Chord(quarter_duration=1, midis=60)
        >>> [type(m) for m in ch.midis]
        [<class 'musicscore.midi.Midi'>]
        >>> [m.value for m in ch.midis]
        [60]
        >>> ch = Chord(quarter_duration=1,midis=[60, Midi(40)])
        >>> [m.value for m in ch.midis]
        [40, 60]
        >>> Chord(quarter_duration=1, midis=[0, 60])
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
    def number_of_beams(self) -> Optional[int]:
        if not self.type:
            raise ChordTypeNotSetError('Number of beams cannot be determined if chord.type is not set.')
        output = NUMBEROFBEAMS.get(self.type)
        if not output:
            return 0
        else:
            return output

    @property
    def number_of_dots(self) -> int:
        """
        Set and get number of dots to be added to the notes. If not set manually ~:obj:`musicscore.beat.Beat.finalize()` will set it usually via calling ~:obj:`~musicscore.quarterduration.QuarterDuration.get_number_of_dots()`.
        """
        return self._number_of_dots

    @number_of_dots.setter
    def number_of_dots(self, val):
        if self._notes_are_set and val != self._number_of_dots:
            raise ChordAlreadyHasNotesError('After creating Notes it is not possible to change number of dots.')
        if not isinstance(val, int):
            raise TypeError()
        if val < 0:
            raise ValueError
        self._number_of_dots = val

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

    @property
    def tuplet(self) -> Optional['Tuplet']:
        return self._tuplet

    @tuplet.setter
    def tuplet(self, val):
        if val is not None and not isinstance(val, Tuplet):
            raise TypeError
        self._tuplet = val

    @property
    def type(self) -> Optional[str]:
        """
        Set and get ```XMLNoteType.value_``` associated with this chord. If not set manually ~:obj:`musicscore.beat.Beat.finalize()` will set it usually via calling ~:obj:`~musicscore.quarterduration.QuarterDuration.get_type()`.  ~:obj:`~musicscore.quarterduration.QuarterDuration` ``0`` returns ``None``.
        :param val: [‘1024th’, ‘512th’, ‘256th’, ‘128th’, ‘64th’, ‘32nd’, ‘16th’, ‘eighth’, ‘quarter’, ‘half’, ‘whole’, ‘breve’, ‘long’, ‘maxima’]
        """
        return self._type

    @type.setter
    def type(self, val):
        permitted = ['1024th', '512th', '256th', '128th', '64th', '32nd', '16th', 'eighth', 'quarter', 'half', 'whole',
                     'breve', 'long', 'maxima']
        if self._notes_are_set and val != self._type:
            raise ChordAlreadyHasNotesError('After creating Notes it is not possible to change the type.')
        if val is not None and val not in permitted:
            raise ValueError(f'Chord.type can only be None or {permitted}')
        self._type = val

    @QuarterDurationMixin.quarter_duration.setter
    def quarter_duration(self, val):
        if self._notes_are_set:
            raise ChordAlreadyHasNotesError('quarter duration of the chord cannot be changed anymore.')
        if self._quarter_duration is not None and self.up:
            raise ChordQuarterDurationAlreadySetError(
                'Chord is already attached to a Beat. Quarter Duration cannot be changed any more.')
        if val is not None:
            if self.midis and self.is_rest and val == 0:
                raise ValueError('A rest cannot be a grace note')
            self._set_quarter_duration(val)

    @property
    def voice_number(self) -> int:
        """
        :return: Number of parent :obj:`~musicscore.voice.Voice`
        :rtype: positive int
        """
        if not self.up:
            raise ChordHasNoParentBeamError()
        if self.up and self.up.up:
            return self.up.up.number
        else:
            return 1

    @property
    def xml_articulations(self) -> List[_all_articulations]:
        """
        :return: list of xml articulations to be added to this :obj:`~musicscore.chord.Chord` during finalization.
        """
        return self._xml_articulations

    @property
    def xml_direction_types(self) -> Dict:
        """
        :return: dict of xml direction types to be added to this :obj:`~musicscore.chord.Chord` during finalization.
        """
        return self._xml_direction_types

    @property
    def xml_lyrics(self) -> List['XMLLyric']:
        """
        :return: list of xml lyrics to be added to this :obj:`~musicscore.chord.Chord` during finalization.
        """
        return self._xml_lyrics

    @property
    def xml_technicals(self) -> List[_all_technicals]:
        """
        :return: list of xml technicals to be added to this :obj:`~musicscore.chord.Chord` during finalization.
        """
        return self._xml_technicals

    # public methods
    def add_after_note_xml_objects(self, xml_element):
        """
        .. deprecated:: 2.0.2
            This method is deprecated.
            Use :obj:`add_xml_element_after_notes()` instead.
        """
        warnings.warn("This method is deprecated. Use add_xml_element_after_notes() instead.")
        return self.add_xml_element_after_notes(xml_element)

    def add_direction_type(self, direction_type: XMLElement, placement: Optional[str] = None):
        """
        Adds a :obj:`~musicxml.xmlelement.xmlelement.XMLDirectionType` to a private dictionary ``_xml_direction_types`` with placement keys: ``below`` and ``above``. This dictionary is used during the finalization to add :obj:`~musicxml.xmlelement.xmlelement.XMLDirection` objects to :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure` before this :obj:`~musicscore.chord.Chord`

        .. seealso::
           :obj:`~add_x`


        :param direction_type: Permitted direction types are found in :obj:`~musicscore.util.XML_DIRECTION_TYPE_CLASSES` and :obj:`~musicscore.util.XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS`
        :param placement: ``None``, ``below``, ``above``
        :return: added direction_type
        """
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
        This method is used to add one or more :obj:`musicscore.dynamics.Dynamics` objects to chord's private dictionary ``_xml_direction_types``

        .. seealso::
           :obj:`~add_direction_type`
           :obj:`~add_x`


        :param dynamics: str, :obj:`~musicscore.dynamics.Dynamics` of a list of Dynamics to be added to directions
        :param placement: ``above`` or ``below``
        :return: List[:obj:`~musicscore.dynamics.Dynamics`]
        :exception: :obj:`~musicscore.exceptions.AlreadyFinalizedError`
        """

        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_dynamics')
        dynamics_list = [dynamics] if isinstance(dynamics, str) or not hasattr(dynamics, '__iter__') else list(
            dynamics)
        dynamics_object_list = [d if isinstance(d, Dynamics) else Dynamics(d) for d in dynamics_list]
        self._xml_direction_types[placement].append(('dynamics', dynamics_object_list))
        return dynamics_object_list

    def add_grace_chord(self, midis_or_grace_chord: Union[
        'Midi', List['Midi'], int, float, List[Union[int, float]], 'GraceChord'],
                        type: Optional[str] = None, *, position: Optional[str] = None):
        """
        This method is used to add :obj:`~musicscore.midi.Midi`'s or :obj:`~musicscore.chord.GraceChord` object to the private dictionary ``_grace_chords`` with two position kyes ``before`` and ``after``. The midis or grace chords will be positioned in :obj:`~musicscore.measure.Measure` before or after this :obj:`~musicscore.chord.Chord`

        A :obj:`~musicscore.chord.GraceChord` or a :obj:`~musicscore.chord.Chord` with :obj:`~musicscore.chord.Chord.quarter_duration` ``0`` can be added directly to a :obj:`~musicscore.beat.Beat` too.

        :param midis_or_grace_chord: :obj:`~musicscore.midi.Midi`'s or :obj:`~musicscore.chord.GraceChord`

        :param type: :obj:`~musicscore.chord.GraceChord.type` value of the :obj:`~musicscore.chord.GraceChord` to be created if ``midis_or_grace_chord`` is a list of midis. It specifices the not type of the grace note. For permitted values see: :obj:`~musicxml.xmlelement.xmlelement.XMLType`

        :param position: ``None``, ``before``, ``after``. :obj:`~musicscore.chord.GraceChord.position` value of the :obj:`musicscore.chord.GraceChord` to be created if ``midis_or_grace_chord`` is a list of midis.

        .. caution::
           ``midis_or_grace_chord`` is of type :obj:`~musicscore.chord.GraceChord`, use :obj:`musicscore.chord.GraceChord.type` for setting its note type and :obj:`musicscore.chord.GraceChord.position` for setting its position instead of using type and position arguments.

        """
        if self.up:
            raise ChordException(f'Chord {self} is already added to a measure. No grace chords can be added anymore.')
        if isinstance(midis_or_grace_chord, GraceChord):
            if type:
                raise ValueError(f'Use GraceNote.type to set the type.')
            if position:
                raise ValueError(f'Use GraceNote.position to set the position.')
            gch = midis_or_grace_chord
        else:
            if not position:
                position = 'before'
            gch = GraceChord(midis_or_grace_chord, type=type, position=position)

        if gch.position == 'before':
            self._grace_chords['before'].append(gch)
        elif gch.position == 'after':
            self._grace_chords['after'].append(gch)
        gch.parent_chord = self
        return gch

    def add_lyric(self, text: Union[Any, XMLLyric], **kwargs) -> XMLLyric:
        """
        This method is used to add :obj:`~musicxml.xmlelement.xmlelement.XMLLyric` to chord's private ``_xml_lyrics`` list.
        This list is used to add lyrics the first :obj:`~musicscore.note.Note` object of chord`s notes during finalization.

        :param text: if not of type :obj:`~musicxml.xmlelement.xmlelement.XMLLyric` a string conversion will be applied to text.
        :parm kwargs: passed on to :obj:`~musicxml.xmlelement.xmlelement.XMLLyric` if it has to be created.
        :return: added :obj:`~musicxml.xmlelement.xmlelement.XMLLyric`
        :exception: :obj:`~musicscore.exceptions.AlreadyFinalizedError`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_lyric')

        if isinstance(text, XMLLyric):
            l = text
        else:
            l = XMLLyric(**kwargs)
            l.xml_text = str(text)
        self._xml_lyrics.append(l)
        return l

    def add_midi(self, midi: Union[float, int, 'Midi']) -> 'Midi':
        """
        This method adds a new :obj:`~musicscore.midi.Midi` to the chord and sorts its midis afterwards.

        :param: a :obj:`~musicscore.midi.Midi` or a valid midi value.
        :return: added :obj:`~musicscore.midi.Midi`
        :exception: :obj:`~musicscore.exceptions.AlreadyFinalizedError`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_midi')
        if not isinstance(midi, Midi):
            midi = Midi(midi)
        midi._set_parent_chord(self)
        self._midis.append(midi)
        self._sort_midis()
        return midi

    def add_tie(self, type: str) -> None:
        """
        Chord's tie list is used to add ties to or _update ties of all midis and consequently :obj:`musicscore.note.Note`
        objects which are to be or are already created.

        :param type: ``start`` or ``stop``
        :return: None
        """

        for midi in self.midis:
            midi.add_tie(type=type)
        self._update_ties()

    def add_wedge(self, wedge: Union['XMLWedge', str], placement: str = 'below') -> 'XMLWedge':
        """
        This method is used to add one or more :obj:`~musicxml.xmlelement.xmlelement.XMLWedge` objects to chord's private dictionary ``_xml_direction_types``

        .. seealso::
           :obj:`~add_direction_type`
           :obj:`~add_x`
           :obj:`~musicscore.util.wedge_chords`

        :param wedge: str, :obj:`~musicxml.xmlelement.xmlelement.XMLWedge` to be added to directions
        :param placement: ``above`` or ``below``
        :return: added :obj:`~musicxml.xmlelement.xmlelement.XMLWedge`
        :exception: :obj:`~musicscore.exceptions.AlreadyFinalizedError`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_wedge')
        wedge = XMLWedge(type=wedge) if isinstance(wedge, str) else wedge
        return self.add_direction_type(wedge, placement=placement)

    def add_words(self, words: Union['XMLWords', str], placement: str = 'above', **kwargs) -> 'XMLWords':
        """
        This method is used to add one or more :obj:`~musicxml.xmlelement.xmlelement.XMLWords` objects to chord's private dictionary ``_xml_direction_types``

        .. seealso::
           :obj:`~add_direction_type`
           :obj:`~add_x`

        :param words: str, :obj:`~musicxml.xmlelement.xmlelement.XMLWords` to be added to directions
        :param placement: ``above`` or ``below``
        :param kwargs:  passed on to :obj:`~musicxml.xmlelement.xmlelement.XMLWords` if it has to be created.
        :return: added :obj:`~musicxml.xmlelement.xmlelement.XMLWords`
        :exception: :obj:`~musicscore.exceptions.AlreadyFinalizedError`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_words')

        if not isinstance(words, XMLWords):
            words = XMLWords(words, **kwargs)
        else:
            for key in kwargs:
                setattr(words, key, kwargs[key])
        return self.add_direction_type(words, placement=placement)

    def add_x(self, x: Union[
        _all_articulations, _all_technicals, _all_ornaments, _all_dynamics, _all_other_notations, _all_direction_types],
              *, placement: str = None, parent_type: str = None) -> 'XMLElement':
        """
        This method is used to add one :obj:`~musicxml.xmlelement.xmlelement.XMLElement` object to a chord's private xml object lists (like _xml_articulations, xml_technicals
        etc.). These lists are used to add or update articulations, technicals etc. of the first :obj:`~musicscore.note.Note` object of
        chord`s notes which are to be or are already created. In case of direction types the object is added before the first note to the measure.

        .. seealso::
            :obj:`~add_direction_type`
            :obj:`~musicscore.util.bracket_chords`
            :obj:`~musicscore.util.octave_chords`
            :obj:`~musicscore.util.slur_chords`
            :obj:`~musicscore.util.trill_chords`
            :obj:`~musicscore.util.wedge_chords`

        :param x: MusicXML articulation, technical, ornament, dynamics, other notations or direction type element.
        :param placement: ``None``, ``above``, ``below``. If this value is set and x does not accept placement an error is raised.
        :param parent_type: ``None, ``articulation``, ``technical``, ``ornament``, ``notation``, ``direction_type``. If ``None`` the right parent type will be tried to determined. If x's parent is ambivalent an error is raised.
        :return: added ``x``
        :exception: :obj:`~musicscore.exceptions.NotationException`, :obj:`~musicscore.exceptions.ChordAddXPlacementException`, :obj:`~musicscore.exceptions.ChordAddXException`

        .. seealso::
            :obj:`~musicscore.util.XML_ARTICULATION_CLASSES`
            :obj:`~musicscore.util.XML_TECHNICAL_CLASSES`
            :obj:`~musicscore.util.XML_ORNAMENT_CLASSES`
            :obj:`~musicscore.util.XML_OTHER_NOTATIONS`
            :obj:`~musicscore.util.XML_DIRECTION_TYPE_CLASSES`
            :obj:`~musicscore.util.XML_ORNAMENT_AND_OTHER_NOTATIONS`
            :obj:`~musicscore.util.XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS`
            :obj:`~musicscore.util.XML_DYNAMIC_CLASSES`

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

    def add_xml_element_after_notes(self, xml_element: XMLElement) -> XMLElement:
        """
        This method adds an :obj:`~musicxml.xmlelement.xmlelement.XMLElement` to a list of elements to be added to :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure` during finalization after adding this :obj:`~musicscore.chord.Chord`'s :obj:`~musicscore.note.Note`'s to it.

        :param: :obj:`~musicxml.xmlelement.xmlelement.XMLElement` to be added after :obj:`~musicxml.xmlelement.xmlelement.XMLNotes`'s to :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure`
        :return: added :obj:`~musicxml.xmlelement.xmlelement.XMLElement`

        """
        self._after_notes_xml_elements.append(xml_element)
        return xml_element

    def break_beam(self):
        self.broken_beam = True

    def check_number_of_beams(self):
        if self.type is None:
            raise ChordTypeNotSetError('Chord.type must be set before testing its number of beams.')
        if self.beams:
            if self.number_of_beams == 0:
                raise ChordTestError(f'Chord with number_of_beams 0 cannot have any beams.')
            else:
                diff = set(range(1, self.number_of_beams + 1)).difference(set(self.beams.keys()))
                if diff:
                    raise ChordTestError(
                        f'Chord with number_of_beams {self.number_of_beams} has wrong beam numbers as keys of its beams dictionary. Diff: {diff}.')
                try:
                    max_num = max(self.beams.keys())
                except ValueError:
                    max_num = 0
                if max_num != self.number_of_beams:
                    raise ChordTestError(
                        f'Chord with number_of_beams {self.number_of_beams} must set same number of beams in its beams dictionary ({max_num} are set.).')
        return True

    def check_printed_duration(self):
        if not self.get_parent():
            raise ChordHasNoParentBeamError(
                ('Chord needs information of its parent beat before testing its quarter duration.'))
        beat_quarter_duration = self.get_parent().quarter_duration
        beat_subdivision = self.get_parent().get_subdivision()
        if beat_quarter_duration is None:
            raise ChordParentBeamError('Parent beat quarter duration is None.')
        if beat_subdivision is None:
            raise ChordParentBeamError('Parent beat subdivision is None.')
        if self.type is None:
            raise ChordTypeNotSetError('Chord.type must be set before testing its quarter duration.')
        if self.number_of_dots is None:
            raise ChordNumberOfDotsNotSetError('Chord.number_of_dots must be set before testing its quarter duration.')

        self.quarter_duration.beat_quarter_duration = beat_quarter_duration
        self.quarter_duration.beat_subdivision = beat_subdivision
        tuplet_ratio = self.quarter_duration.get_tuplet_ratio()
        if tuplet_ratio:
            if not self.tuplet:
                raise ChordTestError(f'Chord has a tuplet ratio of {tuplet_ratio} but its tuplet property is not set.')
            else:
                if self.tuplet.ratio != tuplet_ratio:
                    raise ChordTestError(
                        f'Chord has a tuplet ratio of {tuplet_ratio} but its tuplet property has ratio {self.tuplet.ratio}.')

        if tuplet_ratio:
            ratio = Fraction(tuplet_ratio[1], tuplet_ratio[0])
        else:
            ratio = 1
        printed_duration = QuarterDuration(TYPEDURATION[self.type])
        for i in range(self.number_of_dots):
            printed_duration += printed_duration / 2
        printed_duration *= ratio
        if printed_duration == self.quarter_duration:
            return True
        else:
            raise ChordTestError(f'printed duration {printed_duration} != quarter duration {self.quarter_duration}')

    def finalize(self):
        """
        Finalize can be called only once. All necessary updates and xmlelement object creations will take place and the MusicTree
        object will be prepared for returning a musicxml snippet or a whole musicxml file.

        - Check if parent :obj:`~musicscore.beat.Beat` exists.
        - Ancestors :obj:`~musicscore.measure.Measure._update_divisions()` is called to update :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure`'s :obj:`~musicxml.xmlelement.xmlelement.XMLDivisions` attribute.
        - Following updates are triggered: _update_notes, _update_xml_chord, _update_notes_quarter_durations, _update_xml_lyrics, _update_ties, _update_xml_directions, _update_xml_metronome, _update_xml_articulations, _update_technicals, _update_xml_ornaments, _update_xml_dynamics, _update_xml_other_notations, _update_xml_notations_arpeggiate
        """
        if self._finalized:
            raise AlreadyFinalizedError(self)

        if not self.up:
            raise ChordHasNoParentBeamError('Chord needs a parent Beat to create notes.')

        self._update_notes()
        self._update_xml_chord()
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

    def get_brackets(self) -> List["XMLBracket"]:
        """
        Get :obj:`~musicxml.xmlelement.xmlelement.XMLBracket` objects associated with this :obj:`~musicscore.chord.Chord`

        .. seealso::
          :obj:`~get_x()`


        :return: list of :obj:`~musicxml.xmlelement.xmlelement.XMLBracket`
        """
        return self.get_x(XMLBracket)

    def get_grace_chords(self, position: str = 'before') -> List["GraceChord"]:
        """
        Get :obj:`~musicscore.chord.GraceChord` objects associated with this :obj:`~musicscore.chord.Chord`

        :param position: ``before``, ``after``
        :return: list of positioned :obj:`~musicscore.chord.GraceChord`
        """

        return self._grace_chords[position]

    def get_x(self, type: "type") -> List[Union[
        _all_articulations, _all_technicals, _all_ornaments, _all_dynamics, _all_other_notations, _all_direction_types]]:

        """
        Get different direction_type, ornament, technical, articulation, dynamics or other notations objects objects associated with this :obj:`~musicscore.chord.Chord`

        .. seealso::
           :obj:`~add_x()`

        :param type: type of XMLElement to look for.
        """
        if type == XMLDynamics:
            raise NotImplementedError(f'get_x of type {type} not Implemented.')
        elif type in XML_DIRECTION_TYPE_CLASSES:
            output = []
            output += [x for x in self._xml_direction_types['above'] if isinstance(x, type)]
            output += [x for x in self._xml_direction_types['below'] if isinstance(x, type)]
            return output
        elif type in XML_ORNAMENT_CLASSES:
            return [x for x in self._xml_ornaments if isinstance(x, type)]
        elif type in XML_TECHNICAL_CLASSES:
            return [x for x in self._xml_technicals if isinstance(x, type)]
        elif type in XML_ARTICULATION_CLASSES:
            return [x for x in self._xml_articulations if isinstance(x, type)]
        elif type in XML_OTHER_NOTATIONS:
            return [x for x in self._xml_other_notations if isinstance(x, type)]
        elif type in XML_ORNAMENT_AND_OTHER_NOTATIONS:
            return [x for x in self._xml_ornaments if isinstance(x, type)] + [x for x in
                                                                              self._xml_other_notations if
                                                                              isinstance(x, type)]
        else:
            raise NotImplementedError(f'get_x of type {type} not Implemented.')

    def get_next_in_part(self) -> Optional["Chord"]:
        """
        Get the next chord in part with same voice and staff number

        :raises: ~:obj:`~musicscore.exceptions.ChordHasNoParentPartError`
        """
        pass

    def get_parent_measure(self) -> 'Measure':
        """
        :return: parent :obj:`~musicscore.measure.Measure`
        """
        return self.up.up.up.up

    def get_slurs(self) -> List["XMLSlur"]:
        """
        Get :obj:`~musicxml.xmlelement.xmlelement.XMLSlur` objects associated with this :obj:`~musicscore.chord.Chord`

        .. seealso::
          :obj:`~get_x()`

        :return: list of :obj:`~musicxml.xmlelement.xmlelement.XMLSlur`
        """
        return self.get_x(XMLSlur)

    def get_staff_number(self) -> Optional[int]:
        """
        :return: number of parent :obj:`~musicscore.staff.Staff`
        """
        try:
            return self.up.up.up.number
        except AttributeError:
            return None

    def get_voice(self):
        raise TypeError

    def get_voice_number(self) -> Optional[int]:
        """
        :return: number of parent :obj:`~musicscore.voice.Voice`
        """
        try:
            return self.up.up.number
        except AttributeError:
            return None

    def get_wedges(self) -> List["XMLWedge"]:
        """
        Get :obj:`~musicxml.xmlelement.xmlelement.XMLWedge` objects associated with this :obj:`~musicscore.chord.Chord`

        .. seealso::
          :obj:`~get_x()`


        :return: list of :obj:`~musicxml.xmlelement.xmlelement.XMLWedge`
        """
        return self.get_x(XMLWedge)

    def get_words(self) -> List["XMLWords"]:
        """
        Get :obj:`~musicxml.xmlelement.xmlelement.XMLWords` objects associated with this :obj:`~musicscore.chord.Chord`

        .. seealso::
          :obj:`~get_x()`


        :return: list of :obj:`~musicxml.xmlelement.xmlelement.XMLWords`
        """
        return self.get_x(XMLWords)

    def has_same_pitches(self, other: 'Chord') -> bool:
        """
        Only for chords with pitches. Rest chords cannot use this method.

        :param other: Other chord to which the comparison takes place
        :return: ``True`` if pitches of self and other chord has the same pitch parameters and accidental values else ``False``
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

    def set_possible_subdivisions(self):
        raise TypeError

    def set_beam(self, number, value):
        self._beams[number] = value

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
    """
    .. seealso::
       :obj:`~Chord` for inherited methods and properties

    """
    _ATTRIBUTES = Chord._ATTRIBUTES.union({'parent_chord', 'position'})

    def __init__(self, midis: Union[List[Union[float, int]], List[Midi], float, int, Midi], *,
                 type=None, position='before', **kwargs):
        if 'quarter_duration' in kwargs.keys():
            raise GraceChordCannotSetQuarterDurationError(
                'quarter_duration of a GraceChord is always 0 and cannot be set')
        super().__init__(midis=midis, quarter_duration=0, **kwargs)
        self._position = None
        self.type = type
        self.position = position

    @Chord.quarter_duration.getter
    def quarter_duration(self) -> QuarterDuration:
        """
        Is always zero and Cannot be set.
        :exception: :obj:`~musicscore.exceptions.GraceChordCannotSetQuarterDurationError`
        """
        return super().quarter_duration

    @Chord.quarter_duration.setter
    def quarter_duration(self, val):
        if val != 0:
            raise GraceChordCannotSetQuarterDurationError(
                'quarter_duration of a GraceChord is always 0 and cannot be set')
        else:
            self._quarter_duration = QuarterDuration(0)

    @property
    def position(self):
        """
        Set and get position (``before``, ``after``) of this :obj:`~musicscore.chord.GraceChord`. It is relevant if it would be added to a :obj:`~musicscore.chord.Chord`.

        .. seealso::
           :obj:`musicscore.chord.Chord.add_grace_chord()`
        """
        return self._position

    @position.setter
    def position(self, val):
        permitted = ['before', 'after']
        if val not in permitted:
            raise ValueError(f'Wrong position. Permitted are: {permitted}')
        else:
            self._position = val

    def add_grace_chord(self, midis_or_grace_chord, type=None, *, position=None):
        """
        :exception: :obj:`~musicscore.exceptions.GraceChordCannotHaveGraceNotesError`
        """
        raise GraceChordCannotHaveGraceNotesError

    def get_grace_chords(self, position='before'):
        """
        :exception: :obj:`~musicscore.exceptions.GraceChordCannotHaveGraceNotesError`
        """
        raise GraceChordCannotHaveGraceNotesError


class Rest(Chord):
    """
    .. seealso::
      :obj:`~Chord` for inherited methods and properties
    """
    _ATTRIBUTES = Chord._ATTRIBUTES.union({'display_step', 'display_octave', 'measure'})

    def __init__(self, quarter_duration, display_step=None, display_octave=None, measure=None, **kwargs):
        if 'midis' in kwargs.keys():
            raise RestCannotSetMidiError('midis value of a GraceChord is always 0 and cannot be set')
        super().__init__(midis=0, quarter_duration=quarter_duration, **kwargs)
        self._display_step = None
        self._display_octave = None
        self.display_step = display_step
        self.display_octave = display_octave
        self._measure = None
        self.measure = measure

    @property
    def display_step(self):
        """
        Set and get  :obj:`~musicxml.xmlelement.xmlelement.XMLDisplayStep` child of :obj:`~musicxml.xmlelement.xmlelement.XMLRest`.
        Permitted values are ``None``, ``A``, ``B``, ``C``, ``D``, ``E``, ``F``, ``G``
        """
        return self._display_step

    @display_step.setter
    def display_step(self, val):
        permitted = [None, 'A', 'B', 'C', 'D', 'E', 'F', 'G']
        if val not in permitted:
            raise TypeError(f'display_step value {val} not in permitted list {permitted}')
        self._display_step = val

    @property
    def display_octave(self):
        """
        Set and get :obj:`~musicxml.xmlelement.xmlelement.XMLDisplayOctave` child of :obj:`~musicxml.xmlelement.xmlelement.XMLRest`.
        Permitted are ``None`` and positive int
        """
        return self._display_octave

    @display_octave.setter
    def display_octave(self, val):
        if val and (not isinstance(val, int) or val < 1):
            raise TypeError(f'display_octave value {val} can only be None or a positive integer. ')
        self._display_octave = val

    @property
    def measure(self):
        """
        Set or get measure attribute of :obj:`~musicxml.xmlelement.xmlelement.XMLRest`.
        Permitted values are ``None``, ``yes`` and ``no``. If ``yes``, this indicates this is a complete measure rest.

        """
        return self._measure

    @measure.setter
    def measure(self, val):
        self._measure = val

    @Chord.midis.getter
    def midis(self) -> List['Midi']:
        """
        Is always zero and Cannot be set.
        :exception: :obj:`~musicscore.exceptions.RestCannotSetMidiError`
        """
        return super().midis

    @Chord.midis.setter
    def midis(self, val):

        if val != 0:
            raise RestCannotSetMidiError('midis value of a GraceChord is always 0 and cannot be set')
        else:
            self._midis = 0

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
        raise ValueError(
            f'chords quarter durations ({[c.quarter_duration for c in chords]}) and arg quarter_duration {quarter_durations} does not match.')
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
