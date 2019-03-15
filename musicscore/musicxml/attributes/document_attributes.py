from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Version(AttributeAbstract):
    def __init__(self, version='1.0', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('version', version, 'Token')


class DocumentAttributes(Version):
    """
    The document-attributes attribute group is used to specify the attributes for an entire MusicXML document. Currently
    this is used for the version attribute.

    The version attribute was added in Version 1.1 for the score-partwise and score-timewise documents. It provides an
    easier way to get version information than through the MusicXML public ID. The default value is 1.0 to make it
    possible for programs that handle later versions to distinguish earlier version files reliably. Programs that write
    MusicXML 1.1 or later files should set this attribute.
    """
    def __init__(self, version='1.0', *args, **kwargs):
        super().__init__(version=version, *args, **kwargs)

# class FontSize(AttributeAbstract):
#     """"""
#
#     def __init__(self, font_size=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.generate_attribute('font-size', font_size, 'FontSizeType')
