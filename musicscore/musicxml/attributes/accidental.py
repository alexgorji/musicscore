from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Cautionary(AttributeAbstract):
    def __init__(self, cautionary=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('cautionary', cautionary, 'TypeYesNo')


class Editorial(AttributeAbstract):
    def __init__(self, editorial=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('editorial', editorial, 'TypeYesNo')


class Smulf(AttributeAbstract):
    def __init__(self, smulf=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('smulf', smulf, 'SmulfAccidentalGlyphName')
