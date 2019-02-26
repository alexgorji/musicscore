Define XMLElement as a subclass of XMLElement with an appropriate tag:
```python
from musicscore.musicxml.elements.xml_element import XMLElement

class XMLExample(XMLElement):
    """
    copy of musicxml documentaion
    """
    def __init__(self, *args, **kwargs):
        super().__init__(tag='example', *args, **kwargs)
```
<br>
<br>

**ADDING ATTRIBUTES**

Add a type for attribute in folder types to simple_type.py (as a subclass of SimpleType) or complex_type.py (as a subclass of ComplexType) if needed
```python
from musicscore.musicxml.types.simple_type import SimpleType
class ExampleType(SimpleType):
    permitted = ('one', 'two', 'three')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
```

Define one or more attribute(s) in folder attributes.

```python
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
class AttibuteExample(AttributeAbstract):
    """
    some documentation if needed
    """

    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('attribute-example', attribute_example, "ExampleType")
```
<br>

Make your XMLElement a subclass of defined Attribute and attribute tag[s] to _ATTRIBUTES in the desired order. Be carefull of overwriting inherited _ATTIRBUTES!
```python
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.attributes.attribute_example import AttibuteExample


class XMLExample(XMLElement, AttibuteExample):
    """
    copy of musicxml documentaion
    """
    _ATTRIBUTES = ['attribute-example']
    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(tag='example', attribute_example=attribute_example, *args, **kwargs)
```
<br>
By now you have to have written also some tests in tests folder.

```python
from musicscore.musicxml.xml_example import XMLExample
from unittest import TestCase


class TestExample(TestCase):
    def setUp(self):
        self.example = XMLExample()

    def test_example(self):
        with self.assertRaises(ValueError):
            self.example.attribute_example = 2
        self.example.attribute_example = 'one'
        self.example.value = 2
        result = '''<example attribute-example="one">2</example>
'''
        self.assertEqual(self.example.to_string(), result)
```