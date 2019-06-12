from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class DashLength(AttributeAbstract):
    def __init__(self, dash_length=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('dash-length', dash_length, "TypeTenths")


class SpaceLength(AttributeAbstract):
    def __init__(self, space_length=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('space-length', space_length, "TypeTenths")


class DashedFormatting(DashLength, SpaceLength):
    """
    The dashed-formatting entity represents the length of dashes and spaces in a dashed line. Both the dash-length and
    space-length attributes are represented in tenths. These attributes are ignored if the corresponding line-type attribute is not dashed.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

