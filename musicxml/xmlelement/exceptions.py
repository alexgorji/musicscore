class XMLChildContaiterException(Exception):
    pass


class XMLChildContainerWrongElementError(XMLChildContaiterException):
    pass


class XMLChildContainerMaxOccursError(XMLChildContaiterException):
    pass


class XMLChildContainerChoiceHasOtherElement(XMLChildContaiterException):
    pass
