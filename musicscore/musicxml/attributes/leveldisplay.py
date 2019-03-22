from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Parentheses(AttributeAbstract):

    def __init__(self, parentheses=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('parentheses', parentheses, "TypeYesNo")


class Bracket(AttributeAbstract):

    def __init__(self, bracket=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('bracket', bracket, "TypeYesNo")


class Size(AttributeAbstract):

    def __init__(self, size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('size', size, "TypeSymbolSize")


class LevelDisplay(Parentheses, Bracket, Size):
    """
    The level-display attribute group specifies three common ways to indicate editorial indications: putting parentheses
    or square brackets around a symbol, or making the symbol a different size. If not specified, they are left to
    application defaults. It is used by the level and accidental elements
    """

    def __init__(self, parentheses=None, bracket=None, size=None, *args, **kwargs):
        super().__init__(parentheses=parentheses, bracket=bracket, size=size, *args, **kwargs)
