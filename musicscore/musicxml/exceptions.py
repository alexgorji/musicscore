class XMLError(Exception):
    pass


class AfterInitializationError(XMLError):
    def __init__(self, tag):
        msg = 'tag {} cannot be changed after initializing XMLElement'.format(tag)
        super().__init__(msg)


class XMLTypeError(XMLError):
    def __init__(self, allowed_types):
        msg = 'only {} are allowed'.format(allowed_types)
        super().__init__(msg)


class XMLValueError(XMLError):
    def __init__(self, allowed_values):
        msg = 'only {} are allowed'.format(allowed_values)
        super().__init__(msg)


class ChildAlreadyExists(XMLError):
    def __init__(self, new_child):
        msg = 'not multiple type of child {} already exists'.format(type(new_child))
        super().__init__(msg)
