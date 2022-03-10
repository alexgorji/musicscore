from typing import List

from musictree.finalupdate_mixin import FinalUpdateMixin
from musicxml.xmlelement.xmlelement import XMLScorePartwise, XMLPartList, XMLCredit, XMLCreditWords, XMLIdentification, XMLEncoding, \
    XMLSupports

from musictree.core import MusicTree
from musictree.quarterduration import QuarterDuration
from musictree.xmlwrapper import XMLWrapper
from musictree.layout import Scaling, PageLayout, SystemLayout, StaffLayout

__all__ = ['TITLE', 'SUBTITLE', 'POSSIBLE_SUBDIVISIONS', 'Score']
#:
TITLE = {'font_size': 24, 'default_x': {'A4': {'portrait': 616}}, 'default_y': {'A4': {'portrait': 1573}}, 'justify': 'center',
         'valign': 'top'}

#:
SUBTITLE = {'font_size': 18, 'default_x': {'A4': {'portrait': 616}}, 'default_y': {'A4': {'portrait': 1508}}, 'halign': 'center',
            'valign': 'top'}
#:
POSSIBLE_SUBDIVISIONS = {QuarterDuration(1, 4): [2, 3], QuarterDuration(1, 2): [2, 3, 4, 5],
                         QuarterDuration(1): [2, 3, 4, 5, 6, 7, 8]}


class Score(MusicTree, FinalUpdateMixin, XMLWrapper):
    _ATTRIBUTES = {'version', 'title', 'subtitle', 'scaling', 'page_layout', 'system_layout', 'staff_layout'}
    _ATTRIBUTES = _ATTRIBUTES.union(MusicTree._ATTRIBUTES)

    XMLClass = XMLScorePartwise

    def __init__(self, version='4.0', title=None, subtitle=None, quantize=False, *args, **kwargs):

        super().__init__(quantize=quantize)
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._update_xml_object()
        self._version = None
        self._title = None
        self._subtitle = None
        self._page_layout = None
        self._system_layout = None
        self._staff_layout = None
        self._scaling = None

        self.scaling = Scaling()
        self.page_layout = PageLayout()
        self.system_layout = SystemLayout()
        self.version = version
        self.title = title
        self.subtitle = subtitle
        self._possible_subdivisions = POSSIBLE_SUBDIVISIONS.copy()

        self._final_updated = False

    def _get_title_attributes(self):
        output = TITLE.copy()
        output['default_x'] = TITLE['default_x']['A4']['portrait']
        output['default_y'] = TITLE['default_y']['A4']['portrait']
        return output

    def _get_subtitle_attributes(self):
        output = SUBTITLE.copy()
        output['default_x'] = SUBTITLE['default_x']['A4']['portrait']
        output['default_y'] = SUBTITLE['default_y']['A4']['portrait']
        return output

    def _update_xml_object(self):
        self.xml_object.xml_part_list = XMLPartList()
        self.xml_object.xml_identification = XMLIdentification()
        encoding = self.xml_object.xml_identification.xml_encoding = XMLEncoding()
        encoding.add_child(XMLSupports(element='accidental', type='yes'))
        encoding.add_child(XMLSupports(element='beam', type='yes'))
        encoding.add_child(XMLSupports(element='stem', type='yes'))

    @property
    def page_layout(self) -> PageLayout:
        """
        Sets and gets page layout. After setting value, page layout's parent is set to self.

        :type: :obj:`~musictree.pagelayout.PageLayout`
        :return: :obj:`~musictree.pagelayout.PageLayout`
        """
        return self._page_layout

    @page_layout.setter
    def page_layout(self, val):
        if not isinstance(val, PageLayout):
            raise TypeError
        self._page_layout = val
        self.page_layout.parent = self

    @property
    def scaling(self) -> Scaling:
        """
        :type: :obj:`~musictree.scaling.Scaling`
        :return: :obj:`~musictree.scaling.Scaling`
        """
        return self._scaling

    @scaling.setter
    def scaling(self, val):
        if not isinstance(val, Scaling):
            raise TypeError
        val.score = self
        self._scaling = val

    @property
    def staff_layout(self):
        """
        Sets and gets staff layout. After setting value, staff layout's parent is set to self.

        :type: :obj:`~musictree.stafflayout.StaffLayout`
        :return: :obj:`~musictree.stafflayout.StaffLayout`
        """

        return self._staff_layout

    @staff_layout.setter
    def staff_layout(self, val):
        if not isinstance(val, StaffLayout):
            raise TypeError
        self._staff_layout = val
        self.staff_layout.parent = self

    @property
    def subtitle(self):
        """
        - If val is ``None`` and a subtitle object as credit already exists, this object will be removed.
        - If val is not ``None``:
          - if a subtitle exists its ``value_`` will be replaced.
          - else a subtitle as credit will be added.

        :type: Optional[str]
        :return: Optional[str]
        """
        return self._subtitle

    @subtitle.setter
    def subtitle(self, val):
        if val is not None:
            if self._subtitle is None:
                credit = self.xml_object.add_child(XMLCredit(page=1))
                credit.xml_credit_type = 'subtitle'
                self._subtitle = credit.add_child(XMLCreditWords(value_=val, **self._get_subtitle_attributes()))
            else:
                self._subtitle.value_ = val
        else:
            if self._subtitle is None:
                pass
            else:
                credit = self._subtitle.up
                credit.up.remove(credit)
                self._subtitle = None

    @property
    def system_layout(self):
        """
        Sets and gets system layout. After setting value, system layout's parent is set to self.

        :type: :obj:`~musictree.systemlayout.SystemLayout`
        :return: :obj:`~musictree.systemlayout.SystemLayout`
        """
        return self._system_layout

    @system_layout.setter
    def system_layout(self, val):
        if not isinstance(val, SystemLayout):
            raise TypeError
        self._system_layout = val
        self.system_layout.parent = self

    @property
    def title(self):
        """
        - If val is ``None`` and a title object as credit already exists, this object will be removed.
        - If val is not ``None``:
          - if a title exists its ``value_`` will be replaced.
          - else a title as credit will be added.

        :type: Optional[str]
        :return: Optional[str]
        """
        return self._title

    @title.setter
    def title(self, val):
        if val is not None:
            if self._title is None:
                credit = self.xml_object.add_child(XMLCredit(page=1))
                credit.xml_credit_type = 'title'
                self._title = credit.add_child(XMLCreditWords(value_=val, **self._get_title_attributes()))
            else:
                self._title.value_ = val
        else:
            if self._title is None:
                pass
            else:
                credit = self._title.up
                credit.up.remove(credit)
                self._title = None

    @property
    def version(self) -> str:
        """
        :type: Any
        :return: xml_object's version
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, val):
        self._version = str(val)
        self.xml_object.version = self.version

    @XMLWrapper.xml_object.getter
    def xml_object(self) -> XMLClass:
        return super().xml_object

    def add_child(self, child: 'Part') -> 'Part':
        """
        - Check and add child to list of children. Child's parent is set to self.
        - Part's ``xml_object`` is add to score's ``xml_object`` as child
        - Part's ``score_part.xml_object`` is added to score's ``xml_part_list``

        :param child: :obj:`~musictree.part.Part`, required
        :return: child
        :rtype: :obj:`~musictree.part.Part`
        """
        super().add_child(child)
        self.xml_object.add_child(child.xml_object)
        self.xml_part_list.xml_score_part = child.score_part.xml_object
        return child

    def get_children(self) -> List['Part']:
        """
        :return: list of added children.
        :rtype: List[:obj:`~musictree.part.Part`]
        """
        return super().get_children()

    def export_xml(self, path: 'pathlib.Path') -> None:
        """
        :param path: Output xml file
        :return: None
        """
        with open(path, '+w') as f:
            f.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE score-partwise PUBLIC
    "-//Recordare//DTD MusicXML 4.0 Partwise//EN"
    "http://www.musicxml.org/dtds/partwise.dtd">
""")
            f.write(self.to_string())
