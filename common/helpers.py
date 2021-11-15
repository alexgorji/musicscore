def _check_type(value_name: str, value, type_, none=True):
    if none:
        if value is not None and not isinstance(value, type_):
            raise TypeError(f"{value_name} can be None or of type {type_} not {type(value)}")
    else:
        if not isinstance(value, type_):
            raise TypeError(f"{value_name} can only be of type {type_} not {type(value)}")


def _check_types(value_name: str, values, types, none=True):
    if none:
        if values is None:
            return
        elif isinstance(values, str):
            raise TypeError(f"{value_name} can be None or not string iterable.")
        elif not hasattr(values, '__iter__'):
            raise TypeError(f"{value_name} can be None or not string iterable.")
    else:
        if values is None:
            raise TypeError(f"{value_name} must be a not string iterable.")
        elif isinstance(values, str):
            raise TypeError(f"{value_name} must be a not string iterable.")
        elif not hasattr(values, '__iter__'):
            raise TypeError(f"{value_name} must be a not string iterable.")

    for value in values:
        if type(value) not in types:
            raise TypeError(f"Type of value in {value_name} can only be of types: {types}")


def _check_permitted_value(value_name: str, value, permitted_values):
    if value not in permitted_values:
        raise ValueError(f"{value_name} {value} not in permitted values list {permitted_values}")
