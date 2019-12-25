from musicscore.dtd.dtd import Choice, Element
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.types.complextypes.breathmark import ComplexTypeBreathMark
from musicscore.musicxml.types.complextypes.caesura import ComplexTypeCaesura
from musicscore.musicxml.types.complextypes.complextype import ComplexType, EmptyPlacement
from musicscore.musicxml.types.complextypes.emptyline import ComplexTypeEmptyLine
from musicscore.musicxml.types.complextypes.strongaccent import ComplexTypeStrongAccent


class Accent(EmptyPlacement):
    """he accent element indicates a regular horizontal accent mark."""
    _TAG = 'accent'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class StrongAccent(ComplexTypeStrongAccent):
    """The strong-accent element indicates a vertical accent mark."""
    _TAG = 'strong-accent'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Staccato(EmptyPlacement):
    """The staccato element is used for a dot articulation, as opposed to a stroke or a wedge."""
    _TAG = 'staccato'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Tenuto(EmptyPlacement):
    """The tenuto element indicates a tenuto line symbol."""
    _TAG = 'tenuto'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class DetachedLegato(EmptyPlacement):
    """The detached-legato element indicates the combination of a tenuto line and staccato dot symbol."""
    _TAG = 'detached-legato'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Staccatissimo(EmptyPlacement):
    """The staccatissimo element is used for a wedge articulation, as opposed to a dot or a stroke."""
    _TAG = 'staccatissimo'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Spiccato(EmptyPlacement):
    """The spiccato element is used for a stroke articulation, as opposed to a dot or a wedge."""
    _TAG = 'spiccato'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Scoop(ComplexTypeEmptyLine):
    """The scoop element is an indeterminate slide attached to a single note. The scoop element appears before the main
    note and comes from below the main pitch."""
    _TAG = 'scoop'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Plop(ComplexTypeEmptyLine):
    """The plop element is an indeterminate slide attached to a single note. The plop element appears before the main
    note and comes from above the main pitch."""
    _TAG = 'plop'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Doit(ComplexTypeEmptyLine):
    """The doit element is an indeterminate slide attached to a single note. The doit element appears after the main
    note and goes above the main pitch."""
    _TAG = 'plop'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Falloff(ComplexTypeEmptyLine):
    """The falloff element is an indeterminate slide attached to a single note. The falloff element appears after the
    main note and goes below the main pitch."""
    _TAG = 'falloff'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class BreathMark(ComplexTypeBreathMark):
    _TAG = 'breath-mark'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Caesura(ComplexTypeCaesura):
    """The falloff element is an indeterminate slide attached to a single note. The falloff element appears after the
    main note and goes below the main pitch."""
    _TAG = 'caesura'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Stress(EmptyPlacement):
    """The stress element indicates a stressed note."""
    _TAG = 'stress'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Unstress(EmptyPlacement):
    """The unstress element indicates an unstressed note. It is often notated using a u-shaped symbol."""
    _TAG = 'unstress'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SoftAccent(EmptyPlacement):
    """The soft-accent element indicates a soft accent that is not as heavy as a normal accent. It is often notated as
    &lt;&gt;. It can be combined with other articulations to implement the entire SMuFL Articulation Supplement
    range."""
    _TAG = 'soft-accent'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class OtherArticulation(object):
    """
    type="other-placement-text">
    The other-articulation element is used to define any articulations not yet in the MusicXML format. The smufl
    attribute can be used to specify a particular articulation, allowing application interoperability without requiring
    every SMuFL articulation to have a MusicXML element equivalent. Using the other-articulation element without the
    smufl attribute allows for extended representation, though without application interoperability.
    """
    _TAG = 'other-articulation'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        NotImplementedError()


class ComplexTypeArticulations(ComplexType, OptionalUniqueId):
    """Articulations and accents are grouped together here."""

    # _CHILDREN = [Accent, StrongAccent, Staccato, Tenuto, DetachedLegato, Staccatissimo, Spiccato, Scoop, Plop, Doit,
    #              Falloff, BreathMark, Caesura, Stress, Unstress, SoftAccent]

    _CHILDREN = [Accent, StrongAccent, Staccato, Tenuto, DetachedLegato, Staccatissimo, Spiccato, Scoop, Plop, Doit,
                 Falloff, BreathMark, Caesura, Stress, Unstress]

    _DTD = Choice(
        Element(Accent),
        Element(StrongAccent),
        Element(Staccato),
        Element(Tenuto),
        Element(DetachedLegato),
        Element(Staccatissimo),
        Element(Spiccato),
        Element(Scoop),
        Element(Plop),
        Element(Doit),
        Element(Falloff),
        Element(BreathMark),
        Element(Caesura),
        Element(Stress),
        Element(Unstress),
        # Element(SoftAccent),
        min_occurrence=0,
        max_occurrence=None
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
