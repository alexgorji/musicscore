from musicscore.basic_functions import is_empty
from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.partname_text import PartNameText
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.identification import ComplexTypeIdentification
from musicscore.musicxml.types.simple_type import String


class ComplexTypePartName(ComplexType, PartNameText):
    """
    The part-name type describes the name or abbreviation of a score-part element. Formatting attributes for the
    part-name element are deprecated in Version 2.0 in favor of the new part-name-display and part-abbreviation-display
    elements.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class Id(AttributeAbstract):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('id', id, "ID")


class Identification(ComplexTypeIdentification):
    _TAG = 'identification'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class PartName(ComplexTypePartName):

    def __init__(self, name, *args, **kwargs):
        super().__init__(tag='part-name', *args, **kwargs)
        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self.name is None or is_empty(self.name):
            self.text = 'none'
        else:
            self.text = self.name


class PartNameDisplay(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='part-name-display', *args, **kwargs)
        raise NotImplementedError('PartNameDisplay')


class PartAbbreviation(ComplexTypePartName, String):
    """"""
    _TAG = 'part-abbreviation'

    def __init__(self, value='none', *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class PartAbbreviationDisplay(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='part-abbreviation-display', *args, **kwargs)
        raise NotImplementedError('PartAbbreviationDisplay')


class Group(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='group', *args, **kwargs)
        raise NotImplementedError('Group')


class ScoreInstrument(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='score-instrument', *args, **kwargs)
        raise NotImplementedError('ScoreInstrument')


class MidiDevice(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='midi-device', *args, **kwargs)
        raise NotImplementedError('MidiDevice')


class MidiInstrument(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='midi-instrument', *args, **kwargs)
        raise NotImplementedError('MidiInstrument')


class ComplexTypeScorePart(ComplexType, Id):
    """
    Each MusicXML part corresponds to a track in a Standard MIDI Format 1 file. The score-instrument elements are used
    when there are multiple instruments per track. The midi-device element is used to make a MIDI device or port
    assignment for the given track or specific MIDI instruments. Initial midi-instrument assignments may be made here
    as well.
    """

    _DTD = Sequence(
        Element(Identification, min_occurrence=0),
        Element(PartName),
        Element(PartNameDisplay, min_occurrence=0),
        Element(PartAbbreviation, min_occurrence=0),
        Element(PartAbbreviationDisplay, min_occurrence=0),
        Element(Group, min_occurrence=0, max_occurrence=None),
        Element(ScoreInstrument, min_occurrence=0, max_occurrence=None),
        Sequence(
            Element(MidiDevice, min_occurrence=0),
            Element(MidiInstrument, min_occurrence=0),
            min_occurrence=0,
            max_occurrence=None)
    )

    def __init__(self, tag, id, *args, **kwargs):
        super().__init__(tag=tag, id=id, *args, **kwargs)
