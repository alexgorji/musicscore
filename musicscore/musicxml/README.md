Define XMLElement as a subclass of XMLElement with an appropriate tag:
```python
from musicscore.musicxml.elements.xml_element import XMLElement

class XMLExample(XMLElement):
    """
    copy of musicxml documentation
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
class AttributeExample(AttributeAbstract):
    """
    some documentation if needed
    """

    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('attribute-example', attribute_example, "ExampleType")
```
<br>

Make your XMLElement a subclass of defined Attribute and attribute tag[s] to _ATTRIBUTES in the desired order. Be careful of overwriting inherited _ATTRIBUTES!
```python
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.attributes.attribute_example import AttributeExample


class XMLExample(XMLElement, AttributeExample):
    """
    copy of musicxml documentation
    """
    _ATTRIBUTES = ['attribute-example']
    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(tag='example', attribute_example=attribute_example, *args, **kwargs)
```
<br>
By now you have to have written also some tests in tests folder.

```python
from musicscore.musicxml.elements.xml_example import XMLExample
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
<br>

**ADDING ATTRIBUTES**

Define XMLChildren classes as above.<br>
Add Children Types to _CHILDREN_TYPES .<br>
If the order of children is important set _CHILDREN_ORDER to True.<br>
If in ordered child a child can occur multiple times use attribute self.multiple in child's __init__

```python
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.attributes.attribute_example import AttributeExample


class XMLExampleChild1(XMLElement):
    """
    some documentation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='example-child-1', *args, **kwargs)


class XMLExampleChild2(XMLElement):
    """
    some documentation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='example-child-2', *args, **kwargs)
        self.multiple = True


class XMLExample(XMLElement, AttributeExample):
    """
    some documentation
    """
    _ATTRIBUTES = ['attribute-example']
    _CHILDREN_TYPES = [XMLExampleChild1, XMLExampleChild2]
    _CHILDREN_ORDERED = True

    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(tag='example', attribute_example=attribute_example, *args, **kwargs)
```

<br>
Write some tests ...

```python
from musicscore.musicxml.elements.xml_example import XMLExample, XMLExampleChild1, XMLExampleChild2
from musicscore.musicxml.exceptions import ChildAlreadyExists
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
        self.example.value = None
        self.example.add_child(XMLExampleChild2())
        self.example.add_child(XMLExampleChild1())
        self.example.add_child(XMLExampleChild2())
        result = '''<example attribute-example="one">
  <example-child-1/>
  <example-child-2/>
  <example-child-2/>
</example>
'''
        self.assertEqual(self.example.to_string(), result)
        with self.assertRaises(ChildAlreadyExists):
            self.example.add_child(XMLExampleChild1())

```