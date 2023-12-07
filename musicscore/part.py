from typing import List, Optional, Union, Tuple

from musicscore import Chord
from musicscore.exceptions import IdHasAlreadyParentOfSameTypeError, IdWithSameValueExistsError, VoiceIsFullError, \
    AlreadyFinalizedError
from musicscore.finalize import FinalizeMixin
from musicscore.measure import Measure
from musicscore.musictree import MusicTree
from musicscore.quantize import QuantizeMixin
from musicscore.time import Time
from musicscore.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLPart, XMLScorePart

__all__ = ['Id', 'ScorePart', 'Part']


class Id:
    """
    This class uses the class attribute __refs__ of type list to keep track of all :obj:`~musicscore.part.Part` ids of one score to make sure they are unique.
    """
    __refs__ = []

    def __init__(self, value):
        self._parents = []
        self._value = None
        self.value = value
        self.__refs__.append(self)

    @classmethod
    def _check_value(cls, val):
        for obj in cls.__refs__:
            if obj.value == val:
                raise IdWithSameValueExistsError

    @property
    def value(self) -> str:
        """
        - val: a unique id. If not unique IdWithSameValueExistsError is raised.
        - All parents ids will be updated.
        """
        return self._value

    @value.setter
    def value(self, val):
        self._check_value(val)
        self._value = val
        for parent in self.get_parents():
            self.update_parents_id(parent)

    def delete(self) -> None:
        """
        Removes Id instance from class attribute __refs__ before deleting.
        """
        if self in self.__refs__:
            self.__refs__.remove(self)
        del self

    def update_parents_id(self, parent: XMLWrapper) -> None:
        """
        Sets parent's xml_object.id to self.value
        """
        parent.xml_object.id = self.value

    def add_parent(self, obj: XMLWrapper) -> None:
        """
        Adds object to Id as parent. Parents id gets updated.
        """
        if obj.__class__ in [type(parent) for parent in self.get_parents()]:
            raise IdHasAlreadyParentOfSameTypeError()
        self._parents.append(obj)
        self.update_parents_id(obj)

    def get_parents(self) -> List[XMLWrapper]:
        """
        Gets Id's parent objects
        """
        return self._parents

    def __repr__(self):
        return f"{self.__class__}:{self.value} at {id(self)}"

    def __del__(self):
        if self in self.__refs__:
            self.__refs__.remove(self)


class ScorePart(XMLWrapper):
    _ATTRIBUTES = {'part'}

    XMLClass = XMLScorePart

    def __init__(self, part, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._part = None
        self.part = part

    @property
    def part(self) -> 'Part':
        """
        Setting part property updates its :obj:`~musicxml.xmlelement.xmlelement.XMLPartName` and sets or updates its :obj:`~musicscore.part.Id`

        :return: :obj:`~Part`
        """
        return self._part

    @part.setter
    def part(self, val):
        if not isinstance(val, Part):
            raise TypeError
        self._part = val
        if self in self.part.id_.get_parents():
            self.part.id_.update_parents_id(self)
        else:
            self.part.id_.add_parent(self)
        self._update_name()

    def _update_abbreviation(self):
        self.xml_object.xml_part_abbreviation = self.part.abbreviation

    def _update_name(self):
        self.xml_object.xml_part_name = self.part.name


class Part(MusicTree, QuantizeMixin, FinalizeMixin, XMLWrapper):
    """
    Parent type: :obj:`~musicscore.score.Score`

    Child type: :obj:`~musicscore.measure.Measure`
    """

    _ATTRIBUTES = {'id_', 'name', 'abbreviation'}
    _ATTRIBUTES = _ATTRIBUTES.union(MusicTree._ATTRIBUTES)
    _ATTRIBUTES = _ATTRIBUTES.union(QuantizeMixin._ATTRIBUTES)
    XMLClass = XMLPart

    def __init__(self, id, name=None, abbreviation=None, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._id = None
        self.id_ = id
        self._score_part = ScorePart(part=self)
        self._name = None
        self.name = name
        self._abbreviation = None
        self.abbreviation = abbreviation
        self._current_measures = {}

    def _add_to_next_measure(self, current_measure, chord, staff_number, voice_number):
        if current_measure.next:
            current_measure = current_measure.next
        else:
            current_measure = self.add_measure()
        current_measure._add_chord(chord, staff_number=staff_number, voice_number=voice_number)
        return current_measure

    def _set_first_current_measure(self, staff_number, voice_number):
        for m in self.get_children():
            if m.get_voice(staff_number=staff_number, voice_number=voice_number):
                self.set_current_measure(staff_number, voice_number, m)
                return m

    @property
    def abbreviation(self) -> Optional[str]:
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, val):
        self._abbreviation = val
        try:
            self.score_part._update_abbreviation()
        except AttributeError:
            pass

    @property
    def id_(self) -> Id:
        """
        :rtype: :obj:`~musicscore.part.Id`, str
        :return: :obj:`~musicscore.part.Id`
        """
        return self._id

    @id_.setter
    def id_(self, val):
        if isinstance(val, Id):
            self._id = val
        elif isinstance(self._id, Id):
            self._id.value = val
        else:
            self._id = Id(val)
        if self in self.id_.get_parents():
            self.id_.update_parents_id(self)
        else:
            self.id_.add_parent(self)

    @property
    def name(self) -> str:
        """
        Set and get name. Setting tries toupdate name of :obj:`musicscore.part.score_part`

        :type: str
        :return: part's name. If no name is set part's :obj:`id_` is returned.
        """
        if self._name is not None:
            return self._name
        else:
            return ''

    @name.setter
    def name(self, val):
        self._name = val
        try:
            self.score_part._update_name()
        except AttributeError:
            pass

    @property
    def score_part(self) -> ScorePart:
        """
        :return: the  :obj:`~musicscore.part.ScorePart` which is associated with this part.
        """
        return self._score_part

    def add_child(self, child: Measure) -> Measure:
        """
        Check and add child to list of children. Child's parent is set to self.

        :param child: :obj:`~musicscore.measure.Measure`
        :return: child
        :rtype: :obj:`~musicscore.measure.Measure`

        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_child')
        super().add_child(child)
        self.xml_object.add_child(child.xml_object)
        return child

    def add_chord(self, chord: 'Chord', *, staff_number: Optional[int] = None, voice_number: Optional[int] = 1) -> None:
        """
        - Adds a chord to the specified voice in current measure (see :obj:`get_current_measure()`).
        - If no current measure is set the first measure is selected.
        - If part has still no measures one measure is added.
        - If the specified voice in current measure is full chord is added to the voice with the same number in the next measure. If no
          next measure exists one measure is added
        - If a leftover chord remains after adding chord, it is added to voice's :obj:`~musicscore.voice.Voice.leftover_chord` and is
          added to so many next measures as needed.

        :param chord: :obj:`~musicscore.chord.Chord` required
        :param staff_number: positive int, None. If None is set to 1.
        :param voice_number: positive_int
        :return: None
        """
        if not isinstance(chord, Chord):
            raise TypeError(f'{chord} must be of type Chord.')
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_chord')

        for gch in chord._grace_chords['before']:
            self.add_chord(gch, staff_number=staff_number, voice_number=voice_number)

        if staff_number is None:
            staff_number = 1
        current_measure = self.get_current_measure(staff_number=staff_number, voice_number=voice_number)

        if not current_measure:
            if self.get_children():
                current_measure = self.get_children()[0]
            else:
                current_measure = self.add_measure()
        try:
            current_measure._add_chord(chord, staff_number=staff_number, voice_number=voice_number)
        except VoiceIsFullError:
            current_measure = self._add_to_next_measure(current_measure, chord, staff_number, voice_number)

        for gch in chord._grace_chords['after']:
            self.add_chord(gch, staff_number=staff_number, voice_number=voice_number)

        leftover_chord = current_measure.get_voice(staff_number=staff_number, voice_number=voice_number).leftover_chord
        while leftover_chord:
            current_measure = self._add_to_next_measure(current_measure, leftover_chord, staff_number,
                                                        voice_number)
            leftover_chord = current_measure.get_voice(staff_number=staff_number,
                                                       voice_number=voice_number).leftover_chord

    def add_measure(self, time: Optional[Union[Time, List, Tuple]] = None, number: Optional[int] = None) -> Measure:
        """
        - Creates and adds a :obj:`~musicscore.measure.Measure` to part.
        - If time is not given last measure's :obj:`~musicscore.time.Time` is copied. Its :obj:`~musicscore.time.Time.show` property is set to
          ``False``
        - If number is not given last measure's number is incremented.
        - New measure's :obj:`~musicscore.key.Key` is a copy of last measure's :obj:`~musicscore.key.Key`. Its
          :obj:`~musicscore.key.Key.show` property is set to ``False``

        :param time: :obj:`~musicscore.time.Time`, (numerator, denominator), None
        :param number: positive int, None
        :return: created and added :obj:`~musicscore.measure.Measure`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_measure')
        previous_measure = self.get_children()[-1] if self.get_children() else None
        if not time:
            if previous_measure:
                time = previous_measure.time.__copy__()
                time.show = False
            else:
                time = Time(4, 4)
        else:
            if not isinstance(time, Time):
                time = Time(*time)

        if not number:
            if previous_measure:
                number = previous_measure.number + 1
            else:
                number = 1

        m = Measure(number=number, time=time)
        child = self.add_child(m)
        if previous_measure:
            m.key = previous_measure.key.__copy__()
            m.key.show = False

            for staff in previous_measure.get_children():
                st = m.add_staff(staff_number=staff.number)
                if st.clef:
                    st.clef = staff.clef.__copy__()
                    st.clef.show = False
                if st:
                    st.add_voice(voice_number=1)
        else:
            m.add_voice(staff_number=None, voice_number=1)

        return child

    def get_current_measure(self, staff_number: Optional[int] = 1, voice_number: int = 1):
        """
        Gets current measure for adding :obj:`~musicscore.chord.Chord` to a specific :obj:`~musicscore.voice.Voice`

        staff_number None is set to 1

        :param staff_number: positive int, None
        :param voice_number: positive int
        """
        if staff_number is None:
            staff_number = 1
        try:
            return self._current_measures[staff_number][voice_number]
        except KeyError:
            return self._set_first_current_measure(staff_number=staff_number, voice_number=voice_number)

    def set_current_measure(self, staff_number: int, voice_number: int, measure: Measure) -> None:
        """
        Sets current measure for adding :obj:`~musicscore.chord.Chord` to a specific :obj:`~musicscore.voice.Voice`

        :param staff_number: positive int
        :param voice_number: positive int
        :param measure: :obj:`musicscore.measure.Measure`
        :return: None
        """
        if staff_number is None:
            staff_number = 1
        if not isinstance(measure, Measure):
            raise TypeError(f"{measure} must be of type 'Measure'.")
        if self._current_measures.get(staff_number):
            self._current_measures[staff_number][voice_number] = measure
        else:
            self._current_measures[staff_number] = {voice_number: measure}

    def finalize(self) -> None:
        for beat in self.get_beats():
            if beat.get_quantized:
                beat.quantize_quarter_durations()
        super().finalize()
