from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Location(AttributeAbstract):
    """
    Barlines have a location attribute to make it easier to process barlines independently of the other musical
    data in a score. It is often easier to set up measures separately from entering notes. The location
    attribute must match where the barline element occurs within the rest of the musical data in the score. If
    location is left, it should be the first element in the measure, aside from the print, bookmark, and link
    elements. If location is right, it should be the last element, again with the possible exception of the
    print, bookmark, and link elements.
    """

    def __init__(self, location=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('location', location, "RightLeftMiddle")


class BarlineAttributes(Location):

    def __init__(self, location=None, *args, **kwargs):
        super().__init__(location=location, *args, **kwargs)
