from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class DefaultX(AttributeAbstract):
    def __init__(self, default_x=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('default-x', default_x, 'TypeTenths')


class DefaultY(AttributeAbstract):
    def __init__(self, default_y=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('default-y', default_y, 'TypeTenths')


class RelativeX(AttributeAbstract):
    def __init__(self, relative_x=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('relative-x', relative_x, 'TypeTenths')


class RelativeY(AttributeAbstract):
    def __init__(self, relative_y=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('relative-y', relative_y, 'TypeTenths')


class Position(DefaultX, DefaultY, RelativeX, RelativeY):
    """
    The position attributes are based on MuseData print suggestions.
    For most elements, any program will compute a default x and y position.
    The position attributes let this be changed two ways.

    The default-x and default-y attributes change the computation of the default position.
    For most elements, the origin is changed relative to the left-hand side of the note or the musical position within
    the bar (x) and the top line of the staff (y).

    For the following elements, the default-x value changes the origin relative to the start of the current measure:
    	- note
    	- figured-bass
    	- harmony
    	- link
    	- directive
    	- measure-numbering
    	- all descendants of the part-list element
    	- all children of the direction-type element

    This origin is from the start of the entire measure, at either the left barline or the start of the system.

    When the default-x attribute is used within a child element of the part-name-display, part-abbreviation-display,
    group-name-display, or group-abbreviation-display elements, it changes the origin relative to the start of the first
    measure on the system. These values are used when the current measure or a succeeding measure starts a new system.
    The same change of origin is used for the group-symbol element.

    For the note, figured-bass, and harmony elements, the default-x value is considered to have adjusted the musical
    position within the bar for its descendant elements.

    Since the credit-words and credit-image elements are not related to a measure, in these cases the default-x and
    default-y attributes adjust the origin relative to the bottom left-hand corner of the specified page.

    The relative-x and relative-y attributes change the position relative to the default position, either as computed
    by the individual program, or as overridden by the default-x and default-y attributes.

    Positive x is right, negative x is left; positive y is up, negative y is down. All units are in tenths of interline
    space. For stems, positive relative-y lengthens a stem while negative relative-y shortens it.

    The default-x and default-y position attributes provide higher-resolution positioning data than related features
    such as the placement attribute and the offset element. Applications reading a MusicXML file that can understand
    both features should generally rely on the default-x and default-y attributes for their greater accuracy. For the
    relative-x and relative-y attributes, the offset element, placement attribute, and directive attribute provide
    context for the relative position information, so the two features should be interpreted together.

    As elsewhere in the MusicXML format, tenths are the global tenths defined by the scaling element, not the local
    tenths of a staff resized by the staff-size element.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class YPosition(DefaultX, DefaultY, RelativeX, RelativeY):
    """The y-position attribute group is used for elements like stems where specifying y position is common, but
    specifying x position is rare.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class XPosition(DefaultX, DefaultY, RelativeX, RelativeY):
    """The x-position attribute group is used for elements like notes where specifying x position is common, but
    specifying y position is rare.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
