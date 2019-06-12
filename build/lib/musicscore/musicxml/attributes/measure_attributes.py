from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId


class Number(AttributeAbstract):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('number', str(number), "Token")


class Text(AttributeAbstract):
    def __init__(self, text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('text', text, "TypeMeasureText")


class Implicit(AttributeAbstract):
    def __init__(self, implicit=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('implicit', implicit, "TypeYesNo")


class NonControlling(AttributeAbstract):
    def __init__(self, non_controlling=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('non-controlling', non_controlling, "TypeYesNo")


class Width(AttributeAbstract):
    """"""

    def __init__(self, width=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('width', width, "TypeTenths")


class MeasureAttributes(Number, Text, Implicit, NonControlling, Width, OptionalUniqueId):
    """
    The measure-attributes group is used by the measure element. Measures have a required number attribute (going from
    partwise to timewise, measures are grouped via the number).

    The implicit attribute is set to "yes" for measures where the measure number should never appear, such as pickup
    measures and the last half of mid-measure repeats. The value is "no" if not specified.

    The non-controlling attribute is intended for use in multimetric music like the Don Giovanni minuet. If set to
    "yes", the left barline in this measure does not coincide with the left barline of measures in other parts. The
    value is "no" if not specified.

    In partwise files, the number attribute should be the same for measures in different parts that share the same left
    barline. While the number attribute is often numeric, it does not have to be. Non-numeric values are typically used
    together with the implicit or non-controlling attributes being set to "yes". For a pickup measure, the number
    attribute is typically set to "0" and the implicit attribute is typically set to "yes".

    If measure numbers are not unique within a part, this can cause problems for conversions between partwise and
    timewise formats. The text attribute allows specification of displayed measure numbers that are different than what
    is used in the number attribute. This attribute is ignored for measures where the implicit attribute is set to
    "yes". Further details about measure numbering can be specified using the measure-numbering element.

    Measure width is specified in tenths. These are the global tenths specified in the scaling element, not local
    tenths as modified by the staff-size element.	The width covers the entire measure from barline or system start
    to barline or system end.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
