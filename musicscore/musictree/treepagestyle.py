from musicscore.musicxml.elements.scoreheader import Defaults
from musicscore.musicxml.groups.layout import PageLayout, StaffLayout, SystemLayout
from musicscore.musicxml.groups.margins import LeftMargin, RightMargin, TopMargin, BottomMargin
from musicscore.musicxml.types.complextypes.defaults import Scaling
from musicscore.musicxml.types.complextypes.pagelayout import PageMargins, PageHeight, PageWidth
from musicscore.musicxml.types.complextypes.scaling import Millimeters, Tenths
from musicscore.musicxml.types.complextypes.stafflayout import StaffDistance
from musicscore.musicxml.types.complextypes.systemlayout import SystemDistance, SystemMargins, TopSystemDistance


class TreePageStyle(object):
    sizes = {'A4': (210, 297), 'A3': (297, 420)}

    def __init__(self, score, scale=1, size='A4', orientation='portrait', left_margin=111, right_margin=55,
                 top_margin=83,
                 bottom_margin=83, system_distance=None, system_left_margin=None, system_right_margin=None,
                 top_system_distance=None, staff_distance=None):

        self._score = None
        self.score = score
        self.tenth = 40

        self._size = None
        self._orientation = 'portrait'

        self._defaults = None
        self._scaling = None

        self._page_layout = None
        self._page_height = None
        self._page_width = None
        self._page_margins = None
        self.previous_page_width_value = None
        self.previous_page_height_value = None

        self._left_margin = None
        self._right_margin = None
        self._top_margin = None
        self._bottom_margin = None

        self._system_layout = None
        self._system_margins = None
        self._system_distance = None
        self._staff_layout = None
        self._staff_distance = None
        self._system_left_margin = None
        self._system_right_margin = None
        self._top_system_distance = None

        self.scale = scale
        self.size = size
        self.orientation = orientation

        self.left_margin = left_margin
        self.right_margin = right_margin
        self.top_margin = top_margin
        self.bottom_margin = bottom_margin
        self.staff_distance = staff_distance

        self.system_distance = system_distance
        self.system_left_margin = system_left_margin
        self.system_right_margin = system_right_margin
        self.top_system_distance = top_system_distance

    def millimeters_to_tenth(self, m):
        return round(m / self.millimeters * self.tenth)

    @property
    def millimeters(self):
        return self.scale * 7.2319

    def _add_defaults(self):
        self._defaults = self.score.add_child(Defaults())

    def _add_scaling(self):
        if not self._defaults:
            self._add_defaults()
        self._scaling = self._defaults.add_child(Scaling())
        self._scaling.add_child(Millimeters(self.millimeters))
        self._scaling.add_child(Tenths(self.tenth))

    def _add_page_layout(self):
        if not self._scaling:
            self._add_scaling()

        self._page_layout = self._defaults.add_child(PageLayout())

    def _add_staff_layout(self):
        if not self._scaling:
            self._add_scaling()

        self._staff_layout = self._defaults.add_child(StaffLayout())

    def _add_system_layout(self):
        if not self._scaling:
            self._add_scaling()

        self._system_layout = self._defaults.add_child(SystemLayout())
        self._system_distance = self._system_layout.add_child(SystemDistance(100))
        self._system_margins = self._system_layout.add_child(SystemMargins())
        self._system_left_margin = self._system_margins.add_child(LeftMargin(0))
        self._system_right_margin = self._system_margins.add_child(RightMargin(0))
        self._top_system_distance = self._system_layout.add_child(TopSystemDistance(150))

    def _add_page_margins(self):
        if not self._page_layout:
            self._add_page_layout()

        self._page_margins = self._page_layout.add_child(PageMargins(type_='both'))

    @property
    def score(self):
        '''
        system_layout = defaults.add_child(SystemLayout())
        system_margins = system_layout.add_child(SystemMargins())
        system_margins.add_child(LeftMargin(0))
        system_margins.add_child(RightMargin(0))
        system_layout.add_child(SystemDistance(121))
        system_layout.add_child(TopSystemDistance(300))
        '''
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def page_height(self):
        return self._page_height

    @page_height.setter
    def page_height(self, value):
        value = self.millimeters_to_tenth(value)
        if self.page_height:
            if self.page_height.value != value:
                self.previous_page_height_value = self.page_height.value
                self.page_height.value = value
                self.score.recalculate_y()
        else:
            if not self._page_layout:
                self._add_page_layout()
            self._page_height = self._page_layout.add_child(PageHeight(value))

    @property
    def page_width(self):
        return self._page_width

    @page_width.setter
    def page_width(self, value):
        value = self.millimeters_to_tenth(value)
        if self.page_width:
            if self.page_width.value != value:
                self.previous_page_width_value = self.page_width.value
                self.page_width.value = value
                self.score.recalculate_x()
        else:
            if not self._page_layout:
                self._add_page_layout()
            self._page_width = self._page_layout.add_child(PageWidth(value))

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if value == 'landscape':
            self.page_height, self.page_width = self.size[1], self.size[0]
        elif value == 'portrait':
            self.page_height, self.page_width = self.size[0], self.size[1]
        else:
            raise ValueError()

        self._orientation = value

    @property
    def left_margin(self):
        return self._left_margin

    @left_margin.setter
    def left_margin(self, value):
        # value = self.millimeters_to_tenth(value)
        if self.left_margin:
            self.left_margin.value = value
        else:
            if not self._page_margins:
                self._add_page_margins()
            self._left_margin = self._page_margins.add_child(LeftMargin(value))

    @property
    def right_margin(self):
        return self._right_margin

    @right_margin.setter
    def right_margin(self, value):
        # value = self.millimeters_to_tenth(value)
        if self.right_margin:
            self.right_margin.value = value
        else:
            if not self._page_margins:
                self._add_page_margins()
            self._right_margin = self._page_margins.add_child(RightMargin(value))

    @property
    def top_margin(self):
        return self._top_margin

    @top_margin.setter
    def top_margin(self, value):
        # value = self.millimeters_to_tenth(value)
        if self.top_margin:
            self.top_margin.value = value
        else:
            if not self._page_margins:
                self._add_page_margins()
            self._top_margin = self._page_margins.add_child(TopMargin(value))

    @property
    def bottom_margin(self):
        return self._bottom_margin

    @bottom_margin.setter
    def bottom_margin(self, value):
        # value = self.millimeters_to_tenth(value)
        if self.bottom_margin:
            self.bottom_margin.value = value
        else:
            if not self._page_margins:
                self._add_page_margins()
            self._bottom_margin = self._page_margins.add_child(BottomMargin(value))

    @property
    def staff_distance(self):
        return self._staff_distance

    @staff_distance.setter
    def staff_distance(self, value):
        if value:
            # value = self.millimeters_to_tenth(value)
            if self.staff_distance:
                self.staff_distance.value = value
            else:
                if not self._staff_layout:
                    self._add_staff_layout()
                self._staff_distance = self._staff_layout.add_child(StaffDistance(value))

    @property
    def system_distance(self):
        return self._system_distance

    @system_distance.setter
    def system_distance(self, value):
        if value:
            # value = self.millimeters_to_tenth(value)
            if not self._system_layout:
                self._add_system_layout()
            self.system_distance.value = value

    @property
    def system_left_margin(self):
        return self._system_left_margin

    @system_left_margin.setter
    def system_left_margin(self, value):
        if value:
            # value = self.millimeters_to_tenth(value)
            if not self._system_layout:
                self._add_system_layout()
            self.system_left_margin.value = value

    @property
    def system_right_margin(self):
        return self._system_right_margin

    @system_right_margin.setter
    def system_right_margin(self, value):
        if value:
            # value = self.millimeters_to_tenth(value)
            if not self._system_layout:
                self._add_system_layout()
            self.system_right_margin.value = value

    @property
    def top_system_distance(self):
        return self._top_system_distance

    @top_system_distance.setter
    def top_system_distance(self, value):
        if value:
            # value = self.millimeters_to_tenth(value)
            if not self._system_layout:
                self._add_system_layout()
            self.top_system_distance.value = value

    @property
    def size(self):
        (w, h) = self.sizes[self._size]
        # h = self.millimeters_to_tenth(h)
        # w = self.millimeters_to_tenth(w)
        return h, w

    @size.setter
    def size(self, value):
        self._size = value
        self.orientation = self._orientation
        # self.page_height = self.size[0]
        # self.page_width = self.size[1]

    @property
    def page_size(self):
        return self.size

    @page_size.setter
    def page_size(self, value):
        self.size = value
