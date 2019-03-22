from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class LineHeight(AttributeAbstract):
    """
    The line-height attribute specifies text leading. Values are either "normal" or a number representing the percentage
    of the current font height to use for leading. The default is "normal". The exact normal value is implementation-
    dependent, but values between 100 and 120 are recommended.
    """

    def __init__(self, line_height=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('line-height', line_height, "TypeNumberOrNormal")
