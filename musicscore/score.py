from typing import Union, Optional

from musicscore import Part, Chord
from musicscore.chord import Rest
from musicscore.exceptions import AlreadyFinalizedError, ScoreMultiMeasureRestError
from musicscore.finalize import FinalizeMixin
from musicscore.layout import Scaling, PageLayout, SystemLayout, StaffLayout
from musicscore.musictree import MusicTree
from musicscore.quantize import QuantizeMixin
from musicscore.quarterduration import QuarterDuration
from musicscore.xmlwrapper import XMLWrapper
from musicxml.xmlelement.xmlelement import XMLScorePartwise, XMLPartList, XMLCredit, XMLCreditWords, XMLIdentification, \
    XMLEncoding, \
    XMLSupports, XMLScorePart, XMLPartGroup, XMLGroupSymbol, XMLGroupBarline, XMLGroupName, XMLGroupAbbreviation, \
    XMLMeasureStyle

__all__ = ['TITLE', 'SUBTITLE', 'POSSIBLE_SUBDIVISIONS', 'Score']
#:
TITLE = {'font_size': 24, 'default_x': {'A4': {'portrait': 616}}, 'default_y': {'A4': {'portrait': 1573}},
         'justify': 'center',
         'valign': 'top'}

#:
SUBTITLE = {'font_size': 18, 'default_x': {'A4': {'portrait': 616}}, 'default_y': {'A4': {'portrait': 1508}},
            'halign': 'center',
            'valign': 'top'}
#:
POSSIBLE_SUBDIVISIONS = {QuarterDuration(1, 4): [2, 3], QuarterDuration(1, 2): [2, 3, 4, 5],
                         QuarterDuration(1): [2, 3, 4, 5, 6, 7, 8]}


class Score(MusicTree, QuantizeMixin, FinalizeMixin, XMLWrapper):
    """
    Parent type: ``None``

    Child type: :obj:`~musicscore.part.Part`
    """
    _ATTRIBUTES = {'version', 'title', 'subtitle', 'scaling', 'page_layout', 'system_layout', 'staff_layout',
                   'new_system'}
    _ATTRIBUTES = _ATTRIBUTES.union(MusicTree._ATTRIBUTES)
    _ATTRIBUTES = _ATTRIBUTES.union(QuantizeMixin._ATTRIBUTES)

    XMLClass = XMLScorePartwise

    def __init__(self, version='4.0', title=None, subtitle=None, get_quantized=False, new_system=False, *args,
                 **kwargs):

        super().__init__(get_quantized=get_quantized)
        self._xml_object = self.XMLClass(*args, **kwargs)
        self._update_xml_object()
        self._version = None
        self._title = None
        self._subtitle = None
        self._page_layout = None
        self._system_layout = None
        self._staff_layout = None
        self._scaling = None
        self._new_system = None

        self.scaling = Scaling()
        self.page_layout = PageLayout()
        self.system_layout = SystemLayout()
        self.version = version
        self.title = title
        self.subtitle = subtitle
        self.new_system = new_system
        self._possible_subdivisions = POSSIBLE_SUBDIVISIONS.copy()

        self._measure_numbers_within_multi_measure_rests = set()

        self._final_updated = False

    def _create_missing_measures(self):
        number_of_measures = max([len(p.get_children()) for p in self.get_children()])
        longest_parts = [p for p in self.get_children() if len(p.get_children()) == number_of_measures]
        for p in set(self.get_children()).difference(set(longest_parts)):
            for measure_number in range(len(p.get_children()) + 1, number_of_measures + 1):
                p.add_chord(Rest(longest_parts[0].get_measure(measure_number).quarter_duration))

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

    def _set_last_barline(self):
        last_measures = [p.get_children()[-1] for p in self.get_children() if p.get_children()]
        try:
            if not last_measures[0].get_barline():
                for m in last_measures:
                    m.set_barline(style='light-heavy')
        except IndexError:
            pass

    def _set_missing_barlines(self):
        for measures in zip(*[p.get_children() for p in self.get_children()]):
            right_barline = None
            left_barline = None
            for m in measures:
                if m.get_barline(location='right'):
                    right_barline = m.get_barline(location='right')
                    break
            for m in measures:
                if m.get_barline(location='left'):
                    left_barline = m.get_barline(location='left')
                    break
            if right_barline:
                for m in measures:
                    m._barlines['right'] = right_barline
            if left_barline:
                for m in measures:
                    m._barlines['left'] = left_barline

    def _update_xml_object(self):
        self.xml_object.xml_part_list = XMLPartList()
        self.xml_object.xml_identification = XMLIdentification()
        encoding = self.xml_object.xml_identification.xml_encoding = XMLEncoding()
        encoding.add_child(XMLSupports(element='accidental', type='yes'))
        encoding.add_child(XMLSupports(element='beam', type='yes'))
        encoding.add_child(XMLSupports(element='stem', type='yes'))

    @property
    def new_system(self) -> bool:
        """
        Set or get new_system property. It will be automatically set to ``True`` if a :obj:`~musicscore.measure.Measure` sets its :obj:`musicscore.measure.Measure.new_system` to ``True``. ``<encoding>`` in :obj:`~musicxml.xmlelement.xmlelement.XMLScorePartwise`\'s ``<identification>`` will have a ``<support>`` child with attribute ``new-system`` if :obj:`musicscore.score.Score.new_system` is set to ``True``.
        """
        return self._new_system

    @new_system.setter
    def new_system(self, val):

        if isinstance(val, bool):
            self._new_system = val
        else:
            raise TypeError(f"new_system {val} must be of type bool and not {val.__class__}")
        encoding = self.xml_object.xml_identification.xml_encoding
        new_system_supports = [sup for sup in encoding.get_children_of_type(XMLSupports) if
                               sup.attribute == 'new-system']
        if self.new_system:
            if not new_system_supports:
                self.xml_object.xml_identification.xml_encoding.add_child(
                    XMLSupports(attribute='new-system', element='print', type='yes', value='yes'))
        else:
            if new_system_supports:
                self.xml_object.xml_identification.xml_encoding.remove(new_system_supports[0])

    @property
    def page_layout(self) -> PageLayout:
        """
        Set and get page layout. After setting value, page layout's parent is set to self.

        :type: :obj:`~musicscore.pagelayout.PageLayout`
        :return: :obj:`~musicscore.pagelayout.PageLayout`
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
        :type: :obj:`~musicscore.scaling.Scaling`
        :return: :obj:`~musicscore.scaling.Scaling`
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
        Set and get staff layout. After setting value, staff layout's parent is set to self.

        :type: :obj:`~musicscore.stafflayout.StaffLayout`
        :return: :obj:`~musicscore.stafflayout.StaffLayout`
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
        Set and get system layout. After setting value, system layout's parent is set to self.

        :type: :obj:`~musicscore.systemlayout.SystemLayout`
        :return: :obj:`~musicscore.systemlayout.SystemLayout`
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

    def add_child(self, child: 'Part') -> 'Part':
        """
        - Check and add child to list of children. Child's parent is set to self.
        - Part's ``xml_object`` is add to score's ``xml_object`` as child
        - Part's ``score_part.xml_object`` is added to score's ``xml_part_list``

        :param child: :obj:`~musicscore.part.Part`, required
        :return: child
        :rtype: :obj:`~musicscore.part.Part`
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_child')
        super().add_child(child)
        self.xml_object.add_child(child.xml_object)
        if not self.xml_part_list:
            self.xml_part_list.xml_score_part = child.score_part.xml_object
        else:
            self.xml_part_list.add_child(child.score_part.xml_object)
        return child

    def add_part(self, id: str) -> 'Part':
        """
        Creates and adds part

        :param id: part's id
        :return: part
        """
        if self._finalized is True:
            raise AlreadyFinalizedError(self, 'add_part')
        p = Part(id)
        return self.add_child(p)

    def export_xml(self, path: 'pathlib.Path') -> None:
        """
        Creates a musicxml file

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

    def finalize(self) -> None:
        self._create_missing_measures()
        self._set_missing_barlines()
        self._set_last_barline()
        super().finalize()
        for measure_number in self._measure_numbers_within_multi_measure_rests:
            for part in self.get_children():
                measure = part.get_measure(measure_number)
                for ch in measure.get_chords():
                    ch.notes[0].xml_rest.measure = 'yes'

    def group_parts(self, number: Union[int, str], start_part_number: int, end_part_number: int, symbol: str = 'square',
                    name: Optional[str] = None, abbreviation: Optional[str] = None,
                    **kwargs) -> None:
        """
        Adds a XMLPartList child

        :param number: sets number property of :obj:`~musicxml.xmlelement.xmlelement.XMLPartGroup`
        :param start_part_number: number of part to start the group
        :param end_part_number: number of part to end the group
        :param symbol: symbol property of :obj:`~musicxml.xmlelement.xmlelement.XMLGroupSymbol`:'none', 'brace', 'line', 'bracket', 'square'; default: 'square'
        :param name: value of :obj:`~musicxml.xmlelement.xmlelement.XMLGroupName`
        :param abbreviation: value of :obj:`~musicxml.xmlelement.xmlelement.XMLGroupAbbreviation`
        :param kwargs: kwargs of :obj:`~musicxml.xmlelement.xmlelement.XMLGroupSymbol`
        :return: None
        """
        parts = self.get_children_of_type(Part)
        for part_number in [start_part_number, end_part_number]:
            if not 0 < part_number <= len(parts):
                raise ValueError(f'Wrong part number {part_number}. Permitted between 1 and {len(parts)}')
        if not start_part_number < end_part_number:
            raise ValueError(
                f'Wrong part numbers. start_part_number {start_part_number} must be smaller than end_part_number {end_part_number}')

        new_xml_part_list = XMLPartList(xsd_check=False)
        for child in self.xml_part_list.get_children():
            if isinstance(child, XMLScorePart) and child.id == parts[start_part_number - 1].id_.value:
                pg = new_xml_part_list.add_child(XMLPartGroup(number=str(number), type='start'))
                pg.add_child(XMLGroupSymbol(symbol, **kwargs))
                pg.add_child(XMLGroupBarline('yes'))
                if name:
                    pg.add_child(XMLGroupName(name))
                if abbreviation:
                    pg.add_child(XMLGroupAbbreviation(abbreviation))
            new_xml_part_list.add_child(child)
            if isinstance(child, XMLScorePart) and child.id == parts[end_part_number - 1].id_.value:
                new_xml_part_list.add_child(XMLPartGroup(number=str(number), type='stop'))

        self.xml_part_list = new_xml_part_list

    def set_multi_measure_rest(self, first_measure_number: int, last_measure_number: int) -> None:
        """
        Creates a multi measure rest

        :param first_measure_number: number of measure to start the multi measure rest
        :param last_measure_number: number of measure to end the multi measure rest
        :return: None
        """

        if len(self.get_children()) == 0:
            raise ScoreMultiMeasureRestError(f'score has no parts.')
        if last_measure_number <= first_measure_number:
            raise ScoreMultiMeasureRestError(
                f'last_measure_number {last_measure_number} must be larger than first_measure_number {first_measure_number}')
        for x in range(first_measure_number, last_measure_number + 1):
            if x in self._measure_numbers_within_multi_measure_rests:
                raise ScoreMultiMeasureRestError(f'measure number {x} is already part of a multiple measure reset')
        for part in self.get_children():
            for _ in range(last_measure_number - len(part.get_children())):
                m = part.add_measure()
                part.add_chord(Chord(0, m.quarter_duration))

            for measure in part.get_children()[first_measure_number - 1:last_measure_number]:
                for ch in measure.get_chords():
                    if not ch.is_rest:
                        raise ScoreMultiMeasureRestError(
                            f'Measures contain not rest chords')

            first_measure = part.get_measure(first_measure_number)
            if not first_measure.xml_attributes.xml_measure_style:
                first_measure.xml_attributes.xml_measure_style = XMLMeasureStyle()
            first_measure.xml_attributes.xml_measure_style.xml_multiple_rest = last_measure_number - first_measure_number + 1
            if part == self.get_children()[0]:
                self._measure_numbers_within_multi_measure_rests.update(
                    {x for x in range(first_measure_number, last_measure_number + 1)})

    def write(self, *args, **kwargs):
        """
        Not implemented. Use Score.export_xml instead!
        """
        raise NotImplementedError('Use Score.export_xml instead!')
