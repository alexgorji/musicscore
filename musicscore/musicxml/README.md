Each Musicxml Element must be a subclass of musicscore.musicxml.element.xml_element.XMLElement

Attributes are always assigned via subclasses of musicscore.musicxml.attributes.attribute_abstract AttributeAbstract

**XMLElement._Attributes** is a list of all possible attributes in the desired order

If an Element is a subclass of AttributeAbstract it cannot inherit from XMLElement directly anymore
(XMLExample(XMLElement, AttributeExample) will give an error duo to inheritance conflicts)

Each Class must have super() with *args and **kwargs
<br>
<br>
<br>
Example: 
(in musicscore.musicxml.attributes.print_style.py)
```python
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
class Color(AttributeAbstract):
    """
    copy of musicxml documentation about color
    """

    def __init__(self, tag, color=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.generate_attribute('color', color, 'ColorType')
```
*musicscore.musicxml.types.simple_type.py*
```python
from musicscore.musicxml.types.simple_type import SimpleType
import re
class ColorType(SimpleType):
    pattern = r'^#[\dA-F]{6}([\dA-F][\dA-F])?$'
    p = re.compile(pattern)

    def __init__(self, value, *args, **kwargs):
        super().__init__(value, *args, **kwargs)

    @SimpleType.value.setter
    def value(self, v):
        m = self.p.match(v)
        if m is None:
            raise ValueError(
                '{}.value {} must match the following pattern: {}'.format(self.__class__.__name__,
                                                                          v, self.pattern))
```

Example:

*musicscore.musicxml.types.simple_type.py*
```python
from musicscore.musicxml.types.simple_type import SimpleType
class BarStyleType(SimpleType):
    permitted = ('regular', 'dotted', 'dashed', 'heavy', 'light-light', 'light-heavy', 'heavy-light', 'heavy-heavy',
                 'tick', 'short' 'none')

    def __init__(self, value, *args, **kwargs):
        super().__init__(value, *args, **kwargs)
```

```python
from musicscore.musicxml.attributes.barline import BarlineAttributes
from musicscore.musicxml.types.simple_type import BarStyleType
class Barline(BarlineAttributes):
    """
    copy of musicxml documentation about Barline
    """
    class BarStyle(BarStyleType):
        """
        copy of musicxml documentation about Bar-Style
        """
        def __init__(self, *args, **kwargs):
            super().__init__(tag='bar-style', *args, **kwargs)
    
    _CHILDREN_TYPES = [BarStyle]
    _CHILDREN_ORDERED = True
    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)

```
    