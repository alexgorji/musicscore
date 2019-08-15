from musicscore.dtd.dtd import Sequence, Choice, Element
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.types.complextypes.complextype import ComplexType, Empty


class Natural(Empty):
    """
    The natural element indicates that this is a natural harmonic. These are usually notated at base pitch rather
    than sounding pitch.
    """
    _TAG = 'natural'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Artificial(Empty):
    """
    The artificial element indicates that this is an artificial harmonic.
    """
    _TAG = 'natural'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class BasePitch(Empty):
    """
    The base pitch is the pitch at which the string is played before touching to create the harmonic.
    """
    _TAG = 'base-pitch'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class TouchingPitch(Empty):
    """
    The touching-pitch is the pitch at which the string is touched lightly to produce the harmonic.
    """
    _TAG = 'touching-pitch'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SoundingPitch(Empty):
    """
    The sounding-pitch is the pitch which is heard when playing the harmonic.
    """
    _TAG = 'sounding-pitch'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeHarmonic(ComplexType, PrintObject, PrintStyle, Placement):
    """
    The harmonic type indicates natural and artificial harmonics. Allowing the type of pitch to be specified, combined
    with controls for appearance/playback differences, allows both the notation and the sound to be represented.
    Artificial harmonics can add a notated touching-pitch; artificial pinch harmonics will usually not notate a touching
    pitch. The attributes for the harmonic element refer to the use of the circular harmonic symbol, typically but not
    always used with natural harmonics.
    """
    _DTD = Sequence(
        Choice(
            Element(Natural),
            Element(Artificial),
            min_occurrence=0
        ),
        Choice(
            Element(BasePitch),
            Element(TouchingPitch),
            Element(SoundingPitch),
            min_occurrence=0
        )

    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
