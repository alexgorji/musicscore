from musicxml.xmlelement.xmlelement import XMLPart, XMLScorePart

from musictree.exceptions import IdHasAlreadyParentOfSameTypeError, IdWithSameValueExistsError, VoiceIsAlreadyFullError, \
    QuantizationBeatNotFullError
from musictree.measure import Measure
from musictree.core import MusicTree
from musictree.time import Time
from musictree.xmlwrapper import XMLWrapper


class Id:
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
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._check_value(val)
        self._value = val
        for parent in self.get_parents():
            self.update_parents_id(parent)

    def delete(self):
        if self in self.__refs__:
            self.__refs__.remove(self)
        del self

    def update_parents_id(self, parent):
        parent.xml_object.id = self.value

    def add_parent(self, obj):
        if obj.__class__ in [type(parent) for parent in self.get_parents()]:
            raise IdHasAlreadyParentOfSameTypeError()
        self._parents.append(obj)
        self.update_parents_id(obj)

    def get_parents(self):
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
    def part(self):
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

    def _update_name(self):
        self.xml_object.xml_part_name = self.part.name


class Part(MusicTree, XMLWrapper):
    _ATTRIBUTES = {'id_', 'name', '_score_part', '_current_measures'}
    XMLClass = XMLPart

    def __init__(self, id, name=None, *args, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._id = None
        self.id_ = id
        self._name = None
        self.name = name
        self._score_part = ScorePart(part=self)
        self._current_measures = {}

    def _set_first_current_measure(self, staff_number, voice_number):
        for m in self.get_children():
            if m.get_voice(staff_number=staff_number, voice_number=voice_number):
                self.set_current_measure(staff_number, voice_number, m)
                return m

    @property
    def current_measures(self):
        return self._current_measures

    @property
    def id_(self):
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
    def name(self):
        if self._name is not None:
            return self._name
        else:
            return self.id

    @name.setter
    def name(self, val):
        self._name = val
        try:
            self.score_part._update_name()
        except AttributeError:
            pass

    @property
    def score_part(self):
        return self._score_part

    def add_child(self, child):
        super().add_child(child)
        self.xml_object.add_child(child.xml_object)
        return child

    def add_chord(self, chord, *, staff_number=None, voice_number=1):
        def add_to_next_measure(current_measure, ch):
            if current_measure.next:
                current_measure = current_measure.next
            else:
                current_measure = self.add_measure()
            current_measure.add_chord(ch, staff_number=staff_number, voice_number=voice_number)
            return current_measure

        if staff_number is None:
            staff_number = 1
        current_measure = self.get_current_measure(staff_number=staff_number, voice_number=voice_number)

        if not current_measure:
            if self.get_children():
                current_measure = self.get_children()[0]
            else:
                current_measure = self.add_measure()
        try:
            current_measure.add_chord(chord, staff_number=staff_number, voice_number=voice_number)
        except VoiceIsAlreadyFullError:
            current_measure = add_to_next_measure(current_measure, chord)

        left_over_chord = current_measure.get_voice(staff_number=staff_number, voice_number=voice_number).left_over_chord
        while left_over_chord:
            current_measure = add_to_next_measure(current_measure, left_over_chord)
            left_over_chord = current_measure.get_voice(staff_number=staff_number, voice_number=voice_number).left_over_chord

    def add_measure(self, time=None, number=None):
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
                st.clef = staff.clef.__copy__()
                st.clef.show = False
                if st:
                    st.add_voice(voice_number=1)
        else:
            m.add_voice(staff_number=None, voice_number=1)

        return child

    def get_current_measure(self, staff_number=1, voice_number=1):
        if staff_number is None:
            staff_number = 1
        try:
            return self.current_measures[staff_number][voice_number]
        except KeyError:
            return self._set_first_current_measure(staff_number=staff_number, voice_number=voice_number)

    def set_current_measure(self, staff_number, voice_number, measure):
        if staff_number is None:
            staff_number = 1
        if not isinstance(measure, Measure):
            raise TypeError(f"{measure} must be of type 'Measure'.")
        if self._current_measures.get(staff_number):
            self._current_measures[staff_number][voice_number] = measure
        else:
            self._current_measures[staff_number] = {voice_number: measure}

    def quantize(self):
        for b in [beat for measure in self.get_children() for staff in measure.get_children() for voice in staff.get_children() for beat in \
                  voice.get_children()]:
            if b.is_filled:
                b.quantize()
            else:
                raise QuantizationBeatNotFullError(
                    f"Part:{self.id_.value} Beat {b.up.up.up.number}:{b.up.up.number}:{b.up.number}:{b.number} is not filled.")

    def split_not_writable_chords(self):
        for b in [beat for measure in self.get_children() for staff in measure.get_children() for voice in staff.get_children() for beat in \
                  voice.get_children()]:
            b.split_not_writable_chords()

    def update(self):
        for m in self.get_children():
            m.update()
