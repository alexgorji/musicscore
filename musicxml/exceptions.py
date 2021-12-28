class XSDException(Exception):
    pass


class XSDAttributeRequiredException(XSDException):
    pass


class XSDWrongAttribute(XSDAttributeRequiredException):
    pass
