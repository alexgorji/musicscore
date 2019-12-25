from musicscore.dtd.dtd import Choice, Element
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.types.complextypes.arrow import ComplexTypeArrow
from musicscore.musicxml.types.complextypes.bend import ComplexTypeBend
from musicscore.musicxml.types.complextypes.complextype import ComplexType, EmptyPlacement, EmptyPlacementSmulf, \
    PlacementText, OtherPlacementText
from musicscore.musicxml.types.complextypes.fingering import ComplexTypeFingering
from musicscore.musicxml.types.complextypes.fret import ComplexTypeFret
from musicscore.musicxml.types.complextypes.hammeronpulloff import ComplexTypeHammerOnPullOff
from musicscore.musicxml.types.complextypes.handbell import ComplexTypeHandbell
from musicscore.musicxml.types.complextypes.harmonic import ComplexTypeHarmonic
from musicscore.musicxml.types.complextypes.harmonmute import ComplexTypeHarmonMute
from musicscore.musicxml.types.complextypes.heeltoe import ComplexTypeHeelToe
from musicscore.musicxml.types.complextypes.hole import ComplexTypeHole
from musicscore.musicxml.types.complextypes.string_ import ComplexTypeString_
from musicscore.musicxml.types.complextypes.tap import ComplexTypeTap


class UpBow(EmptyPlacement):
    """
    The up-bow element represents the symbol that is used both for up-bowing on bowed instruments, and up-stroke on
    plucked instruments.
    """
    _TAG = 'up-bow'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class DownBow(EmptyPlacement):
    """
    The down-bow element represents the symbol that is used both for down-bowing on bowed instruments, and down-stroke
    on plucked instruments.
    """
    _TAG = 'down-bow'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Harmonic(ComplexTypeHarmonic):
    _TAG = 'harmonic'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class OpenString(EmptyPlacement):
    """
    The open-string element represents the zero-shaped open string symbol.
    """
    _TAG = 'open-string'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ThumbPosition(EmptyPlacement):
    """
    The thumb-position element represents the thumb position symbol. This is a circle with a line, where the line does
    not come within the circle. It is distinct from the snap pizzicato symbol, where the line comes inside the circle.
"""
    _TAG = 'thumb-position'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Fingering(ComplexTypeFingering):
    _TAG = 'fingering'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Pluck(PlacementText):
    """
    The pluck element is used to specify the plucking fingering on a fretted instrument, where the fingering element
    refers to the fretting fingering. Typical values are p, i, m, a for pulgar/thumb, indicio/index, medio/middle,
    and anular/ring fingers.
    """
    _TAG = 'placement-text'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class DoubleTongue(EmptyPlacement):
    """he double-tongue element represents the double tongue symbol (two dots arranged horizontally)."""

    _TAG = 'double-tongue'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class TripleTongue(EmptyPlacement):
    """The triple-tongue element represents the triple tongue symbol (three dots arranged horizontally)."""

    _TAG = 'triple-tongue'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Stopped(EmptyPlacementSmulf):
    """
    The stopped element represents the stopped symbol, which looks like a plus sign. The smufl attribute distinguishes
    different SMuFL glyphs that have a similar appearance such as handbellsMalletBellSuspended and guitarClosePedal.
    If not present, the default glyph is brassMuteClosed.
    """

    _TAG = 'stopped'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SnapPizzicato(EmptyPlacement):
    """The snap-pizzicato element represents the snap pizzicato symbol. This is a circle with a line, where the line
    comes inside the circle. It is distinct from the thumb-position symbol, where the line does not come inside the
    circle."""

    _TAG = 'snap-pizzicato'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Fret(ComplexTypeFret):
    """"""

    _TAG = 'fret'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class String_(ComplexTypeString_):
    """"""

    _TAG = 'string'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class HammerOn(ComplexTypeHammerOnPullOff):
    """"""

    _TAG = 'hammer-on'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class PullOff(ComplexTypeHammerOnPullOff):
    """"""

    _TAG = 'pull-off'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Bend(ComplexTypeBend):
    """"""

    _TAG = 'bend'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Tap(ComplexTypeTap):
    """"""

    _TAG = 'tap'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Heel(ComplexTypeHeelToe):
    """"""

    _TAG = 'heel'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Toe(ComplexTypeHeelToe):
    """"""

    _TAG = 'toe'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Fingernails(EmptyPlacement):
    """The fingernails element is used in notation for harp and other plucked string instruments."""

    _TAG = 'fingernails'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Hole(ComplexTypeHole):
    """"""

    _TAG = 'hole'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Arrow(ComplexTypeArrow):
    """"""

    _TAG = 'arrow'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Handbell(ComplexTypeHandbell):
    """"""

    _TAG = 'handbell'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class BrassBend(EmptyPlacement):
    """The brass-bend element represents the u-shaped bend symbol used in brass notation,  distinct from the bend
    element used in guitar music."""

    _TAG = 'brass-bend'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Flip(EmptyPlacement):
    """The flip element represents the flip symbol used in brass notation."""

    _TAG = 'flip'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Smear(EmptyPlacement):
    """The smear element represents the tilde-shaped smear symbol used in brass notation."""

    _TAG = 'smear'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Open(EmptyPlacementSmulf):
    """The open element represents the open symbol, which looks like a circle. The smufl attribute can be used to
    distinguish different SMuFL glyphs that have a similar appearance such as brassMuteOpen and guitarOpenPedal. If not
    present, the default glyph is brassMuteOp
    """
    _TAG = 'open'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class HalfMuted(EmptyPlacementSmulf):
    """The half-muted element represents the half-muted symbol, which looks like a circle with a plus sign inside.
    The smufl attribute can be used to distinguish different SMuFL glyphs that have a similar appearance such as
    brassMuteHalfClosed and guitarHalfOpenPedal. If not present, the default glyph is brassMuteHalfClosed."""

    _TAG = 'half-muted'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class HarmonMute(ComplexTypeHarmonMute):
    """"""

    _TAG = 'harmon-mute'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Golpe(EmptyPlacement):
    """The golpe element represents the golpe symbol that is used for tapping the pick guard in guitar music."""

    _TAG = 'golpe'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class OtherTechnical(OtherPlacementText):
    """The other-technical element is used to define any technical indications not yet in the MusicXML format. The smufl
    attribute can be used to specify a particular glyph, allowing application interoperability without requiring every
    SMuFL technical indication to have a MusicXML element equivalent. Using the other-technical element without the smufl
    attribute allows for extended representation, though without application interoperability."""

    _TAG = 'other-technical'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeTechnical(ComplexType, OptionalUniqueId):
    """
    Technical indications give performance information for individual instruments.
    """
    _DTD = Choice(
        Element(UpBow),
        Element(DownBow),
        Element(Harmonic),
        Element(OpenString),
        Element(ThumbPosition),
        Element(Fingering),
        Element(Pluck),
        Element(DoubleTongue),
        Element(TripleTongue),
        Element(Stopped),
        Element(SnapPizzicato),
        Element(Fret),
        Element(String_),
        Element(HammerOn),
        Element(PullOff),
        Element(Bend),
        Element(Tap),
        Element(Heel),
        Element(Toe),
        Element(Fingernails),
        Element(Hole),
        Element(Arrow),
        Element(Handbell),
        Element(BrassBend),
        Element(Flip),
        Element(Smear),
        Element(Open),
        Element(HalfMuted),
        Element(HarmonMute),
        Element(Golpe),
        Element(OtherTechnical),

        min_occurrence=0,
        max_occurrence=None)

    def __init__(self, tag, *args, **kwargs):
        super().__init__(*args, tag=tag, **kwargs)
