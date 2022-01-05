class XMLChildContainerException(Exception):
    pass


class XMLChildContainerWrongElementError(XMLChildContainerException):
    pass


class XMLChildContainerMaxOccursError(XMLChildContainerException):
    pass


class XMLChildContainerChoiceHasOtherElement(XMLChildContainerException):
    pass


class XMLChildContainerElementRequired(XMLChildContainerException):
    pass


class XMLChildContainerFactoryException(Exception):
    pass


class XMLChildContainerFactoryError(XMLChildContainerFactoryException):
    pass
