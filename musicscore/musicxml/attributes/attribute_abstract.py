from musicscore.basic_functions import replace_dash
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.simple_type import Tenths, FontSizeType, FontWeightType, FontStyleType, YesNo, \
    CommaSeparatedText, RightLeftMiddle


class AttributeAbstract(XMLElement):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.type_tester = None

    def generate_attribute(self, attribute_name, attribute_value, type_string=None):
        property_name = replace_dash(attribute_name)

        exec('def getter(self): return self.get_attribute("{}")'.format(attribute_name))
        exec('''def setter(self, value): 
    if value is None:
        self.remove_attribute('{}')
    else:
        if {} is not None:
            {}(value)
        self.set_attribute('{}', value)'''.format(attribute_name, type_string, type_string, attribute_name))
        exec('AttributeAbstract.{} = property(getter, setter)'.format(property_name))
        if isinstance(attribute_value, str):
            exec('self.{} = "{}"'.format(property_name, attribute_value))
        else:
            exec('self.{} = {}'.format(property_name, attribute_value))

        return property_name
