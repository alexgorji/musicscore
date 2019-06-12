from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.id import Id
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import String


class Port(AttributeAbstract):
    def __init__(self, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('port', port, "TypeMidi16")


class ComplexTypeMidiDevice(ComplexType, String, Port, Id):
    """The midi-device type corresponds to the DeviceName meta event in Standard MIDI Files. The optional port attribute
    is a number from 1 to 16 that can be used with the unofficial MIDI port (or cable) meta event. Unlike the DeviceName
    meta event, there can be multiple midi-device elements per MusicXML part starting in MusicXML 3.0. The optional id
    attribute refers to the score-instrument assigned to this device. If missing, the device assignment affects all
    score-instrument elements in the score-part."""

    def __init__(self, tag, value=None, *args, **kwargs):
        super().__init__(tag=tag, value=value, *args, **kwargs)
