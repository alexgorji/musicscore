from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class DefaultX(AttributeAbstract):
    def __init__(self, tag,  default_x=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.generate_attribute('default-x', default_x, 'Tenths')


class DefaultY(AttributeAbstract):
    def __init__(self, tag, default_y=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.generate_attribute('default-y', default_y, 'Tenths')


class RelativeX(AttributeAbstract):
    def __init__(self, tag, relative_x=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.generate_attribute('relative-x', relative_x, 'Tenths')


class RelativeY(AttributeAbstract):
    def __init__(self, tag, relative_y=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.generate_attribute('relative-y', relative_y, 'Tenths')


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

    def __init__(self, tag, default_x=None, default_y=None, relative_x=None, relative_y=None, *args, **kwargs):
        super().__init__(tag=tag, default_x=default_x, default_y=default_y, relative_x=relative_x, relative_y=relative_y,
                         *args, **kwargs)


class FontWeight(AttributeAbstract):
    """"""

    def __init__(self, tag, font_weight=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)

        self.generate_attribute('font-weight', font_weight, 'FontWeightType')

class FontSize(AttributeAbstract):
    """"""

    def __init__(self, tag, font_size=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.generate_attribute('font-size', font_size, 'FontSizeType')


class Font(FontWeight, FontSize):
    """	The font entity gathers together attributes for determining the font within a directive or direction.
    They are based on the text styles for Cascading Style Sheets. The font-family is a comma-separated list
    of font names. These can be specific font styles such as Maestro or Opus, or one of several generic font styles:
    music, engraved, handwritten, text, serif, sans-serif, handwritten, cursive, fantasy, and monospace. The music,
    engraved, and handwritten values refer to music fonts; the rest refer to text fonts. The fantasy style refers to
    decorative text such as found in older German-style printing. The font-style can be normal or italic. The
    font-size can be one of the CSS sizes (xx-small, x-small, small, medium, large, x-large, xx-large) or a numeric
    point size. The font-weight can be normal or bold. The default is application-dependent, but is a text font vs. """

    def __init__(self, tag, font_weight=None, font_size=None, *args, **kwargs):
        super().__init__(tag=tag, font_weight=font_weight, font_size=font_size, *args, **kwargs)
