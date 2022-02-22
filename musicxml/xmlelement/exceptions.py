class XMLElementException(Exception):
    pass


class XMLElementCannotHaveChildrenError(XMLElementException):
    pass


class XMLChildContainerException(Exception):
    pass


class XMLChildContainerWrongElementError(XMLChildContainerException):
    pass


class XMLChildContainerMaxOccursError(XMLChildContainerException):
    pass


class XMLChildContainerChoiceHasAnotherChosenChild(XMLChildContainerException):
    pass


class XMLChildContainerFactoryException(Exception):
    pass


class XMLChildContainerFactoryError(XMLChildContainerFactoryException):
    pass
