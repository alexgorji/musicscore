from quicktions import Fraction

from musicscore.basic_functions import Scale, dToX, xToD
from musicscore.dtd.dtd import Sequence, Choice, Element, GroupReference
from musicscore.musictree.midi import Midi
from musicscore.musictree.treechordflags1 import TreeChordFlag1
from musicscore.musictree.treechordflags2 import TreeChordFlag2
from musicscore.musictree.treechordflags3 import TreeChordFlag3
from musicscore.musictree.treeclef import TreeClef
from musicscore.musicxml.elements.fullnote import Chord, FullNote, Rest, Event, Pitch, Alter
from musicscore.musicxml.elements.note import Cue, Tie, Instrument, Play, Lyric, Notations, Stem, TimeModification, \
    Type, Dot, Notehead, NoteheadText, Beam, Duration, Accidental, Note, Grace
from musicscore.musicxml.elements.xml_element import XMLTree
from musicscore.musicxml.groups.common import EditorialVoice, Staff, Voice, StaffElement
from musicscore.musicxml.groups.musicdata import Direction, Attributes, Backup
from musicscore.musicxml.types.complextypes.articulations import Accent, StrongAccent, DetachedLegato, Tenuto, Spiccato, \
    Staccato, Staccatissimo, BreathMark, Caesura, Stress, Unstress, Plop, Scoop, Doit, Falloff
from musicscore.musicxml.types.complextypes.direction import DirectionType
from musicscore.musicxml.types.complextypes.directiontype import Words, Bracket, Wedge
from musicscore.musicxml.types.complextypes.dynamics import P, PP, PPP, PPPP, PPPPP, PPPPPP, F, FF, FFF, FFFF, FFFFF, \
    FFFFFF, MP, MF, SF, SFP, SFPP, FP, RF, SFZP, PF, FZ, SFFZ, SFZ, RFZ, N, Dynamics
from musicscore.musicxml.types.complextypes.lyric import Text
from musicscore.musicxml.types.complextypes.notations import Tied, Tuplet, Ornaments, Technical, \
    Articulations, Slur, Fermata, Slide
from musicscore.musicxml.types.complextypes.ornaments import Tremolo
from musicscore.musicxml.types.complextypes.timemodification import ActualNotes, NormalNotes, NormalType


class TreeBackup(Backup):
    def __init__(self, quarter_duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_duration = None
        self.quarter_duration = quarter_duration

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        self._quarter_duration = value

    def update_duration(self, divisions):
        try:
            self.get_children_by_type(Duration)[0].value = int(self.quarter_duration * divisions)
        except IndexError:
            self.add_child(Duration())
            self.duration.value = int(self.quarter_duration * divisions)


class TreeAccidental(Accidental):
    """"""

    def __init__(self, value='natural', show=False, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        self._note = None
        self._show = None
        self._force_show = None
        self._force_hide = None

        self.show = show

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, value):
        if not isinstance(value, bool):
            raise TypeError('show.value must be of type bool not{}'.format(type(value)))
        self._show = value
        if self._note:
            self._note.update_accidental()

    def set_force_show(self, value):
        self._force_show = value

    def set_force_hide(self, value):
        self._force_hide = value


class TreeNote(Note):
    # todo: Inheritance Chain must be Midi, MidiNote, TreeMidiNote (or TreeNote)
    """
    quarter_duration = 0 means grace note
    """

    def __init__(self, parent_chord, event=Rest(), is_tied=False, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._parent_chord = None
        self._accidental = TreeAccidental(show=False, value='natural')
        self._accidental._note = self
        self._event = None
        self.event = event
        self._offset = None
        self._is_tied = False

        self.parent_chord = parent_chord
        self.is_tied = is_tied
        self.is_finger_tremolo = False

    # // private methods
    def _add_notations(self, notation):
        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        notations.add_child(notation)

    # //public properties
    @property
    def accidental(self):
        return self._accidental

    @property
    def end_position(self):
        return self.parent_chord.end_postion

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        if not isinstance(value, Event):
            raise TypeError('event.value must be of type  not{}'.format(type(value)))
        try:
            self.remove_child(self._event)
        except ValueError as err:
            print(err)
            pass
        self._event = self.add_child(value)
        self.update_accidental()

    @property
    def offset(self):
        return self.parent_chord.offset

    @property
    def parent_chord(self):
        return self._parent_chord

    @parent_chord.setter
    def parent_chord(self, val):
        if not isinstance(val, TreeChord):
            raise TypeError('parent_chord.value must be of type TreeChord not{}'.format(type(val)))
        self._parent_chord = val

    @property
    def quarter_duration(self):
        return self.parent_chord.quarter_duration

    # // public methods
    # add
    def add_lyric(self, text, number=1, **kwargs):
        lyric = self.add_child(Lyric(number=str(number), **kwargs))
        lyric.add_child(Text(str(text)))
        return lyric

    # update
    def update_accidental(self):
        _accidentals = {-1.5: 'three-quarters-flat',
                        -1: 'flat',
                        -0.5: 'quarter-flat',
                        0: 'natural',
                        0.5: 'quarter-sharp',
                        1: 'sharp',
                        1.5: 'three-quarters-sharp',
                        2: 'double-sharp'
                        }
        accidental = self.get_children_by_type(type_=TreeAccidental)
        if self._accidental.show:
            if isinstance(self.event, Pitch):
                alter = self.event.get_children_by_type(type_=Alter)
                if not alter:
                    self.event.add_child(Alter(0))

                accidental_value = _accidentals[self.event.alter.value]
                if accidental:
                    accidental[0].value = accidental_value
                else:
                    self._accidental.value = accidental_value
                    self.add_child(self._accidental)
        else:
            if accidental:
                self.remove_child(accidental[0])

    def update_duration(self, divisions):
        try:
            self.duration.value = int(self.quarter_duration * divisions)
        except AttributeError:
            self.add_child(Duration())
            self.duration.value = int(self.quarter_duration * divisions)

    def update_grace(self):
        if self.quarter_duration == 0:
            if not self.get_children_by_type(Grace):
                children = self.get_children()[:]
                self.reset_dtd()
                for child in children:
                    if not isinstance(child, Duration):
                        self.add_child(child)
                    else:
                        del child
                self.add_child(Grace())


class TreeChord(XMLTree):
    _DTD = Sequence(
        Choice(
            Sequence(
                GroupReference(FullNote),
                Element(Duration),
                Element(Tie, 0, 2)
            ),
            Sequence(
                Element(Cue),
                GroupReference(FullNote),
                Element(Duration)
            ),
        ),
        Element(Attributes, 0),
        Element(Direction, 0, None),
        Element(Instrument, 0),
        GroupReference(EditorialVoice, 0),
        Element(Type, 0),
        Element(Dot, 0, None),
        Element(TimeModification, 0, None),
        Element(Stem, 0),
        Element(Notehead, 0),
        Element(NoteheadText, 0),
        GroupReference(Staff, 0),
        Element(Beam, 0, 8),
        Element(Notations, 0, None),
        Element(Lyric, 0, None),
        Element(Play, 0)
    )

    def __init__(self, midis=71, quarter_duration=1, zero_mode='grace', **kwargs):
        super().__init__(**kwargs)
        self.parent_tree_part_voice = None
        self.parent_beat = None
        self._notes = None
        self._offset = None
        self._quarter_duration = None
        self._zero_mode = None
        self.zero_mode = zero_mode
        self.quarter_duration = quarter_duration
        self._midis = None
        self._pre_grace_chords = []
        self._post_grace_chords = []

        self.midis = midis
        self._tail = False
        self._head = False
        self._is_adjoinable = True
        self._flags = None

        self._manual_type = False
        self._manual_dots = False
        self._manual_staff_number = None
        self.manual_voice_number = None
        self.is_finger_tremolo = False
        self.relative_x = None
        self.tie_orientation = None

    # //private methods
    def _generate_notes(self):
        output = []
        if self.zero_mode == 'remove' and self.quarter_duration == 0:
            return output

        for index, midi in enumerate(self.midis):
            note = TreeNote(parent_chord=self, event=midi.get_pitch_rest())
            note.update_grace()
            note.accidental.set_force_show(midi.accidental.force_show)
            note.accidental.set_force_hide(midi.accidental.force_hide)
            note.is_finger_tremolo = self.is_finger_tremolo
            if self.relative_x is not None:
                note.relative_x = self.relative_x
            if midi.notehead:
                note.add_child(midi.notehead)

            for child in self.get_children():
                if isinstance(child, Lyric) and index != 0:
                    pass

                elif isinstance(child, Notations) and index != 0:
                    grandchildren = child.get_children()
                    for grandchild in grandchildren:
                        if type(grandchild) not in (Ornaments, Technical, Articulations, Dynamics):
                            note._add_notations(grandchild)
                elif isinstance(child, Direction):
                    pass
                elif isinstance(child, Attributes):
                    pass
                else:
                    note.add_child(child)
            if index > 0:
                note.add_child(Chord())
            output.append(note)
        return output

    def _get_staff_object(self):
        try:
            return self.get_children_by_type(StaffElement)[0]
        except IndexError:
            return None

    def _get_direction_types(self):
        output = []
        for direction in self.get_children_by_type(Direction):
            for dt in direction.get_children_by_type(DirectionType):
                output.append(dt)
        return output

    def _remove_direction(self, direction):
        self.remove_child(direction)

    def _remove_direction_type(self, direction_type):
        parent = direction_type.up
        parent.remove_child(direction_type)
        if not parent.get_children():
            self._remove_direction(parent)

    def _set_staff_number(self, val):
        if not isinstance(val, int):
            raise TypeError('staff_number.value must be of type int not{}'.format(type(val)))
        staff = self._get_staff_object()
        if staff is None:
            self.add_child(StaffElement(val))
        else:
            staff.value = val

    # //public properties
    @property
    def end_position(self):
        return self.offset + self.quarter_duration

    @property
    def flags(self):

        if self._flags is None:
            self._flags = set()
        return self._flags

    @property
    def is_adjoinable(self):
        return self._is_adjoinable

    @is_adjoinable.setter
    def is_adjoinable(self, value):
        if not isinstance(value, bool):
            raise TypeError('is_adjoinable.value must be of type bool not{}'.format(type(value)))
        self._is_adjoinable = value

    @property
    def is_head(self):
        return self._head

    @property
    def is_rest(self):
        if self.midis[0].value == 0:
            return True
        return False

    @property
    def is_tail(self):
        return self._tail

    @property
    def is_tied_to_next(self):
        if 'start' in self.tie_types:
            return True
        return False

    @property
    def is_tied_to_previous(self):
        if 'stop' in self.tie_types:
            return True
        return False

    @property
    def manual_staff_number(self):
        return self._manual_staff_number

    @manual_staff_number.setter
    def manual_staff_number(self, val):
        if not isinstance(val, int):
            raise TypeError('manual_staff_number.value must be of type int not{}'.format(type(val)))
        self._manual_staff_number = val
        self._set_staff_number(val)

    @property
    def midis(self):
        return self._midis

    @midis.setter
    def midis(self, values):
        try:
            values = list(values)
        except TypeError:
            values = [values]

        output = []
        for midi in values:
            if not isinstance(midi, Midi):
                output.append(Midi(midi))
            else:
                output.append(midi)

        for midi in output:
            if midi.value == 0 and len(values) > 1:
                raise ValueError('midi with value 0 must be alone.')

        output = sorted(output, key=lambda midi: midi.value)

        self._midis = output

    @property
    def notes(self):
        if self._notes is None:
            self._notes = self._generate_notes()
        return self._notes

    @property
    def next_in_score(self):
        index = self.parent_tree_part_voice.chords.index(self)
        if index == len(self.parent_tree_part_voice.chords) - 1:
            current_part = self.parent_tree_part_voice.parent_tree_part_staff.parent_part
            next_measure = current_part.up.next
            if next_measure:
                next_part = next_measure.get_part_with_id(id=current_part.id)
                next_chord = next_part.get_staff(self.parent_tree_part_voice.parent_tree_part_staff.number).get_voice(
                    self.parent_tree_part_voice.number).chords[0]
                return next_chord
            else:
                return None
        else:
            return self.parent_tree_part_voice.chords[index + 1]

    @property
    def offset(self):
        if self._offset is None:
            self.update_offset()
        return self._offset

    @property
    def position_in_beat(self):
        index_in_beat = self.parent_beat.chords.index(self)
        if index_in_beat == 0:
            return 0
        previous_in_beat = self.parent_beat.chords[index_in_beat - 1]

        return previous_in_beat.position_in_beat + previous_in_beat.quarter_duration

    @property
    def previous_in_part_voice(self):
        index = self.parent_tree_part_voice.chords.index(self)
        if index == 0:
            return None
        return self.parent_tree_part_voice.chords[index - 1]

    @property
    def previous_in_score_voice(self):
        if self.previous_in_part_voice is None:
            current_part = self.parent_tree_part_voice.parent_tree_part_staff.parent_part
            previous_measure = current_part.up.previous
            if previous_measure:
                previous_part = previous_measure.get_part_with_id(id=current_part.id)
                previous_chord = \
                    previous_part.get_staff(self.parent_tree_part_voice.parent_tree_part_staff.number).get_voice(
                        self.parent_tree_part_voice.number).chords[-1]
                return previous_chord
            else:
                return None
        else:
            return self.previous_in_part_voice

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, Fraction):
            raise TypeError('quarter_duration must be of type int, float or Fraction not {}'.format(type(value)))

        if value < 0:
            raise ValueError('quarter_duration {} must be zero or positive'.format(value))

        if not isinstance(self.quarter_duration, Fraction):
            self._quarter_duration = Fraction(value)
        else:
            self._quarter_duration = value

    @property
    def staff_number(self):
        staff = self._get_staff_object()
        if staff:
            return staff.value
        else:
            return None

    @staff_number.setter
    def staff_number(self, val):
        if self.manual_staff_number is None:
            self._set_staff_number(val)

    @property
    def tie_types(self):
        return [tie.type for tie in self.get_children_by_type(Tie)]

    @property
    def tremoli(self):
        try:
            return self.get_children_by_type(Notations)[0].get_children_by_type(Ornaments)[0].get_children_by_type(
                Tremolo)
        except IndexError:
            return []

    def update_offset(self):
        if self.previous_in_part_voice:
            output = self.previous_in_part_voice.offset + self.previous_in_part_voice.quarter_duration
            self._offset = output
        else:
            self._offset = 0

    @property
    def zero_mode(self):
        return self._zero_mode

    @zero_mode.setter
    def zero_mode(self, val):
        permitted = ['remove', 'grace']
        if val not in permitted:
            raise ValueError('zero_mode.value {} must be in {}'.format(val, permitted))
        self._zero_mode = val

    @property
    def __name__(self):
        # return self.parent_tree_part_voice.__name__ + ' ' + 'ch:' + str(self.parent_tree_part_voice.chords.index(self) + 1)
        return self.parent_tree_part_voice.__name__ + '.' + str(self.parent_tree_part_voice.chords.index(self) + 1)

    # //public methods
    # add

    def add_action_dynamics(self, value, **kwargs):
        dynamics = self.add_dynamics(value, **kwargs)
        direction = dynamics.up.up
        direction_type = direction.add_child(DirectionType())

        direction_type.add_child(Words(value='"', font_size=20))
        for child in direction.get_children():
            if child.get_children_by_type(Dynamics):
                direction.remove_child(child)

        direction_type = direction.add_child(DirectionType())
        direction_type.add_child(dynamics)
        direction_type = direction.add_child(DirectionType())
        direction_type.add_child(Words(value=' "', font_size=20))

    def add_articulation(self, articulation, **kwargs):

        def add_type(dict):
            new_dict = dict.copy()
            if 'type' not in new_dict:
                new_dict['type'] = 'up'
            return new_dict

        def add_breath_mark_value(dict):
            new_dict = dict.copy()
            if 'value' not in new_dict:
                new_dict['value'] = 'comma'
            return new_dict

        articulations = {'accent': Accent(**kwargs),
                         'strong-accent': StrongAccent(**add_type(kwargs)),
                         'staccato': Staccato(**kwargs),
                         'tenuto': Tenuto(**kwargs),
                         'detached-legato': DetachedLegato(**kwargs),
                         'staccatissimo': Staccatissimo(**kwargs),
                         'spiccato': Spiccato(**kwargs),
                         'scoop': Scoop(**kwargs),
                         'plop': Plop(**kwargs),
                         'doit': Doit(**kwargs),
                         'falloff': Falloff(**kwargs),
                         'breath-mark': BreathMark(**add_breath_mark_value(kwargs)),
                         'caesura': Caesura(**kwargs),
                         'stress': Stress(**kwargs),
                         'unstress': Unstress(**kwargs)}

        if articulation not in articulations:
            raise ValueError('articulation {}  must be in {}'.format(articulation, list(articulations.keys())))

        return self.add_articulation_object(articulations[articulation])

    def add_articulation_object(self, articulation_object):

        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        try:
            articulations = notations.get_children_by_type(Articulations)[0]
        except IndexError:
            articulations = notations.add_child(Articulations())

        articulations.add_child(articulation_object)

    def add_bracket(self, type, line_end, placement='above', **kwargs):
        d = self.add_child(Direction(placement=placement))
        dt = d.add_child(DirectionType())
        dt.add_child(Bracket(type=type, line_end=line_end, **kwargs))

    def add_clef(self, clef):
        try:
            attributes = self.get_children_by_type(Attributes)[0]
        except IndexError:
            attributes = self.add_child(Attributes())
        clef_copy = clef.__deepcopy__()
        attributes.add_child(clef_copy)

    def add_dynamics(self, value, placement='below', **kwargs):
        dynamic_classes = [P, PP, PPP, PPPP, PPPPP, PPPPPP, F, FF, FFF, FFFF, FFFFF, FFFFFF, MP, MF, SF, SFP, SFPP, FP,
                           RF, RFZ, SFZ, SFFZ, FZ, N, PF, SFZP]

        tags = [d._TAG for d in dynamic_classes]
        try:
            index = tags.index(value)
        except ValueError:
            raise ValueError('wrong dynamics value')

        direction = self.add_child(Direction(placement=placement))
        direction_type = direction.add_child(DirectionType())
        dynamics = direction_type.add_child(Dynamics(**kwargs))

        dynamics.add_child(dynamic_classes[index]())

        return dynamics

    def add_fermata(self, value='normal', **kwargs):
        fermata = Fermata(value, **kwargs)
        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        notations.add_child(fermata)

    def add_flag(self, flag):
        if not isinstance(flag, TreeChordFlag1) and not isinstance(flag, TreeChordFlag2) \
                and not isinstance(flag, TreeChordFlag3):
            raise TypeError(
                'flag must be of type TreeChordFlag, TreeChordFlag2 or TreeChordFlag3 or TreeChordFlag4 not {}'.format(
                    flag.__class__))
        if self._flags is None:
            self._flags = set()
        self._flags.add(flag)

    def add_grace_chords(self, chords, mode='pre'):
        permitted = ['pre', 'post']
        if mode not in permitted:
            raise ValueError('mode must be in {}'.format(permitted))
        try:
            chords = list(chords)
        except TypeError:
            chords = [chords]

        for chord in chords:
            if not isinstance(chord, TreeChord):
                raise TypeError('wrong type {}'.format(type(chord)))
        for chord in chords:
            chord.quarter_duration = 0
            chord.zero_mode = 'grace'
            if mode == 'pre':
                self._pre_grace_chords.append(chord)
            else:
                self._post_grace_chords.append(chord)

    def add_harmonic(self, interval):
        if len(self.midis) != 1:
            raise Exception('harmonic can only be added to chords with one midi')
        self.add_midi(self.midis[0].value + interval)
        self.midis[-1].add_notehead('diamond', filled='no')

    def add_lyric(self, text, number=1, **kwargs):
        lyric = self.add_child(Lyric(number=str(number), **kwargs))
        lyric.add_child(Text(str(text)))
        return lyric

    def add_midi(self, val):
        if val == 0:
            raise ValueError('midi with value 0 can not be added.')

        if not isinstance(val, Midi):
            val = Midi(val)

        self._midis.append(val)

    def add_notations_object(self, object):
        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        notations.add_child(object)
        return object

    def add_slide(self, type, **kwargs):
        object = Slide(type, **kwargs)
        return self.add_notations_object(object)

    def add_slur_object(self, slur):
        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        notations.add_child(slur)
        return slur

    def add_slur(self, type, **kwargs):
        slur = Slur(type, **kwargs)
        return self.add_slur_object(slur)

    def add_technical_object(self, technical_object):

        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        try:
            technical = notations.get_children_by_type(Technical)[0]
        except IndexError:
            technical = notations.add_child(Technical())

        technical.add_child(technical_object)

    def add_tuplet(self, type, number=1):
        normals = {3: 2, 5: 4, 6: 4, 7: 4, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 8, 15: 8}
        types = {8: '32nd', 4: '16th', 2: 'eighth'}
        actual_notes = self.parent_beat.best_div
        normal_notes = normals[actual_notes]
        normal_type = types[normal_notes / self.parent_beat.duration]
        if type != 'continue':
            try:
                notations = self.notations
            except AttributeError:
                notations = self.add_child(Notations())

            v = self.get_children_by_type(Voice)[0]
            if int(v.value) % 2 == 0:
                placement = 'below'
            else:
                placement = 'above'

            notations.add_child(Tuplet(type=type, number=number, bracket='yes', placement=placement))

        tm = self.add_child(TimeModification())
        tm.add_child(ActualNotes(actual_notes))
        tm.add_child(NormalNotes(normal_notes))
        tm.add_child(NormalType(normal_type))

    def add_tremolo(self, number=3, **kwargs):

        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        try:
            ornaments = notations.get_children_by_type(Ornaments)[0]
        except IndexError:
            ornaments = notations.add_child(Ornaments())

        ornaments.add_child(Tremolo(number, **kwargs))

    def add_tie(self, value):
        if value not in ('stop', 'start'):
            raise NotImplementedError('value {} cannot be a tie value'.format(value))

        try:
            notations = self.get_children_by_type(Notations)[0]
        except IndexError:
            notations = self.add_child(Notations())

        if value == 'start' and 'start' not in self.tie_types:
            self.add_child(Tie('start'))
            notations.add_child(Tied('start', orientation=self.tie_orientation))

        elif value == 'stop' and 'stop' not in self.tie_types:
            self.add_child(Tie('stop'))
            notations.add_child(Tied('stop'))

    def add_wedge(self, value, placement='below', **kwargs):
        wedge_object = Wedge(value, **kwargs)

        direction = self.add_child(Direction(placement=placement))
        direction_type = direction.add_child(DirectionType())
        wedge = direction_type.add_child(wedge_object)
        #
        # dynamics.add_child(dynamic_classes[index]())

        return wedge

    def add_words(self, words, placement='above', **kwargs):
        d = self.add_child(Direction(placement=placement))
        dt = d.add_child(DirectionType())
        if isinstance(words, Words):
            if kwargs:
                raise ValueError('no keywords possible if add_words gets a Words()')
            dt.add_child(words)
        else:
            dt.add_child(Words(value=str(words), **kwargs))

    # get

    def get_articulations(self):
        output = []
        for notations in self.get_children_by_type(Notations):
            articulations = notations.get_children_by_type(Articulations)
            for articulation in articulations:
                output.extend(articulation.get_children())
        return output

    def get_clef(self):
        try:
            attributes = self.get_children_by_type(Attributes)[0]
            return attributes.get_children_by_type(TreeClef)[0]
        except IndexError:
            return None

    def get_dynamics(self):
        directions = self.get_children_by_type(Direction)
        for direction in directions:
            direction_types = direction.get_children_by_type(DirectionType)
            for direction_type in direction_types:
                for child in direction_type.get_children():
                    if isinstance(child, Dynamics):
                        return child.get_children()[0].to_string()[1:-3]
        return None

    def get_notes(self):
        return self.notes

    def get_pre_grace_chords(self):
        return self._pre_grace_chords

    def get_post_grace_chords(self):
        return self._post_grace_chords

    def get_words(self):
        output = []
        for dt in self._get_direction_types():
            for child in dt.get_children():
                if isinstance(child, Words):
                    output.append(child)
        return output

    # remove

    def remove_dynamics(self):
        for direction_type in self._get_direction_types():
            for child in direction_type.get_children():
                if isinstance(child, Dynamics):
                    direction_type.remove_child(child)
            if not direction_type.get_children():
                self._remove_direction_type(direction_type)

    def remove_flag(self, flag):
        if flag in self._flags:
            self._flags.remove(flag)

    def remove_from_score(self):
        if 'stop' in self.tie_types and 'start' not in self.tie_types:
            self.remove_tie('stop')
            previous_chord = self.previous_in_score_voice
            if previous_chord:
                previous_chord.remove_tie('start')

        elif 'start' in self.tie_types and 'stop' not in self.tie_types:
            self.remove_tie('start')
            next_chord = self.next_in_score
            if next_chord:
                next_chord.remove_tie('stop')

                for l in self.get_children_by_type(Lyric):
                    next_chord.add_child(l)
                for n in self.get_children_by_type(Notations):
                    next_chord.add_child(n)
                for d in self.get_children_by_type(Direction):
                    next_chord.add_child(d)
                clef = self.get_clef()
                if clef:
                    next_chord.add_clef(clef)

        self.parent_beat.chords.remove(self)
        self.parent_tree_part_voice.chords.remove(self)

    def remove_notations(self):
        notations = self.get_children_by_type(Notations)
        for notation in notations:
            self.remove_child(notation)

    def remove_previous_tie(self):
        if 'stop' in self.tie_types:
            self.remove_tie('stop')
            try:
                self.previous_in_score_part.remove_tie('start')
            except AttributeError:
                pass

    def remove_slur(self, type):
        try:
            notations = self.get_children_by_type(Notations)[0]
            slurs = [s for s in notations.get_children_by_type(Slur) if s.type == type]
            for slur in slurs:
                notations.remove_child(slur)
            if not notations.get_children():
                self.remove_child(notations)
        except IndexError:
            pass

    def remove_tie(self, type):
        if type in self.tie_types:
            notations = self.get_children_by_type(Notations)[0]
            tie = [t for t in self.get_children_by_type(Tie) if t.type == type][0]
            self.remove_child(tie)

            tied = [t for t in notations.get_children_by_type(Tied) if t.type == type][0]
            notations.remove_child(tied)
            if not notations.get_children():
                self.remove_child(notations)

    def remove_voice(self):
        for voice in self.get_children_by_type(Voice):
            self.remove_child(voice)

    # set

    def set_manual_type(self, val, **kwargs):
        try:
            chord_type = self.get_children_by_type(Type)[0]
            self.remove_child(chord_type)
        except IndexError:
            self.add_child(Type(value=val, **kwargs))

        self._manual_type = True

    def set_manual_dots(self, val):
        try:
            for dot in self.get_children_by_type(Dot):
                self.remove_child(dot)
        except IndexError:
            pass
        for i in range(val):
            self.add_child(Dot())

        self._manual_dots = True

    def set_staff_number(self, staff_number):
        self.manual_staff_number = staff_number

    def set_tie_orientation(self, orientation):
        if self.is_tied_to_next:
            tied = [t for t in self.get_children_by_type(Notations)[0].get_children_by_type(Tied) if t.type == 'start']
            for t in tied:
                t.orientation = orientation

    def set_voice_number(self, voice_number):
        self.manual_voice_number = voice_number

    # update

    def update_dot(self):
        if self._manual_dots is False:
            _dot = 0

            if self.quarter_duration.numerator % 3 == 0:
                _dot = 1
            elif self.quarter_duration == Fraction(1, 2) and self.parent_beat.best_div == 6:
                _dot = 1
            elif self.quarter_duration == Fraction(1, 4) and self.parent_beat.best_div == 6:
                _dot = 1
            elif (self.quarter_duration == Fraction(3, 9) or self.quarter_duration == Fraction(6,
                                                                                               9)) and self.parent_beat.best_div == 9:
                _dot = 1
            elif self.quarter_duration == Fraction(7, 8):
                _dot = 2
            elif self.quarter_duration == Fraction(7, 4):
                _dot = 2
            else:
                _dot = 0

            for dot in self.get_children_by_type(Dot):
                self.remove_child(dot)

            for i in range(_dot):
                self.add_child(Dot())

    def update_type(self):
        """get type of a Note() depending on its quantized duration and return it [whole, half, quarter, eighth, 16th,
        32nd, 64th]"""
        _types = {(1, 12): '32nd',
                  (1, 11): '32nd',
                  (2, 11): '16th',
                  (3, 11): '16th',
                  (4, 11): 'eighth',
                  (6, 11): 'eighth',
                  (8, 11): 'quarter',
                  (1, 10): '32nd',
                  (3, 10): '16th',
                  (1, 9): '32nd',
                  (2, 9): '16th',
                  (4, 9): 'eighth',
                  (8, 9): 'quarter',
                  (1, 8): '32nd',
                  (3, 8): '16th',
                  (7, 8): 'eighth',
                  (1, 7): '16th',
                  (2, 7): 'eighth',
                  (3, 7): 'eighth',
                  (4, 7): 'quarter',
                  (6, 7): 'quarter',
                  (1, 6): '16th',
                  (1, 5): '16th',
                  (2, 5): 'eighth',
                  (3, 5): 'eighth',
                  (4, 5): 'quarter',
                  (1, 4): '16th',
                  (2, 4): 'eighth',
                  (3, 4): 'eighth',
                  (7, 4): 'quarter',
                  (1, 3): 'eighth',
                  (2, 3): 'quarter',
                  (3, 2): 'quarter',
                  (1, 2): 'eighth',
                  (1, 1): 'quarter',
                  (2, 1): 'half',
                  (3, 1): 'half',
                  (4, 1): 'whole',
                  (6, 1): 'whole',
                  (8, 1): 'breve',
                  (12, 1): 'breve'
                  }

        if self._manual_type is False:
            tremoli_types = [tremolo.type for tremolo in self.tremoli]

            if self.quarter_duration == 0:
                value = 'eighth'

            elif ('start' in tremoli_types or 'stop' in tremoli_types):
                show_duration = self.quarter_duration * 2
                value = _types[(show_duration.numerator, show_duration.denominator)]
                if not self.get_children_by_type(TimeModification):
                    tm = TimeModification()
                    tm.add_child(ActualNotes(2))
                    tm.add_child(NormalNotes(1))
                    self.add_child(tm)
            else:
                value = _types[(self.quarter_duration.numerator, self.quarter_duration.denominator)]

            try:
                chord_type = self.get_children_by_type(Type)[0]
                chord_type.value = value
            except IndexError:
                self.add_child(Type(value))

    # others

    def change_range(self, min_midi, max_midi, microtone=2):
        if self.is_rest:
            pass
        else:
            scale = Scale(self.midis[0].value, self.midis[-1].value, min_midi, max_midi, step=2 / microtone)
            self.midis = [scale(midi.value) for midi in self.midis]

    def force_tie(self):
        self.is_adjoinable = False

    def has_same_pitches(self, other_chord):
        if len(self.notes) == len(other_chord.notes):
            for note_1, note_2 in zip(self.notes, other_chord.notes):
                if isinstance(note_1.event, Rest) or isinstance(note_2.event, Rest):
                    return False
                pitch_1 = note_1.pitch.dump()
                pitch_2 = note_2.pitch.dump()
                if len(pitch_1) == len(pitch_2):
                    for i in range(1, len(pitch_1)):
                        if pitch_1[i].value != pitch_2[i].value:
                            return False
                    return True
        return False

    def inverse(self):
        intervals = xToD([midi.value for midi in self.midis])
        intervals = [-interval for interval in intervals]
        self.midis = dToX(intervals, first_element=self.midis[0].value)

    def split(self, *ratios):
        if len(ratios) == 1:
            ratios = ratios[0]

        new_ratios = [Fraction(Fraction(ratio), Fraction(sum(ratios))) for ratio in ratios]

        old_duration = self.quarter_duration

        self.quarter_duration *= new_ratios[0]

        new_chords = [self.split_copy(quarter_duration=ratio * old_duration) for ratio in new_ratios[1:]]
        for ch in new_chords:
            ch.tie_orientation = self.tie_orientation

        if 'start' in self.tie_types:
            new_chords[-1].add_tie('start')

        if not self.is_adjoinable:
            self.is_adjoinable = True
            new_chords[-1].is_adjoinable = False

        for tremolo in self.tremoli:
            new_chords[-1].add_tremolo(number=tremolo.value)

        new_chords.insert(0, self)

        if self.midis[0].value != 0:
            for new_chord in new_chords[1:]:
                new_chord.add_tie('stop')

            for new_chord in new_chords[:-1]:
                new_chord.add_tie('start')

        return new_chords

    def to_rest(self):
        self.midis = [0]
        self.remove_tie('stop')
        self.remove_tie('start')
        for notation in self.get_children_by_type(Notations):
            articulations = notation.get_children_by_type(Articulations)
            for articulation in articulations:
                notation.remove_child(articulation)

    def transpose(self, interval):
        for midi in self.midis:
            if midi.value != 0:
                midi.value += interval

    def untie(self):
        if 'start' in self.tie_types:
            self.remove_tie('start')
            try:
                self.next.remove_tie('stop')
            except AttributeError:
                pass

    # //copy

    def copy_tremolo_flag(self):
        new_chord = TreeChord()
        new_chord.midis = self.midis
        return new_chord

    def split_copy(self, quarter_duration):
        new_chord = TreeChord(quarter_duration=quarter_duration)

        new_chord.midis = self.midis
        new_chord.parent_tree_part_voice = self.parent_tree_part_voice
        new_chord.parent_beat = self.parent_beat

        if self._flags is not None:
            new_chord._flags = []
            for flag in self._flags:
                new_chord._flags.append(flag.__deepcopy__())

        new_chord._offset = None
        new_chord.is_finger_tremolo = self.is_finger_tremolo
        for grace_chord in self.get_post_grace_chords():
            new_chord.add_grace_chords(grace_chord.__deepcopy__(), mode='post')

        try:
            voice = self.get_children_by_type(Voice)[0]
            new_chord.add_child(voice)
        except IndexError:
            pass

        try:
            staff = self.get_children_by_type(StaffElement)[0]
            new_chord.add_child(staff)
        except IndexError:
            pass

        try:
            notehead = self.get_children_by_type(Notehead)[0]
            new_chord.add_child(notehead)
        except IndexError:
            pass

        return new_chord

    def deepcopy_for_SimpleFormat(self):
        new_chord = TreeChord(quarter_duration=self.quarter_duration, zero_mode=self.zero_mode)
        new_chord.midis = [midi.__deepcopy__() for midi in self.midis]
        for child in self.get_children():
            if not isinstance(child, Voice):
                new_chord.add_child(child)
        for grace_chord in self.get_pre_grace_chords():
            new_chord.add_grace_chords(grace_chord.deepcopy_for_SimpleFormat())
        for grace_chord in self.get_post_grace_chords():
            new_chord.add_grace_chords(grace_chord.deepcopy_for_SimpleFormat().__deepcopy__(), 'post')
        return new_chord

    def __deepcopy__(self, memodict={}):
        new_chord = TreeChord(quarter_duration=self.quarter_duration, zero_mode=self.zero_mode)
        new_chord.midis = [midi.__deepcopy__() for midi in self.midis]
        for child in self.get_children():
            if isinstance(child, Notations):
                copied_notations = Notations()
                for grand_child in child.get_children():
                    copied_notations.add_child(grand_child)
                new_chord.add_child(copied_notations)
            else:
                new_chord.add_child(child)

        new_chord.is_adjoinable = self.is_adjoinable
        if self._flags:
            new_chord._flags = []
            for flag in self._flags:
                new_chord._flags.append(flag.__deepcopy__())

        new_chord._flags = self._flags
        new_chord._manual_type = self._manual_type
        new_chord._manual_staff_number = self._manual_staff_number
        new_chord.tie_orientation = self.tie_orientation

        for grace_chord in self.get_pre_grace_chords():
            new_chord.add_grace_chords(grace_chord.__deepcopy__())

        for grace_chord in self.get_post_grace_chords():
            new_chord.add_grace_chords(grace_chord.__deepcopy__(), 'post')
        return new_chord
