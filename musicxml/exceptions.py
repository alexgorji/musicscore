class XSDException(Exception):
    pass


class XSDAttributeRequiredException(XSDException):
    pass


class XSDWrongAttribute(XSDAttributeRequiredException):
    pass


class XMLElementException(Exception):
    pass


class XMLElementWrongChildType(XMLElementException):
    pass


class XMLElementChildrenRequired(XMLElementException):
    pass