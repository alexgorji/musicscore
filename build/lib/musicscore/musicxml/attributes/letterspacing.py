from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class LetterSpacing(AttributeAbstract):
    """
    The letter-spacing attribute specifies text tracking. Values are either "normal" or a number representing the number
    of ems to add between each letter. The number may be negative in order to subtract space. The default is normal,
    which allows flexibility of letter-spacing for purposes of text justification.
    """

    def __init__(self, letter_spacing=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('letter-spacing', letter_spacing, "TypeNumberOrNormal")