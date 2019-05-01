from musicscore import basic_functions
from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.tree.tree import Tree
from quicktions import Fraction
from musicscore.permutation.permutation import permute, self_permute
import copy

from musicscore.fractaltree.midigenerators import RelativeMidi, MidiGenerator


class FractalTree(Tree):
    def __init__(self, value=None, proportions=None, tree_permutation_order=None, multi=None, fertile=True,
                 first_position=None, *args, **kwargs):
        Tree.__init__(self, *args, **kwargs)
        self._value = None
        self._proportions = None
        self._tree_permutation_order = None
        self._multi = None
        self._permutation_order = None
        self._first_position = None
        self._position_in_tree = None
        self._fractal_order = None
        self._name = None

        self.value = value
        self.multi = multi
        self.tree_permutation_order = tree_permutation_order
        self.proportions = proportions
        self.first_position = first_position

        self.fertile = fertile

    def calculate_position_in_tree(self):
        parent = self.up
        if self.is_root:
            return 0
        else:
            index = parent.children.index(self)
            if index == 0:
                return parent.position_in_tree
            else:
                return parent.children[index - 1].position_in_tree + parent.children[index - 1].value

    def add_self(self):
        leaves = self.get_leaves()
        for leaf in leaves:
            new_node = self.copy()
            new_node._up = self
            new_node._fractal_order = self.fractal_order
            leaf.add_child(new_node)

    @property
    def position_in_tree(self):
        if self._position_in_tree is None:
            self._position_in_tree = self.calculate_position_in_tree()

        return self._position_in_tree

    @property
    def number_of_layers(self):
        if len(self.get_leaves()) == 1:
            return 0
        else:
            return self.get_farthest_leaf().get_distance() + 1

    @property
    def name(self):
        if self._name is None:
            if self.is_root:
                self._name = '0'
            elif self.up.is_root():
                self._name = str(self.up.children.index(self) + 1)
            else:
                self._name = self.up.name + '.' + str(self.up.children.index(self) + 1)
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is None:
            self._value = 10
        else:
            self._value = val

    @property
    def first_position(self):
        if self._first_position is None:
            self._first_position = 0
        return self._first_position

    @first_position.setter
    def first_position(self, value):
        self._first_position = value

    @property
    def position(self):
        if self.is_root():
            return self.first_position
        else:
            siblings = self.up.children
            index = siblings.index(self)
            previous_siblings = siblings[:index]
            position_in_parent = 0
            for child in previous_siblings: position_in_parent += child.value
            return position_in_parent + self.up.position

    @property
    def proportions(self):
        if self._proportions is None:
            self._proportions = [1, 1]
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if values:
            self._proportions = [Fraction(Fraction(value) / Fraction(sum(values))) for value in values]

    @property
    def tree_permutation_order(self):
        return self._tree_permutation_order

    @tree_permutation_order.setter
    def tree_permutation_order(self, values):
        self._tree_permutation_order = values

    @property
    def multi(self):
        m_1 = self._multi[0]
        m_2 = self._multi[1]
        m_1, m_2 = ((m_1 - 1) % len(self.proportions)) + 1, ((m_2 - 1) % len(self.proportions)) + 1
        self._multi = (m_1, m_2)
        return self._multi

    @multi.setter
    def multi(self, values):
        if values is None:
            self._multi = (1, 1)
        elif not isinstance(values, tuple) or len(values) != 2:
            raise TypeError('multi has to be a tuple with a length of 2')
        else:
            self._multi = values

    @property
    def children_fractal_values(self):
        return self._calculate_children_fractal_values()

    @property
    def children_fractal_orders(self):
        return self._calculate_children_fractal_orders()

    # @property
    # def distance(self):
    #     return int(self.get_distance(self.get_root, topology_only=True))

    @property
    def permutation_order(self):
        def _calculate_permutation_order():
            if self.tree_permutation_order:
                self_permuted_order = self_permute(self.tree_permutation_order)
                multiplied_order = [permute(self_permuted_order, current_order) for current_order in
                                    self_permuted_order]

                def reordered():
                    index_of_first_row = None
                    for index_of_first_row in range(len(multiplied_order)):
                        if multiplied_order[index_of_first_row][0] == self.tree_permutation_order:
                            break
                    output = []
                    for i in range(index_of_first_row, index_of_first_row + len(multiplied_order)):
                        output.append(multiplied_order[i % len(multiplied_order)])
                    return output

                multiplied_order = reordered()
                return multiplied_order[self.multi[0] - 1][self.multi[1] - 1]
            else:
                return range(1, len(self.proportions) + 1)

        if self._permutation_order is None:
            self._permutation_order = _calculate_permutation_order()
        return self._permutation_order

    @property
    def fractal_order(self):
        if self._fractal_order is None:
            if self.is_root():
                self._fractal_order = None
            else:
                index = self.up.children.index(self)
                self._fractal_order = self.up.children_fractal_orders[index]
        return self._fractal_order

    def _calculate_children_fractal_values(self):
        if self.value and self.proportions:
            children_fractal_values = [self.value * prop for prop in self.proportions]
            if self.permutation_order:
                try:
                    children_fractal_values = permute(children_fractal_values, self.permutation_order)
                except ValueError:
                    raise ValueError('proportions and tree_permutation_order should have the same length')
            return children_fractal_values

    def _calculate_children_fractal_orders(self):
        if self.value and self.proportions:
            children_fractal_orders = range(1, len(self.proportions) + 1)
            if self.permutation_order:
                children_fractal_orders = permute(children_fractal_orders, self.permutation_order)
            return children_fractal_orders

    def _child_multi(self, parent, index):
        number_of_children = len(self.proportions)
        multi_first = sum(parent.multi) % number_of_children
        if multi_first == 0:
            multi_first = number_of_children
        ch_multi = (multi_first, index + 1)
        return ch_multi

    def add_layer(self, *conditions):
        leaves = list(self.traverse_leaves())
        if not leaves:
            leaves = [self]

        if conditions:
            for leaf in leaves:
                for condition in conditions:
                    if not condition(leaf):
                        leaf.fertile = False
                        break

        for leaf in leaves:
            if leaf.fertile is True:
                for i in range(len(leaf.proportions)):
                    new_node = leaf.copy()
                    new_node.value = leaf.children_fractal_values[i]
                    new_node.multi = self._child_multi(leaf, i)

                    leaf.add_child(new_node)
            else:
                pass

    def get_layer(self, layer=0, key=None):

        if layer <= self.get_root().number_of_layers:

            branch_distances = []
            for child in self.get_children():
                branch_distances.append(child.get_farthest_leaf().get_distance() + 1)

            if layer == 0:
                if key:
                    return getattr(self, key)
                else:
                    return self

            if layer >= 1:
                if layer > max(branch_distances):
                    self.get_layer(layer=layer - 1, key=key)

                output = []
                for i in range(len(self.get_children())):
                    child = self.get_children()[i]
                    if branch_distances[i] == 1:
                        if key:
                            output.append(getattr(child, key))
                        else:
                            output.append(child)
                    else:
                        output.append(child.get_layer(layer - 1, key))

                return output
        else:
            err = 'max layer number=' + str(self.number_of_layers)
            raise ValueError(err)

    @property
    def next(self):
        if not self.is_leaf():
            raise Exception('FractalTree().next property can only be used for leaves')
        else:
            try:

                parent = self.up
                while parent is not None:
                    parent_leaves = list(parent.traverse_leaves())
                    index = parent_leaves.index(self)
                    try:
                        return parent_leaves[index + 1]
                    except IndexError:
                        parent = parent.up
                raise IndexError()
            except IndexError:
                return None

    @property
    def previous(self):
        if not self.is_leaf():
            raise Exception('FractalTree().previous property can only be used for leaves')
        else:
            try:
                parent = self.up
                while parent is not None:
                    parent_leaves = list(parent.traverse_leaves())
                    index = parent_leaves.index(self)
                    try:
                        if index - 1 < 0:
                            raise Exception()
                        else:
                            return parent_leaves[index - 1]
                    except IndexError:
                        parent = parent.up
                raise IndexError()
            except IndexError:
                return None

    def split(self, proportions):

        for prop in proportions:
            self.add_self()
            self.get_children()[-1].value = self.value * prop / sum(proportions)

    def copy(self):
        return self.__class__(value=self.value, proportions=self.proportions,
                              tree_permutation_order=self.tree_permutation_order, fertile=self.fertile)


class FractalMusic(FractalTree):

    def __init__(self, midi_generator=None, duration=None, *args, **kwargs):
        super(FractalMusic, self).__init__(*args, **kwargs)
        self._midi_value = None
        self._chord = None
        self._tempo = None
        self._midi_generator = None
        self._children_generated_midis = None

        self.value = duration
        self.tempo = 60
        self.midi_generator = midi_generator

    @property
    def tempo(self):
        return self.get_root()._tempo

    @tempo.setter
    def tempo(self, value):
        self.get_root()._tempo = value

    @property
    def duration(self):
        return self.value

    @duration.setter
    def duration(self, value):
        self._value = value

    @property
    def midi_generator(self):
        if self._midi_generator is None:
            try:
                self._midi_generator = RelativeMidi(midi_range=[71, 71], proportions=self.children_fractal_values,
                                                    directions=[1, -1])
            except AttributeError:
                raise Exception('midi_generator is None and cannot be set:')

        if isinstance(self._midi_generator, RelativeMidi):
            if self._midi_generator.midi_range is None:
                if self.is_root():
                    self._midi_generator.midi_range = [71]
                self._midi_generator.midi_range = self.auto_midi_range

        return self._midi_generator

    @midi_generator.setter
    def midi_generator(self, value):
        if value is not None:
            if not (isinstance(value, MidiGenerator)):
                err = 'midi_generator can only be an instance of subclasses of MidiGenerator or None. None=RelativeMidi(midi_range=self.midi_range, proportions=permute(self.fractal_proportions, self.fractal.permutation_order)'
                raise TypeError(err)

        self._midi_generator = value

    @property
    def _midi_iterator(self):
        return self.midi_generator.iterator

    @_midi_iterator.setter
    def _midi_iterator(self, value):
        raise AttributeError('_midi_iterator cannot be set directly. Use midi-generator!')

    @property
    def children_generated_midis(self):
        if self._children_generated_midis is None:
            self._children_generated_midis = []
            for i in range(len(self.proportions) + 1):
                self._children_generated_midis.append(self._midi_iterator.next())

        return self._children_generated_midis

    @property
    def _children_midis(self):
        return [child.midi_value for child in self.get_children()]

    @property
    def midi_value(self):
        if self._midi_value is None:
            if self.is_root():
                self._midi_value = 71
            else:
                self._midi_value = self.up.children_generated_midis[self.up.children.index(self)]
        return self._midi_value

    @midi_value.setter
    def midi_value(self, value):
        if value is not None:
            if isinstance(value, int) or isinstance(value, float):
                if value >= 18:
                    self._midi_value = value
                else:
                    raise ValueError('midi cannot be smaller than 18')
            else:
                raise TypeError('midi can only be int, float or None')
        else:
            self._midi_value = value

    @property
    def auto_midi_range(self):
        if self.is_root():
            raise AttributeError('root has no auto_midi_range')

        parent_midis = self.up._children_midis
        parent_midis.append(self.up.children_generated_midis[-1])
        self_index = self.up.children.index(self)
        return parent_midis[self_index:self_index + 2]

    def get_chord(self, ambitus_factor=1, microtone=2, proportions=None):
        if proportions is None:
            proportions = self.proportions
        fractal_tree = FractalTree(value=self.duration, proportions=proportions,
                                   tree_permutation_order=self.tree_permutation_order, multi=self.multi)
        ambitus = abs(self.midi_range[1] - self.midi_range[0]) * ambitus_factor
        chord_intervals = [float(value) * ambitus / sum(self.children_fractal_values) for value in
                           self.children_fractal_values]
        chord_midis = [(value + self.midi_value) for value in [0] + basic_functions.step_sums(chord_intervals)][:-1]
        factor = microtone / 2.0
        chord_midis = map(lambda midi: round(midi * factor) / factor, chord_midis)
        return Note(duration=self.duration, event=Chord(chord_midis))

    @property
    def midi_range(self):
        return self.midi_generator.midi_range

    @property
    def note(self):
        tempo_factor = Fraction(self.tempo, 60)
        if self._chord is None:  # or self._note.midis!=[self.midi] or self._note.duration!=self.duration:
            self._chord = Note(duration=self.duration * tempo_factor, event=Chord(self.midi_value))

        return self._chord

    def copy(self):
        copied_midi_generator = self.midi_generator.copy()
        copied = self.__class__(duration=self.duration, proportions=self.proportions,
                                tree_permutation_order=self.tree_permutation_order, fertile=self.fertile,
                                midi_generator=copied_midi_generator)
        if self.fertile is False:
            try:
                copied.midi_value = self.midi_value
            except:
                copied.midi_value = None
        return copied

    def get_chords(self, layer=1):
        if layer < 1:
            layer = 1
        try:
            return self.get_layer(layer=layer)
        except ValueError:
            for i in range(layer - self.number_of_layers):
                self.add_layer()

        midis = self.get_layer(self.number_of_layers, key='midi')
        durations = self.get_layer(self.number_of_layers - 1, key='duration')

        simple_format = SimpleFormat(durations=ml.flatten(durations), midis=ml.one_dimensional(midis))
        return simple_format

    def split(self, proportions):
        for prop in proportions:
            duration = self.duration * float(prop) / sum(proportions)
            note = Note(duration=duration, event=copy.deepcopy(self.note.event))
            note.additionals = self.note.additionals
            # print 'duration', duration

            self.add_child()
            self.get_children()[-1].duration = duration
            self.get_children()[-1]._note = note
            # self.children[-1].name=self.name+'.'+str(index+1)
            self.get_children()[-1]._fractal_order = self.fractal_order

        return self.get_children()

    def add_notes(self, notes):
        if self.is_leaf is False:
            raise Exception('notes can only be added to leaf')
        else:
            notes = copy.deepcopy(notes)
            remaining_time = self.duration

            for note in notes:
                if remaining_time <= 0:
                    break
                else:
                    if note.duration > remaining_time:
                        note.duration = remaining_time

                    child = self.add_child()
                    child.duration = note.duration
                    child._note = note
                    remaining_time -= note.duration
            if remaining_time > 0:
                child = self.add_child()
                child.duration = remaining_time
                child._note = Note(duration=remaining_time, event=Rest())

    def add_field(self, field):
        field.duration = self.duration
        notes = list(field)
        self.add_notes(notes)

    def split_rest(self, offset=None):
        if not self.is_leaf():
            raise Exception('FractalMusic.split_rest can only be used on leaves')
        else:
            if self.note.duration > 0.5:

                if offset is None:
                    offset = self.position_in_tree - int(self.position_in_tree)
                else:
                    print('split_rest.offset:', self.name, offset)

                duration = 1 - offset
                if offset % 1. == 0: duration = 0.5
                first_note = copy.deepcopy(self.note)
                first_note.duration = duration
                self.add_notes([first_note])

    @property
    def simple_format(self):
        simple_format = SimpleFormat()
        for note_node in self.get_leaves():
            simple_format.add_note(note_node.note)
        return simple_format
