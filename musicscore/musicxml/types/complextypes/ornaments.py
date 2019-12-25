from musicscore.dtd.dtd import Sequence, Element, Choice
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.types.complextypes.accidentalmark import ComplexTypeAccidentalMark
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.emptytrillsound import ComplexTypeEmptyTrillSound
from musicscore.musicxml.types.complextypes.horizontalturn import ComplexTypeHorizontalTurn
from musicscore.musicxml.types.complextypes.tremolo import ComplexTypeTremolo
from musicscore.musicxml.types.complextypes.wavyline import ComplexTypeWavyLine


class TrillMark(ComplexTypeEmptyTrillSound):
    """
    The trill-mark element represents the trill-mark symbol.
    """
    _TAG = "trill-mark"

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Turn(ComplexTypeHorizontalTurn):
    """
    The turn element is the normal turn shape which goes up then down.
    """
    _TAG = "turn"

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class DelayedTurn(ComplexTypeHorizontalTurn):
    """
    The delayed-turn element indicates a normal turn that is delayed until the end of the current note.
    """
    _TAG = "delayed-turn"

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class InvertedTurn(ComplexTypeHorizontalTurn):
    """
    The inverted-turn element has the shape which goes down and then up.
    """
    _TAG = "inverted-turn"

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class DelayedInvertedTurn(ComplexTypeHorizontalTurn):
    """
    The delayed-inverted-turn element indicates an inverted turn that is delayed until the end of the current note.
    """
    _TAG = "delayed-inverted-turn"

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class VerticalTurn(ComplexTypeEmptyTrillSound):
    """
    The vertical-turn element has the turn symbol shape arranged vertically going from upper left to lower right.
    """
    _TAG = "vertical-turn"

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class InvertedVerticalTurn(ComplexTypeEmptyTrillSound):
    """
    The inverted-vertical-turn element has the turn symbol shape arranged vertically going from upper right to lower
    left.
    """
    _TAG = "inverted-vertical-turn"

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Shake(ComplexTypeEmptyTrillSound):
    """
    The shake element has a similar appearance to an inverted-mordent element.
    """
    _TAG = "shake"

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class WavyLine(ComplexTypeWavyLine):
    _TAG = 'wavy-line'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Mordent(object):
    """
                    <xs:element name="mordent" type="mordent">
                    <xs:annotation>
                        <xs:documentation>The mordent element represents the sign with the vertical line. The choice of
                            which mordent sign is inverted differs between MusicXML and SMuFL. The long attribute is
                            "no" by default.
                        </xs:documentation>
                    </xs:annotation>
                </xs:element>
    """
    _TAG = "mordent"

    def __init__(self, *args, **kwargs):
        super().__init__(self, tag=self._TAG, *args, **kwargs)
        raise NotImplementedError()


class InvertedMordent(object):
    """
                    <xs:element name="inverted-mordent" type="mordent">
                    <xs:annotation>
                        <xs:documentation>The inverted-mordent element represents the sign without the vertical line.
                            The choice of which mordent is inverted differs between MusicXML and SMuFL. The long
                            attribute is "no" by default.
                        </xs:documentation>
                    </xs:annotation>
                </xs:element>
    """
    _TAG = "inverted-mordent"

    def __init__(self, *args, **kwargs):
        super().__init__(self, tag=self._TAG, *args, **kwargs)
        raise NotImplementedError()


class Schleifer(object):
    """
                    <xs:element name="schleifer" type="empty-placement">
                    <xs:annotation>
                        <xs:documentation>The name for this ornament is based on the German, to avoid confusion with the
                            more common slide element defined earlier.
                        </xs:documentation>
                    </xs:annotation>
                </xs:element>
    """
    _TAG = "schleifer"

    def __init__(self, *args, **kwargs):
        super().__init__(self, tag=self._TAG, *args, **kwargs)
        raise NotImplementedError()


class Tremolo(ComplexTypeTremolo):
    _TAG = 'tremolo'

    def __init__(self, value=3, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Haydn(ComplexTypeEmptyTrillSound):
    """
    The haydn element represents the Haydn ornament. This is defined in SMuFL as ornamentHaydn.
    """
    _TAG = "haydn"

    def __init__(self, *args, **kwargs):
        super().__init__(self, tag=self._TAG, *args, **kwargs)


class OtherOrnament(object):
    """
                    <xs:element name="other-ornament" type="other-placement-text">
                    <xs:annotation>
                        <xs:documentation>The other-ornament element is used to define any ornaments not yet in the
                            MusicXML format. The smufl attribute can be used to specify a particular ornament, allowing
                            application interoperability without requiring every SMuFL ornament to have a MusicXML
                            element equivalent. Using the other-ornament element without the smufl attribute allows for
                            extended representation, though without application interoperability.
                        </xs:documentation>
                    </xs:annotation>
                </xs:element>
    """
    _TAG = "other-ornament"

    def __init__(self, *args, **kwargs):
        super().__init__(self, tag=self._TAG, *args, **kwargs)
        raise NotImplementedError()


class AccidentalMark(ComplexTypeAccidentalMark):
    _TAG = "accidental-mark"

    def __init__(self, *args, **kwargs):
        super().__init__(self, tag=self._TAG, *args, **kwargs)
        raise NotImplementedError()


class ComplexTypeOrnaments(ComplexType, OptionalUniqueId):
    """
    Ornaments can be any of several types, followed optionally by accidentals. The accidental-mark element's content is
    represented the same as an accidental element, but with a different name to reflect the different musical meaning.
    """

    _DTD = Sequence(
        Choice(
            Element(TrillMark),
            Element(Turn),
            Element(DelayedTurn),
            Element(InvertedTurn),
            Element(DelayedInvertedTurn),
            Element(VerticalTurn),
            Element(InvertedVerticalTurn),
            Element(Shake),
            Element(WavyLine),
            Element(Mordent),
            Element(InvertedMordent),
            Element(Schleifer),
            Element(Tremolo),
            Element(Haydn),
            Element(OtherOrnament)
            , min_occurrence=0, max_occurrence=None
        ),
        Element(AccidentalMark,
                min_occurrence=0, max_occurrence=None
                )

    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
