from typing import Optional, Union

from musicxml import XMLAccidental

from musicscore.musictree import MusicTree
from musicscore.xmlwrapper import XMLWrapper

__all__ = ['STANDARD', 'FLAT', 'SHARP', 'ENHARMONIC', 'FORCESHARP', 'FORCEFLAT', 'SIGNS', 'Accidental']
#:
STANDARD = {
    0: ('C', 0, 0),
    0.5: ('C', 0.5, 0),
    1: ('C', 1, 0),
    1.5: ('C', 1.5, 0),
    2: ('D', 0, 0),
    2.5: ('E', -1.5, 0),
    3: ('E', -1, 0),
    3.5: ('E', -0.5, 0),
    4: ('E', 0, 0),
    4.5: ('E', 0.5, 0),
    5: ('F', 0, 0),
    5.5: ('F', 0.5, 0),
    6: ('F', 1, 0),
    6.5: ('F', 1.5, 0),
    7: ('G', 0, 0),
    7.5: ('A', -1.5, 0),
    8: ('A', -1, 0),
    8.5: ('A', -0.5, 0),
    9: ('A', 0, 0),
    9.5: ('B', -1.5, 0),
    10: ('B', -1, 0),
    10.5: ('B', -0.5, 0),
    11: ('B', 0, 0),
    11.5: ('C', -0.5, 1)
}

#:
FLAT = {
    0: ('C', 0, 0),
    0.5: ('D', -1.5, 0),
    1: ('D', -1, 0),
    1.5: ('D', -0.5, 0),
    2: ('D', 0, 0),
    2.5: ('E', -1.5, 0),
    3: ('E', -1, 0),
    3.5: ('E', -0.5, 0),
    4: ('E', 0, 0),
    4.5: ('F', -0.5, 0),
    5: ('F', 0, 0),
    5.5: ('G', -1.5, 0),
    6: ('G', -1, 0),
    6.5: ('G', -0.5, 0),
    7: ('G', 0, 0),
    7.5: ('A', -1.5, 0),
    8: ('A', -1, 0),
    8.5: ('A', -0.5, 0),
    9: ('A', 0, 0),
    9.5: ('B', -1.5, 0),
    10: ('B', -1, 0),
    10.5: ('B', -0.5, 0),
    11: ('B', 0, 0),
    11.5: ('C', -0.5, 1)
}

#:
SHARP = {
    0: ('C', 0, 0),
    0.5: ('C', 0.5, 0),
    1: ('C', 1, 0),
    1.5: ('C', 1.5, 0),
    2: ('D', 0, 0),
    2.5: ('D', 0.5, 0),
    3: ('D', 1, 0),
    3.5: ('D', 1.5, 0),
    4: ('E', 0, 0),
    4.5: ('E', 0.5, 0),
    5: ('F', 0, 0),
    5.5: ('F', 0.5, 0),
    6: ('F', 1, 0),
    6.5: ('F', 1.5, 0),
    7: ('G', 0, 0),
    7.5: ('G', 0.5, 0),
    8: ('G', 1, 0),
    8.5: ('G', 1.5, 0),
    9: ('A', 0, 0),
    9.5: ('A', 0.5, 0),
    10: ('A', 1, 0),
    10.5: ('A', 1.5, 0),
    11: ('B', 0, 0),
    11.5: ('B', 0.5, 0)
}

#:
ENHARMONIC = {
    0: ('C', 0, 0),
    0.5: ('D', -1.5, 0),
    1: ('D', -1, 0),
    1.5: ('D', -0.5, 0),
    2: ('D', 0, 0),
    2.5: ('D', 0.5, 0),
    3: ('D', 1, 0),
    3.5: ('D', 1.5, 0),
    4: ('E', 0, 0),
    4.5: ('F', -0.5, 0),
    5: ('F', 0, 0),
    5.5: ('G', -1.5, 0),
    6: ('G', -1, 0),
    6.5: ('G', -0.5, 0),
    7: ('G', 0, 0),
    7.5: ('G', 0.5, 0),
    8: ('G', 1, 0),
    8.5: ('G', 1.5, 0),
    9: ('A', 0, 0),
    9.5: ('A', 0.5, 0),
    10: ('A', 1, 0),
    10.5: ('A', 1.5, 0),
    11: ('B', 0, 0),
    11.5: ('B', 0.5, 0)
}

#:
FORCESHARP = {
    0: ('B', 1, -1),
    0.5: ('B', 1.5, -1),
    1: ('B', 2, -1),
    1.5: ('C', 1.5, 0),
    2: ('C', 2, 0),
    2.5: ('D', 0.5, 0),
    3: ('D', 1, 0),
    3.5: ('D', 1.5, 0),
    4: ('D', 2, 0),
    4.5: ('E', 0.5, 0),
    5: ('E', 1, 0),
    5.5: ('E', 1.5, 0),
    6: ('E', 2, 0),
    6.5: ('F', 1.5, 0),
    7: ('F', 2, 0),
    7.5: ('G', 0.5, 0),
    8: ('G', 1, 0),
    8.5: ('G', 1.5, 0),
    9: ('G', 2, 0),
    9.5: ('A', 0.5, 0),
    10: ('A', 1, 0),
    10.5: ('A', 1.5, 0),
    11: ('A', 2, 0),
    11.5: ('B', 0.5, 0)
}

#:
FORCEFLAT = {
    0: ('D', -2, 0),
    0.5: ('D', -1.5, 0),
    1: ('D', -1, 0),
    1.5: ('D', -0.5, 0),
    2: ('E', -2, 0),
    2.5: ('E', -1.5, 0),
    3: ('F', -2, 0),
    3.5: ('F', -1.5, 0),
    4: ('F', -1, 0),
    4.5: ('F', -0.5, 0),
    5: ('G', -2, 0),
    5.5: ('G', -1.5, 0),
    6: ('G', -1, 0),
    6.5: ('G', -0.5, 0),
    7: ('A', -2, 0),
    7.5: ('A', -1.5, 0),
    8: ('A', -1, 0),
    8.5: ('A', -0.5, 0),
    9: ('B', -2, 0),
    9.5: ('B', -1.5, 0),
    10: ('C', -2, 1),
    10.5: ('C', -1.5, 1),
    11: ('C', -1, 1),
    11.5: ('C', -0.5, 1)
}

#:
SIGNS = {-2: 'flat-flat',
         -1.5: 'three-quarters-flat',
         -1: 'flat',
         -0.5: 'quarter-flat',
         0: 'natural',
         0.5: 'quarter-sharp',
         1: 'sharp',
         1.5: 'three-quarters-sharp',
         2: 'double-sharp'
         }


class Accidental(MusicTree, XMLWrapper):
    """
    Parent type: :obj:`~musicscore.midi.Midi`

    Child type: None

    Accidental is the class for managing :obj:`musicscore.midi.Midi`'s accidental sign and its pitch parameters: step, alter, octave.
    The parameter mode ('standard', 'enharmonic', 'flat', 'sharp', 'force-flat', 'force-sharp') can be used to set different enharmonic variants of the same
    pitch.
    """
    _ATTRIBUTES = {'mode', 'show', 'parent_midi'}

    XMLClass = XMLAccidental

    def __init__(self, mode='standard', show: Optional[bool] = None, **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(value_='natural', **kwargs)
        self._mode = None
        self._show = None
        self.show = show
        self.mode = mode

    def _update(self):
        self._update_parent_midi()
        self._update_xml_object()

    def _update_parent_midi(self):
        if self.parent_midi and self.parent_midi.value != 0:
            self.parent_midi._update_pitch_parameters()

    def _update_xml_object(self):
        if self.sign:
            self._xml_object.value_ = self.sign

    @XMLWrapper.xml_object.getter
    def xml_object(self) -> Optional[XMLClass]:
        """
        If an attribute is not found directly in a :obj:`~musicscore.musictree.MusicTree` class which inherits this class, it wll be passed on to ``__get_attribute__`` and ``__set__attribute__`` methods of ``xml_object``.
        It can also use the short cut attributes of :obj:`~musicxml.xmlelement.xmlelement.XMLElement` to get or set the first child.

        :return: wrapped MusicXML element of type :obj:`XMLClass`
        """
        if self.parent_midi and self.parent_midi.value == 0:
            return None
        if self.show is True:
            return self._xml_object
        elif self.show is False:
            return None

    @property
    def mode(self):
        """
        permitted modes: ``standard``, ``flat``, ``sharp``, ``enharmonic``, ``force-sharp``, ``force-flat``

        :return: accidental mode which corresponds to global variables :obj:`~musicscore.accidental.STANDARD`, :obj:`~musicscore.accidental.FLAT`, :obj:`~musicscore.accidental.SHARP`,
                 :obj:`~musicscore.accidental.ENHARMONIC`, :obj:`~musicscore.accidental.FORCESHARP`, :obj:`~musicscore.accidental.FORCEFLAT`
        """
        return self._mode

    @mode.setter
    def mode(self, value):
        permitted = ('standard', 'flat', 'sharp', 'enharmonic', 'force-sharp', 'force-flat')
        if value not in permitted:
            raise TypeError(f'accidental_mode.value {value} must be in {permitted}')
        self._mode = value
        self._update_xml_object()
        self._update_parent_midi()

    @property
    def parent_midi(self) -> 'Midi':
        """
        :return: The midi parent of Accidental in the :obj:`~musicscore.musictree.MusicTree` structure. It is equivalent to :obj:`up` or :obj:`get_parent()`
        :rtype: :obj:`musicscore.midi.Midi`
        """
        return self.up

    @parent_midi.setter
    def parent_midi(self, val):
        val.add_child(self)

    @property
    def sign(self) -> Optional[str]:
        """
        Converts ``alter`` parameter of :obj:`~get_pitch_parameters` into an actual ``sign`` depending on :obj:`~mode`. :obj:`~parent_midi` must be set first.

        :return: Possible values: ``flat-flat``, ``three-quarters-flat``, ``flat``, ``quarter-flat``, ``natural``,
                 ``quarter-sharp``, ``sharp``, ``three-quarters-sharp``, ``double-sharp``
        """
        try:
            alter = self.get_pitch_parameters()[1]
            return SIGNS[alter]
        except TypeError:
            return None

    @property
    def show(self) -> bool:
        """
        If ``False`` ``xml_object`` will be ``None`` and no accidental is shown in the :obj:`~musicscore.score.Score`.
        If ``True`` the accidental is shown. If the value of one of the following xml_object :obj:`~musicxml.xmlelement.xmlelement.XMLAccidental` properties:``self.parentheses``, ``self.editorial``.
        ``self.cautionary`` or ``self.bracket`` is set to yes, the accidental is always shown regardless of this
        property
        """
        if 'yes' in [self.parentheses, self.editorial, self.cautionary, self.bracket]:
            return True
        return self._show

    @show.setter
    def show(self, val):
        if val is not None and not isinstance(val, bool):
            raise TypeError
        if val != self._show:
            self._show = val
            try:
                self.up.up._update_xml_accidental()
            except AttributeError:
                pass

    def get_pitch_parameters(self, midi_value: Optional[Union[int, float]] = None) -> Optional[tuple]:
        """
        :param: a valid midi value or ``None``. If ``midi_value == 0`` (for a rest) return value is ``None``. If ``midi_value is None`` and a :obj:`~parent_midi` exists, parent_midi's value will be used.

        :return: A tuple consisting of pitch step name, alter value and octave value: ``(step, alter, octave)``

        .. seealso::
           :obj:`~mode`
        """

        if midi_value is None:
            if self.parent_midi:
                midi_value = self.parent_midi.value
            else:
                return None
        if midi_value == 0:
            return None

        if self.mode == 'standard':
            output = STANDARD[midi_value % 12]

        elif self.mode == 'enharmonic':
            output = ENHARMONIC[midi_value % 12]

        elif self.mode == 'force-sharp':
            output = FORCESHARP[midi_value % 12]

        elif self.mode == 'force-flat':
            output = FORCEFLAT[midi_value % 12]

        elif self.mode == 'flat':
            output = FLAT[midi_value % 12]

        elif self.mode == 'sharp':
            output = SHARP[midi_value % 12]

        else:
            raise ValueError
        return output[0], output[1], output[2] + (int(midi_value // 12)) - 1

    def __copy__(self):
        return self.__class__(mode=self.mode, show=self.show)
