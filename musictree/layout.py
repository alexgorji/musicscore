from musicxml.xmlelement.xmlelement import XMLPageLayout, XMLPageMargins, XMLLeftMargin, XMLRightMargin, XMLTopMargin, XMLBottomMargin

from musictree.xmlwrapper import XMLWrapper

PAGE_MARGINS = {
    'A4': {
        'portrait': {'left': 140, 'right': 70, 'top': 70, 'bottom': 70},
        'landscape': {'left': 111, 'right': 70, 'top': 70, 'bottom': 70}
    }, 'A3': {
        'portrait': {'left': 111, 'right': 70, 'top': 70, 'bottom': 70},
        'landscape': {'left': 111, 'right': 70, 'top': 70, 'bottom': 70}
    }
}

SYSTEM_MARGINS = {'left': 0, 'right': 0, 'top': None, 'bottom': None}

SYSTEM_LAYOUT = {'system_distance': 117, 'top_system_distance': 66}

STAFF_LAYOUT = {'staff_distance': 80}


class Margins:
    def __init__(self, parent, left=None, right=None, top=None, bottom=None):
        self._parent = None
        self._left = None
        self._right = None
        self._top = None
        self._parent_object = None
        self._parent = None

        self.parent = parent
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def _update_parent(self, side):
        if eval(f"self._parent_object.xml_{side}_margin"):
            setattr(self._parent_object, f"xml_{side}_margin", eval(f"self.{side}"))
        else:
            if eval(f"self.{side}") is not None:
                setattr(self._parent_object, f"xml_{side}_margin", eval(f"XML{side.capitalize()}Margin(self.{side})"))

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, val):
        self._bottom = val
        self._update_parent('bottom')

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, val):
        self._left = val
        self._update_parent('left')

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        self._parent = val
        if isinstance(val, PageLayout):
            self._parent_object = self._parent.xml_object.xml_page_margins
        else:
            raise NotImplementedError

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, val):
        self._right = val
        self._update_parent('right')

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, val):
        self._top = val
        self._update_parent('top')


class Scaling:
    def __init__(self, millimeters=7.2319, tenths=40):
        self.millimeters = millimeters
        self.tenths = tenths

    def millimeters_to_tenths(self, x):
        return round((x * self.tenths) / self.millimeters)


class SystemLayout:
    def __init__(self, system_distance=SYSTEM_LAYOUT['system_distance'], top_system_distance=SYSTEM_LAYOUT['top_system_distance']):
        self._margins = Margins(**SYSTEM_MARGINS)
        self._system_distance = None
        self._top_system_distance = None
        self.system_distance = system_distance
        self.top_system_distance = top_system_distance

    @property
    def margins(self):
        return self._margins

    @property
    def system_distance(self):
        return self._system_distance

    @system_distance.setter
    def system_distance(self, val):
        self._system_distance = val

    @property
    def top_system_distance(self):
        return self._top_system_distance

    @top_system_distance.setter
    def top_system_distance(self, val):
        self._top_system_distance = val


class StaffLayout:
    def __init__(self, staff_distance=STAFF_LAYOUT['staff_distance']):
        self._staff_distance = None
        self.staff_distance = staff_distance

    @property
    def staff_distance(self):
        return self._staff_distance

    @staff_distance.setter
    def staff_distance(self, val):
        self._staff_distance = val


class PageLayout(XMLWrapper):
    _ATTRIBUTES = {'scaling', 'size', 'orientation'}
    SIZES = {'A4': (209.991, 297.0389), 'A3': (297.0389, 419.9819)}

    def __init__(self, scaling=Scaling(), size='A4', orientation='portrait'):
        super().__init__()
        self._xml_object = XMLPageLayout()
        self._xml_object.xml_page_margins = XMLPageMargins(type='both')

        self._scaling = None
        self._size = None
        self._orientation = None

        self.scaling = scaling
        self.size = size
        self.orientation = orientation

        self._margins = Margins(parent=self, **PAGE_MARGINS[self.size][self.orientation])

    @property
    def margins(self):
        return self._margins

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, val):
        _permitted = ['portrait', 'landscape']
        if val not in _permitted:
            raise ValueError(f"{val} can only be: {_permitted}")
        if val != self._orientation:
            self._orientation = val
            if self.size:
                self._set_page_height_and_width()
                self._margins = Margins(parent=self, **PAGE_MARGINS[self.size][self.orientation])

    @property
    def scaling(self):
        return self._scaling

    @scaling.setter
    def scaling(self, val):
        if not isinstance(val, Scaling):
            raise TypeError
        self._scaling = val
        if self.size and self.orientation:
            self._set_page_height_and_width()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        if val not in self.SIZES:
            raise NotImplementedError
        if val != self._size:
            self._size = val
            if self.orientation:
                self._set_page_height_and_width()
                self._margins = Margins(parent=self, **PAGE_MARGINS[self.size][self.orientation])

    def _set_page_height_and_width(self):
        self.xml_object.xml_page_height = self._get_page_height()
        self.xml_object.xml_page_width = self._get_page_width()

    def _get_page_height(self):
        return self.scaling.millimeters_to_tenths(self.SIZES[self.size][1]) if self.orientation == 'portrait' else \
            self.scaling.millimeters_to_tenths(self.SIZES[self.size][0])

    def _get_page_width(self):
        return self.scaling.millimeters_to_tenths(self.SIZES[self.size][0]) if self.orientation == 'portrait' else \
            self.scaling.millimeters_to_tenths(self.SIZES[self.size][1])
