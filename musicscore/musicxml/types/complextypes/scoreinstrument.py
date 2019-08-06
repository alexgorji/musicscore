from musicscore.dtd.dtd import Sequence, Element, Choice
from musicscore.musicxml.attributes.id import Id
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType, Empty
from musicscore.musicxml.types.complextypes.virtualinstrument import ComplexTypeVirtualInstrument
from musicscore.musicxml.types.simple_type import String, TypePositiveIntegerOrEmpty


class InstrumentName(XMLElement, String):
    """
    The instrument-name element is typically used within a software application, rather than appearing on the printed
    page of a score.
    """
    _TAG = 'instrument-name'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class InstrumentAbbreviation(XMLElement, String):
    """
    The optional instrument-abbreviation element is typically used within a software application, rather than appearing
    on the printed page of a score.
    """
    _TAG = 'instrument-abbreviation'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class InstrumentSound(XMLElement, String):
    """
    The instrument-sound element describes the default timbre of the score-instrument.
    This description is independent of a particular virtual or MIDI instrument specification and allows playback to be
    shared more easily between applications and libraries.
    """
    _TAG = 'instrument-sound'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Solo(Empty):
    """
    The solo element was added in Version 2.0. It is present if performance is intended by a solo instrument.
    """
    _TAG = 'solo'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Ensemble(XMLElement, TypePositiveIntegerOrEmpty):
    """
    The ensemble element was added in Version 2.0. It is present if performance is intended by an ensemble such as an
    orchestral section. The text of the ensemble element contains the size of the section, or is empty if the ensemble
    size is not specified
    """
    _TAG = 'ensemble'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class VirtualInstrument(ComplexTypeVirtualInstrument):
    _TAG = 'virtual-instrument'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeScoreInstrument(ComplexType, Id):
    """
    The score-instrument type represents a single instrument within a score-part. As with the score-part type,
    each score-instrument has a required ID attribute, a name, and an optional  abbreviation.

    A score-instrument type is also required if the score specifies MIDI 1.0 channels, banks, or programs.
    An initial midi-instrument assignment can also be made here. MusicXML software should be able to automatically
    assign reasonable channels and instruments without these elements in simple cases, such as where part names match
    General MIDI instrument names.
    """
    _DTD = Sequence(
        Element(InstrumentName, min_occurrence=0),
        Element(InstrumentAbbreviation, min_occurrence=0),
        Element(InstrumentSound, min_occurrence=0),
        Choice(
            Element(Solo),
            Element(Ensemble),
            min_occurrence=0
        ),
        Element(VirtualInstrument, min_occurrence=0)
    )

    def __init__(self, tag, id, *args, **kwargs):
        super().__init__(tag=tag, id=id, *args, **kwargs)
