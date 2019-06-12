from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract

class BezierX(AttributeAbstract):
    def __init__(self, bezier_x=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('bezier-x', bezier_x, "TypeTenths")


class BezierY(AttributeAbstract):
    def __init__(self, bezier_y=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('bezier-y', bezier_y, "TypeTenths")


class BezierX2(AttributeAbstract):
    def __init__(self, bezier_x2=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('bezier-x2', bezier_x2, "TypeTenths")


class BezierY2(AttributeAbstract):
    def __init__(self, bezier_y2=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('bezier-y2', bezier_y2, "TypeTenths")


class BezierOffset(AttributeAbstract):
    def __init__(self, bezier_offset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('bezier-offset', bezier_offset, "TypeDivisions")


class BezierOffset2(AttributeAbstract):
    def __init__(self, bezier_offset2=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('bezier-offset2', bezier_offset2, "TypeDivisions")


class Bezier(BezierX, BezierY, BezierX2, BezierY2, BezierOffset, BezierOffset2):
    """
    The bezier attribute group is used to indicate the curvature of slurs and ties, representing the control points for
    a cubic bezier curve. For ties, the bezier attribute group is used with the tied element.

    Normal slurs, S-shaped slurs, and ties need only two bezier points: one associated with the start of the slur or
    tie, the other with the stop. Complex slurs and slurs divided over system breaks can specify additional bezier data
    at slur elements with a continue type.

    The bezier-x, bezier-y, and bezier-offset attributes describe the outgoing bezier point for slurs and ties with a
    start type, and the incoming bezier point for slurs and ties with types of stop or continue. The bezier-x2,
    bezier-y2, and bezier-offset2 attributes are only valid with slurs of type continue, and describe the outgoing
    bezier point.

    The bezier-x, bezier-y, bezier-x2, and bezier-y2 attributes are specified in tenths, relative to any position
    settings associated with the slur or tied element. The bezier-offset and bezier-offset2 attributes are measured in
    terms of musical divisions, like the offset element.

    The bezier-offset and bezier-offset2 attributes are deprecated as of MusicXML 3.1. If both the bezier-x and
    bezier-offset attributes are present, the bezier-x attribute takes priority. Similarly, the bezier-x2 attribute
    takes priority over the bezier-offset2 attribute. The two types of bezier attributes are not additive.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
