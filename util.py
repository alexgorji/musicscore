import math
from typing import Union, List


def lcm(l):
    return math.lcm(*l)


def dToX(input_list, first_element=0):
    if isinstance(input_list, list) is False:
        raise TypeError('xToD(input_list)')
    else:
        output = [first_element]
        for i in range(len(input_list)):
            output.append(input_list[i] + output[i])
        return output


def xToD(input_list):
    result = []
    for i in range(1, len(input_list)):
        result.append(input_list[i] - input_list[i - 1])
    return result


def isinstance_as_string(child: object, parent_class_names: Union[str, List[str]]) -> bool:
    """
    This function can be used to check if some class names (parent_class_names) can be found in another class's __mro__.
    If parent classes cannot be imported due to recursive imports this can be used instead of isinstance function.
    :param object child:
    :param str/[str] parent_class_names:
    :return: bool
    """
    if isinstance(parent_class_names, str):
        parent_class_names = [parent_class_names]

    for parent_class_name in parent_class_names:
        if parent_class_name not in [cls.__name__ for cls in child.__class__.__mro__]:
            return False
    return True
