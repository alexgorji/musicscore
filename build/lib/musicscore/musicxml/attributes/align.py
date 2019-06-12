from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Halign(AttributeAbstract):
    """
    In cases where text extends over more than one line, horizontal alignment and justify values can be different. The
    most typical case is for credits, such as:

	Words and music by
	  Pat Songwriter

	Typically this type of credit is aligned to the right, so that the position information refers to the right-most
	part of the text. But in this example, the text is center-justified, not right-justified.

	The halign attribute is used in these situations. If it is not present, its value is the same as for the justify
	attribute.
    """

    def __init__(self, halign=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('halign', halign, 'TypeLeftCenterRight')


class Valign(AttributeAbstract):
    """
    The valign attribute is used to indicate vertical alignment to the top, middle, bottom, or baseline of the text.
    Defaults are implementation-dependent.
    """

    def __init__(self, valign=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('valign', valign, 'TypeValign')


class ValignImage(AttributeAbstract):
    """
    The valign-image attribute is used to indicate vertical alignment for images and graphics, so it removes the
    baseline value. Defaults are implementation-dependent.
    """

    def __init__(self, valign_image=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('valign-image', valign_image, 'TypeValignImage')
