from musicxml.xmlelement.xmlelement import XMLPageLayout, XMLPageMargins, XMLLeftMargin, XMLRightMargin, XMLTopMargin, XMLBottomMargin, \
    XMLScaling, XMLDefaults, XMLSystemLayout, XMLSystemMargins, XMLStaffLayout

from musictree.util import isinstance_as_string
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

SYSTEM_MARGINS = {'left': 0, 'right': 0}

SYSTEM_LAYOUT = {'system_distance': 117, 'top_system_distance': 66}

STAFF_LAYOUT = {'staff_distance': 80}

SCALING = {
    'millimeters': 7.2319,
    'tenths': 40
}


class LayoutMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        self._parent = val
        if isinstance(self, PageLayout):
            if isinstance_as_string(self.parent, 'Score'):
                self._update()
                self.parent.xml_object.xml_defaults.xml_page_layout = self.xml_object
            else:
                raise NotImplementedError
        elif isinstance_as_string(self, 'SystemLayout'):
            if isinstance_as_string(self.parent, 'Score'):
                self.parent.xml_object.xml_defaults.xml_system_layout = self.xml_object
            else:
                raise NotImplementedError
        elif isinstance_as_string(self, 'StaffLayout'):
            if isinstance_as_string(self.parent, 'Score'):
                self.parent.xml_object.xml_defaults.xml_staff_layout = self.xml_object
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError


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
        if side not in ['left', 'right', 'top', 'bottom']:
            raise ValueError
        if side in ['top', 'bottom'] and isinstance(self.parent, SystemLayout):
            if eval(f"self.{side}") is not None:
                raise ValueError
        else:
            setattr(self._parent_object, f"xml_{side}_margin", eval(f"self.{side}"))

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
        elif isinstance(val, SystemLayout):
            self._parent_object = self._parent.xml_object.xml_system_margins
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


class Scaling(XMLWrapper):
    _ATTRIBUTES = {'millimeters', 'tenths', 'score'}
    XMLClass = XMLScaling

    def __init__(self, millimeters=SCALING['millimeters'], tenths=SCALING['tenths']):
        super().__init__()
        self._xml_object = self.XMLClass()
        self._millimeters = None
        self._tenths = None
        self._score = None

        self.millimeters = millimeters
        self.tenths = tenths

    def _update_score(self):
        if self.score:
            self.score.page_layout._set_page_height_and_width()

    @property
    def millimeters(self):
        return self._millimeters

    @millimeters.setter
    def millimeters(self, val):
        if val != self._millimeters:
            self._millimeters = val
            self.xml_object.xml_millimeters = val
            self._update_score()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        self._score = val
        if not self.score.xml_object.xml_defaults:
            self.score.xml_object.xml_defaults = XMLDefaults()
        self.score.xml_object.xml_defaults.xml_scaling = self.xml_object

    @property
    def tenths(self):
        return self._tenths

    @tenths.setter
    def tenths(self, val):
        if val != self._tenths:
            self._tenths = val
            self.xml_object.xml_tenths = val
            self._update_score()

    def millimeters_to_tenths(self, x):
        return round((x * self.tenths) / self.millimeters)


class PageLayout(XMLWrapper, LayoutMixin):
    _ATTRIBUTES = {'scaling', 'size', 'orientation', 'parent'}
    SIZES = {'A4': (209.991, 297.0389), 'A3': (297.0389, 419.9819)}

    def __init__(self, size='A4', orientation='portrait'):
        super().__init__()
        self._xml_object = XMLPageLayout()
        self._xml_object.xml_page_margins = XMLPageMargins(type='both')

        self._size = None
        self._orientation = None

        self.size = size
        self.orientation = orientation

        self._margins = Margins(parent=self, **PAGE_MARGINS[self.size][self.orientation])

    def _update(self):
        self._set_page_height_and_width()
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
            if self.size and self.parent:
                self._update()

    @property
    def scaling(self):
        return self.parent.get_root().scaling

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        if val not in self.SIZES:
            raise NotImplementedError
        if val != self._size:
            self._size = val
            if self.orientation and self.parent:
                self._update()

    def _set_page_height_and_width(self):
        self.xml_object.xml_page_height = self._get_page_height()
        self.xml_object.xml_page_width = self._get_page_width()

    def _get_page_height(self):
        return self.scaling.millimeters_to_tenths(self.SIZES[self.size][1]) if self.orientation == 'portrait' else \
            self.scaling.millimeters_to_tenths(self.SIZES[self.size][0])

    def _get_page_width(self):
        return self.scaling.millimeters_to_tenths(self.SIZES[self.size][0]) if self.orientation == 'portrait' else \
            self.scaling.millimeters_to_tenths(self.SIZES[self.size][1])


class SystemLayout(XMLWrapper, LayoutMixin):
    _ATTRIBUTES = {'system_distance', 'top_system_distance', 'parent'}

    def __init__(self, system_distance=SYSTEM_LAYOUT['system_distance'], top_system_distance=SYSTEM_LAYOUT['top_system_distance']):
        super().__init__()

        self._xml_object = XMLSystemLayout()
        self._xml_object.xml_system_margins = XMLSystemMargins()
        self._system_distance = None
        self._top_system_distance = None

        self.system_distance = system_distance
        self.top_system_distance = top_system_distance

        self._margins = Margins(parent=self, **SYSTEM_MARGINS)

    @property
    def margins(self):
        return self._margins

    @property
    def system_distance(self):
        return self._system_distance

    @system_distance.setter
    def system_distance(self, val):
        self._system_distance = val
        self.xml_object.xml_system_distance = self.system_distance

    @property
    def top_system_distance(self):
        return self._top_system_distance

    @top_system_distance.setter
    def top_system_distance(self, val):
        self._top_system_distance = val
        self.xml_object.xml_top_system_distance = self.top_system_distance


class StaffLayout(XMLWrapper, LayoutMixin):
    _ATTRIBUTES = {'staff_distance', 'parent'}

    def __init__(self, staff_distance=STAFF_LAYOUT['staff_distance']):
        super().__init__()
        self._xml_object = XMLStaffLayout()
        self._staff_distance = None
        self.staff_distance = staff_distance

    @property
    def staff_distance(self):
        return self._staff_distance

    @staff_distance.setter
    def staff_distance(self, val):
        self._staff_distance = val
        self.xml_object.xml_staff_distance = self.staff_distance
