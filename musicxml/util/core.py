def cap_first(s):
    return s[0].upper() + s[1:]


def get_cleaned_token(string_value):
    output = ' '.join(partial.strip() for partial in string_value.split('\n'))
    output = ' '.join(partial.strip() for partial in output.split('\t'))
    output = ' '.join(partial.strip() for partial in output.split('\r'))
    output = ' '.join([partial.strip() for partial in output.split(' ') if partial != ''])
    return output


def convert_to_xsd_class_name(name, type_='simple_type'):
    try:
        name = name.split(':')[1]
    except IndexError:
        pass
    name = cap_first(name)
    name = ''.join([cap_first(partial) for partial in name.split('-')])
    if type_ == 'simple_type':
        name = 'XSDSimpleType' + name
    elif type_ == 'complex_type':
        name = 'XSDComplexType' + name
    elif type_ == 'group':
        name = 'XSDGroup' + name
    else:
        raise ValueError
    return name


def convert_to_xml_class_name(name: str) -> str:
    return 'XML' + ''.join([cap_first(partial) for partial in name.split('-')])


def replace_key_underline_with_hyphen(dict_):
    output = {}
    for k, v in dict_.items():
        new_key = '-'.join(k.split('_'))
        if output.get(new_key) is not None:
            raise KeyError(f"Key {new_key} already exists in dictionary.")
        output[new_key] = v
    return output
