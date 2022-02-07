import math
from typing import Union, List

note_types = {(1, 12): '32nd',
              (1, 11): '32nd',
              (2, 11): '16th',
              (3, 11): '16th',
              (4, 11): 'eighth',
              (6, 11): 'eighth',
              (8, 11): 'quarter',
              (1, 10): '32nd',
              (3, 10): '16th',
              (1, 9): '32nd',
              (2, 9): '16th',
              (4, 9): 'eighth',
              (8, 9): 'quarter',
              (1, 8): '32nd',
              (3, 8): '16th',
              (7, 8): 'eighth',
              (1, 7): '16th',
              (2, 7): 'eighth',
              (3, 7): 'eighth',
              (4, 7): 'quarter',
              (6, 7): 'quarter',
              (1, 6): '16th',
              (1, 5): '16th',
              (2, 5): 'eighth',
              (3, 5): 'eighth',
              (4, 5): 'quarter',
              (1, 4): '16th',
              (2, 4): 'eighth',
              (3, 4): 'eighth',
              (7, 4): 'quarter',
              (1, 3): 'eighth',
              (2, 3): 'quarter',
              (3, 2): 'quarter',
              (1, 2): 'eighth',
              (1, 1): 'quarter',
              (2, 1): 'half',
              (3, 1): 'half',
              (4, 1): 'whole',
              (6, 1): 'whole',
              (8, 1): 'breve',
              (12, 1): 'breve'
              }


def isinstance_as_string(child_class: type, parent_class_names: Union[str, List[str]]) -> bool:
    """
    This function can be used to check if some class names (parent_class_names) can be found in another class's __mro__.
    If parent classes cannot be imported due to recursive imports this can be used instead of isinstance function.
    :param type child_class:
    :param str/[str] parent_class_names:
    :return: bool
    """
    if isinstance(parent_class_names, str):
        parent_class_names = [parent_class_names]

    for parent_class_name in parent_class_names:
        if parent_class_name not in [cls.__name__ for cls in child_class.__mro__]:
            return False
    return True


#
# def lcm(l):
#     """least common multiple of numbers in a list"""
#
#     def _lcm(a, b):
#         if a > b:
#             greater = a
#         else:
#             greater = b
#
#         while True:
#             if greater % a == 0 and greater % b == 0:
#                 lcm_ = greater
#                 break
#             greater += 1
#
#         return lcm_
#
#     x = l[0]
#     for y in l:
#         x = _lcm(x, y)
#     return x

def lcm(l):
    return math.lcm(*l)
    # return abs(a * b) // math.gcd(a, b)
