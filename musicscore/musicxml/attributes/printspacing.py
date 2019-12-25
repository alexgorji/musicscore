from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class PrintSpacing(AttributeAbstract):
    """The print-spacing attribute controls whether or not spacing is left for an invisible note or object. It is
    used only if no note, dot, or lyric is being printed. The value is yes (leave spacing) by default."""

    def __init__(self, print_spacing=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('print-spacing', print_spacing, 'TypeYesNo')
