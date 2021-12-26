class XMLTree:
    """
    Abstract class as root of all generated XML Classes
    """
    XSD_TREE = None

    @classmethod
    def get_xsd(cls):
        return cls.XSD_TREE.get_xsd()
