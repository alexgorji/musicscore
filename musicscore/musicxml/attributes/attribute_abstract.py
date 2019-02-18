from musicscore.basic_functions import replace_dash
from musicscore.musicxml.elements.xml_element import XMLElement


class AttributeAbstract(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_tester = None

    def generate_attribute(self, attribute_name, attribute_value):
        property_name = replace_dash(attribute_name)
        exec('def getter(self): return self.get_attribute("{}")'.format(attribute_name))
        exec('''def setter(self, value): 
    if value is None:
        self.remove_attribute('{}')
    else:
        if self.type_tester is not None:
            self.type_tester(value)
        self.set_attribute('{}', value)'''.format(attribute_name, attribute_name))
        exec('AttributeAbstract.{} = property(getter, setter)'.format(property_name))
        if isinstance(attribute_value, str):
            exec('self.{} = "{}"'.format(property_name, attribute_value))
        else:
            exec('self.{} = {}'.format(property_name, attribute_value))

        return property_name
