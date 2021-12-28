from xml.etree import ElementTree as ET


class XMLElement:
    """
    Use this class to create elements of complex types. A XSDComplexType must be set as type_ for each element when initiating.
    """

    def __init__(self, type_, value=None, attributes=None):
        """
        :param type_: XSDComplexType required
        :param value: None if empty, otherwise depends on type_.
        :param attributes: dict can only be set during initialization.
        """
        self._type = None
        self._value = None
        self._attributes = None
        self._xml_element = None
        self._set_type(type_)
        self.value = value
        self._set_attributes(attributes)

        self._create_xml_element()

    def _create_xml_element(self):
        self._xml_element = ET.Element(self.type_.XSD_TREE.name, self.attributes)
        if self.value:
            self._xml_element.text = str(self.value)

    def _set_attributes(self, val):
        if val is None:
            self._attributes = {}
        elif not isinstance(val, dict):
            raise TypeError
        else:
            self.type_.check_attributes(val)
            self._attributes = val

    def _set_type(self, val):
        if 'XSDComplexType' not in [cls.__name__ for cls in val.__mro__]:
            raise TypeError
        self._type = val

    @property
    def attributes(self):
        return self._attributes

    @property
    def type_(self):
        return self._type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is not None:
            self._value = self.type_(val)

    def to_string(self):
        return ET.tostring(self._xml_element, encoding='unicode')