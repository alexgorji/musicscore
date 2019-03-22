from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class FontFamily(AttributeAbstract):
    """"""

    def __init__(self, font_family=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('font-family', font_family, 'TypeCommaSeparatedText')


class FontStyle(AttributeAbstract):
    """"""

    def __init__(self, font_style=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('font-style', font_style, 'TypeFontStyle')


class FontSize(AttributeAbstract):
    """"""

    def __init__(self, font_size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('font-size', font_size, 'TypeFontSize')


class FontWeight(AttributeAbstract):
    """"""

    def __init__(self, font_weight=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.generate_attribute('font-weight', font_weight, 'TypeFontWeight')


class Font(FontFamily, FontStyle, FontSize, FontWeight):
    """	The font entity gathers together attributes for determining the font within a directive or direction.
    They are based on the text styles for Cascading Style Sheets. The font-family is a comma-separated list
    of font names. These can be specific font styles such as Maestro or Opus, or one of several generic font styles:
    music, engraved, handwritten, text, serif, sans-serif, handwritten, cursive, fantasy, and monospace. The music,
    engraved, and handwritten values refer to music fonts; the rest refer to text fonts. The fantasy style refers to
    decorative text such as found in older German-style printing. The font-style can be normal or italic. The
    font-size can be one of the CSS sizes (xx-small, x-small, small, medium, large, x-large, xx-large) or a numeric
    point size. The font-weight can be normal or bold. The default is application-dependent, but is a text font vs. """

    def __init__(self, font_weight=None, font_size=None, font_style=None, font_family=None, *args, **kwargs):
        super().__init__(font_weight=font_weight, font_size=font_size, font_style=font_style,
                         font_family=font_family, *args, **kwargs)
