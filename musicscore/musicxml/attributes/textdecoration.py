from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Underline(AttributeAbstract):
    """"""

    def __init__(self, underline=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('underline', underline, "TypeNumberOfLines")


class Overline(AttributeAbstract):
    """"""

    def __init__(self, overline=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('overline', overline, "TypeNumberOfLines")


class LineThrough(AttributeAbstract):
    """"""

    def __init__(self, line_through=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('line-through', line_through, "TypeNumberOfLines")


class TextDecoration(Underline, Overline, LineThrough):
    """
    The text-decoration attribute group is based on the similar feature in XHTML and CSS. It allows for text to be
    underlined, overlined, or struck-through. It extends the CSS version by allow double or triple lines instead of just
    being on or off.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
