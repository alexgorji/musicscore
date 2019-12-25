from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import IDREF, TypeMidi16, String, TypePercent, TypeRotationDegrees, \
    TypeMidi16384, TypeMidi128


class MidiChannel(XMLElement, TypeMidi16):
    """The midi-channel element specifies a MIDI 1.0 channel numbers ranging from 1 to 16."""
    _TAG = 'midi-channel'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class MidiName(XMLElement, String):
    """The midi-name element corresponds to a ProgramName meta-event within a Standard MIDI File."""
    _TAG = 'midi-name'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class MidiBank(XMLElement, TypeMidi16384):
    """The midi-bank element specified a MIDI 1.0 bank number ranging from 1 to 16,384."""
    _TAG = 'midi-bank'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class MidiProgram(XMLElement, TypeMidi128):
    """The midi-program element specifies a MIDI 1.0 program number ranging from 1 to 128."""
    _TAG = 'midi-program'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class MidiUnpitched(XMLElement, TypeMidi128):
    """For unpitched instruments, the midi-unpitched element specifies a MIDI 1.0 note number ranging from 1 to 128.
    It is usually used with MIDI banks for percussion. Note that MIDI 1.0 note numbers are generally specified from 0
    to 127 rather than the 1 to 128 numbering used in this element."""
    _TAG = 'midi-unpitched'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Volume(XMLElement, TypePercent):
    """The volume element value is a percentage of the maximum ranging from 0 to 100, with decimal values allowed. This
    corresponds to a scaling value for the MIDI 1.0 channel volume controller."""
    _TAG = 'volume'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Pan(XMLElement, TypeRotationDegrees):
    """The pan and elevation elements allow placing of sound in a 3-D space relative to the listener. Both are expressed
    in degrees ranging from -180 to 180. For pan, 0 is straight ahead, -90 is hard left, 90 is hard right, and -180 and
    180 are directly behind the listener."""
    _TAG = 'rotation-degrees'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Elevation(XMLElement, TypeRotationDegrees):
    """:documentation>The elevation and pan elements allow placing of sound in a 3-D space relative to the listener.
     Both are expressed in degrees ranging from -180 to 180. For elevation, 0 is level with the listener, 90 is directly
     above, and -90 is directly below."""
    _TAG = 'elevation'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class ComplexTypeMidiInstrument(ComplexType):
    """The midi-instrument type defines MIDI 1.0 instrument playback. The midi-instrument element can be a part of
    either the score-instrument element at the start of a part, or the sound element within a part. The id attribute
    refers to the score-instrument affected by the change."""

    _ATTRIBUTES = []
    _DTD = Sequence(
        Element(MidiChannel, min_occurrence=0),
        Element(MidiName, min_occurrence=0),
        Element(MidiBank, min_occurrence=0),
        Element(MidiProgram, min_occurrence=0),
        Element(MidiUnpitched, min_occurrence=0),
        Element(Volume, min_occurrence=0),
        Element(Pan, min_occurrence=0),
        Element(Elevation, min_occurrence=0)
    )

    def __init__(self, tag, id_, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.id = id_

    @property
    def id(self):
        return self.get_attribute('id')

    @id.setter
    def id(self, value):
        if value is None:
            self.remove_attribute('id')
        else:
            IDREF(value)
            self._ATTRIBUTES.insert(0, 'id')
            self.set_attribute('id', value)
