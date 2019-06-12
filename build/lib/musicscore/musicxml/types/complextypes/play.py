from musicscore.dtd.dtd import Sequence, Choice, Element
from musicscore.musicxml.attributes.id import Id
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import String, TypeMute, TypeSemiPitched


class Ipa(XMLElement, String):
    """The ipa element represents International Phonetic Alphabet (IPA) sounds for vocal music. String content is
    limited to IPA 2005 symbols represented in Unicode 6.0."""
    _TAG = 'ipa'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Mute(XMLElement, TypeMute):
    _TAG = 'mute'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class SemiPitched(XMLElement, TypeSemiPitched):
    _TAG = 'semi-pitched'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class OtherPlay(XMLElement):
    _TAG = 'other=play'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)
        NotImplementedError()


class ComplexTypePlay(ComplexType, Id):
    """The play type, new in Version 3.0, specifies playback techniques to be used in conjunction with the
    instrument-sound element. When used as part of a sound element, it applies to all notes going forward in score
    order. In multi-instrument parts, the affected instrument should be specified using the id attribute. When used as
    part of a note element, it applies to the current note only."""

    _DTD = Sequence(
        Choice(
            Element(Ipa),
            Element(Mute),
            Element(SemiPitched),
            Element(OtherPlay),
            min_occurrence=0,
            max_occurrence=None
        )

    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
