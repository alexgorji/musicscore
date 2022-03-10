from typing import Union, Optional

from musicxml.xmlelement.xmlelement import XMLPageLayout, XMLPageMargins, XMLLeftMargin, XMLRightMargin, XMLTopMargin, XMLBottomMargin, \
    XMLScaling, XMLDefaults, XMLSystemLayout, XMLSystemMargins, XMLStaffLayout

from musictree.util import isinstance_as_string
from musictree.xmlwrapper import XMLWrapper

__all__ = ['PAGE_MARGINS', 'PAGE_SIZES', 'SYSTEM_MARGINS', 'SYSTEM_LAYOUT', 'STAFF_LAYOUT', 'SCALING', 'Margins', 'Scaling',
           'PageLayout', 'SystemLayout', 'StaffLayout']
#:
PAGE_MARGINS = {
    'A4': {
        'portrait': {'left': 140, 'right': 70, 'top': 70, 'bottom': 70},
        'landscape': {'left': 111, 'right': 70, 'top': 70, 'bottom': 70}
    }, 'A3': {
        'portrait': {'left': 111, 'right': 70, 'top': 70, 'bottom': 70},
        'landscape': {'left': 111, 'right': 70, 'top': 70, 'bottom': 70}
    }
}

#:
PAGE_SIZES = {'A4': (209.991, 297.0389), 'A3': (297.0389, 419.9819)}

#:
SYSTEM_MARGINS = {'left': 0, 'right': 0}

#:
SYSTEM_LAYOUT = {'system_distance': 117, 'top_system_distance': 117}

#:
STAFF_LAYOUT = {'staff_distance': 80}

#:
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
        """
        :return: musictree object which uses this layout object.

        .. todo::
           Print implementation: At this moment only :obj:`~musictree.score.Score` is implemented.
        """
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
    def __init__(self, parent: Union['PageLayout', 'SystemLayout'], left: Union[float, int] = None, right: Union[float, int] = None,
                 top: Union[float, int] = None, bottom: Union[float, int] = None):
        self._parent = None
        self._left = None
        self._right = None
        self._top = None
        self._parent_xml_object = None
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
            setattr(self._parent_xml_object, f"xml_{side}_margin", eval(f"self.{side}"))

    @property
    def bottom(self):
        """
        Sets and gets :obj:`~musicxml.xmlelement.xmlelement.XMLBottomMargin` value of parent.
        """
        return self._bottom

    @bottom.setter
    def bottom(self, val):
        self._bottom = val
        self._update_parent('bottom')

    @property
    def left(self) -> Union[int, float]:
        """
        Sets and gets :obj:`~musicxml.xmlelement.xmlelement.XMLLeftMargin` value of parent.
        """
        return self._left

    @left.setter
    def left(self, val):
        self._left = val
        self._update_parent('left')

    @property
    def parent(self):
        """
        :return: parent layout object. :obj:`PageLayout` and :obj:`SystemLayout` are implemented.
        """
        return self._parent

    @parent.setter
    def parent(self, val):
        self._parent = val
        if isinstance(val, PageLayout):
            self._parent_xml_object = self._parent.xml_object.xml_page_margins
        elif isinstance(val, SystemLayout):
            self._parent_xml_object = self._parent.xml_object.xml_system_margins
        else:
            raise NotImplementedError

    @property
    def right(self) -> Union[int, float]:
        """
        Sets and gets :obj:`~musicxml.xmlelement.xmlelement.XMLRightMargin` value of parent.
        """
        return self._right

    @right.setter
    def right(self, val):
        self._right = val
        self._update_parent('right')

    @property
    def top(self) -> Union[int, float]:
        """
        Sets and gets :obj:`~musicxml.xmlelement.xmlelement.XMLTopMargin` value of parent.
        """
        return self._top

    @top.setter
    def top(self, val) -> Union[int, float]:
        self._top = val
        self._update_parent('top')


class Scaling(XMLWrapper):
    _ATTRIBUTES = {'millimeters', 'tenths', 'score'}
    XMLClass = XMLScaling

    def __init__(self, millimeters: Union[int, float] = SCALING['millimeters'], tenths: Union[int, float] = SCALING['tenths']):
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
    def millimeters(self) -> Union[int, float]:
        """
        Sets and gets millimeters value of scaling object. After setting value, parent :obj:`~musictree.score.Score`'s :obj:`PageLayout` is
        updated to reflect the changes.

        :return: millimeters
        :rtype: Union[int, float]
        """
        return self._millimeters

    @millimeters.setter
    def millimeters(self, val):
        if val != self._millimeters:
            self._millimeters = val
            self.xml_object.xml_millimeters = val
            self._update_score()

    @property
    def score(self):
        """
        Sets and gets parent :obj:`~musictree.score.Score`. After setting score, its :obj:`~musicxml.xmlelement.xmlelement.XMLScaling`
        and :obj:`~musicxml.xmlelement.xmlelement.XMLDefaults` are created if needed.

        :return: parent score
        :rtype: :obj:`~musictree.score.Score`
        """
        return self._score

    @score.setter
    def score(self, val):
        self._score = val
        if not self.score.xml_object.xml_defaults:
            self.score.xml_object.xml_defaults = XMLDefaults()
        self.score.xml_object.xml_defaults.xml_scaling = self.xml_object

    @property
    def tenths(self) -> Union[int, float]:
        """
        Sets and gets tenths value of scaling object. After setting value, parent :obj:`~musictree.score.Score`'s :obj:`PageLayout` is updated to reflect the
        changes.

        :return: tenths
        :rtype: Union[int, float]
        """
        return self._tenths

    @tenths.setter
    def tenths(self, val):
        if val != self._tenths:
            self._tenths = val
            self.xml_object.xml_tenths = val
            self._update_score()

    def millimeters_to_tenths(self, x: Union[int, float]) -> Union[int, float]:
        """
        Converts millimeter value into tenths

        :param x: millimeters
        :return: calculated tenths
        """
        return round((x * self.tenths) / self.millimeters)


class PageLayout(XMLWrapper, LayoutMixin):
    """
    :param size: :obj:`PAGE_SIZES`
    :param orientation: 'portrait', 'landscape'
    """
    _ATTRIBUTES = {'scaling', 'size', 'orientation', 'parent'}
    XMLClass = XMLPageLayout

    def __init__(self, size: str = 'A4', orientation: str = 'portrait'):

        super().__init__()
        self._xml_object = self.XMLClass()
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
    def margins(self) -> Margins:
        """
        Gets margins attribute.

        :return: margins object
        :rtype: :obj:`Margins`
        """
        return self._margins

    @property
    def orientation(self) -> str:
        """
        Sets and gets orientation. Permitted values are ['portrait', 'landscape']. After setting value, if parent and size already
        exist, page's height and width are set.

        :return: 'portrait', 'landscape'
        :rtype: str
        """
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
    def scaling(self) -> Scaling:
        """
        :return: :obj:`~musictree.score.Score`'s :obj:`Scaling`.
        :rtype: :obj:`Scaling`
        """
        return self.parent.get_root().scaling

    @property
    def size(self) -> str:
        """
        Sets and gets orientation. Permitted values are keys of obj:`PAGE_SIZES`. After setting value, if parent and orientation already
        exist, page's height and width are set.

        :return: sizes in :obj:`PAGE_SIZES`
        :rtype: str
        """
        return self._size

    @size.setter
    def size(self, val):
        if val not in PAGE_SIZES:
            raise NotImplementedError
        if val != self._size:
            self._size = val
            if self.orientation and self.parent:
                self._update()

    def _set_page_height_and_width(self):
        self.xml_object.xml_page_height = self._get_page_height()
        self.xml_object.xml_page_width = self._get_page_width()

    def _get_page_height(self):
        return self.scaling.millimeters_to_tenths(PAGE_SIZES[self.size][1]) if self.orientation == 'portrait' else \
            self.scaling.millimeters_to_tenths(PAGE_SIZES[self.size][0])

    def _get_page_width(self):
        return self.scaling.millimeters_to_tenths(PAGE_SIZES[self.size][0]) if self.orientation == 'portrait' else \
            self.scaling.millimeters_to_tenths(PAGE_SIZES[self.size][1])


class SystemLayout(XMLWrapper, LayoutMixin):
    _ATTRIBUTES = {'system_distance', 'top_system_distance', 'parent'}
    XMLClass = XMLSystemLayout

    def __init__(self, system_distance: Union[int, float] = SYSTEM_LAYOUT['system_distance'],
                 top_system_distance: Union[int, float] = SYSTEM_LAYOUT['top_system_distance']):
        super().__init__()

        self._xml_object = self.XMLClass()
        self._xml_object.xml_system_margins = XMLSystemMargins()

        self.system_distance = system_distance
        self.top_system_distance = top_system_distance

        self._margins = Margins(parent=self, **SYSTEM_MARGINS)

    @property
    def margins(self) -> Margins:
        """
        Gets margins attribute.

        :return: margins object
        :rtype: :obj:`Margins`
        """
        return self._margins

    @property
    def system_distance(self) -> Optional[Union[int, float]]:
        """
        Sets and gets ``value`` of :obj:`~musicxml.xmlelement.xmlelement.XMLSystemDistance`.

        :return: ``self.xml_object.xml_system_distance.value_``
        :rtype: int, float, None
        """
        if self.xml_object.xml_system_distance:
            return self.xml_object.xml_system_distance.value_

    @system_distance.setter
    def system_distance(self, val):
        self.xml_object.xml_system_distance = val

    @property
    def top_system_distance(self) -> Optional[Union[int, float]]:
        """
        Sets and gets ``value`` of :obj:`~musicxml.xmlelement.xmlelement.XMLTopSystemDistance`.

        :return: ``self.xml_object.xml_top_system_distance.value_``
        :rtype: int, float, None
        """
        if self.xml_object.xml_top_system_distance:
            return self.xml_object.xml_top_system_distance.value_

    @top_system_distance.setter
    def top_system_distance(self, val):
        self.xml_object.xml_top_system_distance = val


class StaffLayout(XMLWrapper, LayoutMixin):
    _ATTRIBUTES = {'staff_distance', 'parent'}
    XMLClass = XMLStaffLayout

    def __init__(self, staff_distance=STAFF_LAYOUT['staff_distance']):
        super().__init__()
        self._xml_object = self.XMLClass()
        self.staff_distance = staff_distance

    @property
    def staff_distance(self) -> Optional[Union[int, float]]:
        """
        Sets and gets ``value_`` of :obj:`~musicxml.xmlelement.xmlelement.XMLStaffDistance`.

        :return: ``self.xml_object.xml_staff_distance.value_``
        :rtype: int, float, None
        """
        if self.xml_object.xml_staff_distance:
            return self.xml_object.xml_staff_distance.value_

    @staff_distance.setter
    def staff_distance(self, val):
        self.xml_object.xml_staff_distance = val
