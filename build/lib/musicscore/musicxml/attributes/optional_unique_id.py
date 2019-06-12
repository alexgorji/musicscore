from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class OptionalUniqueId(AttributeAbstract):
    """
    The optional-unique-id attribute group allows an element to optionally specify an ID that is unique to the entire
    document. This attribute group is not used for a required id attribute, or for an id attribute that specifies an
    id reference.
    """

    def __init__(self, id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('id', id, 'ID')
