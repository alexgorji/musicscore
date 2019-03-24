from musicscore.basic_functions import roundrobin, flatten
from musicscore.tree.tree import Tree
import copy
import warnings


class DTDError(Exception):
    def __init__(self, msg='DTD Error'):
        super().__init__(msg)


class ChildTypeDTDConflict(DTDError):
    def __init__(self, child):
        msg = 'child of type {} cannot be added due to DTD Type conflicts'.format(type(child))
        super().__init__(msg)


class ChildOccurrenceDTDConflict(DTDError):
    def __init__(self, child):
        msg = 'child of type {} cannot be added due to DTD Occurrence conflicts'.format(type(child))
        super().__init__(msg)


class ChildIsNotOptional(DTDError):
    def __init__(self, node, xmltree):
        msg = 'child of type {} is due to DTD Occurrence not optional for {}'.format(node.type_.__name__,
                                                                                     type(xmltree).__name__)
        super().__init__(msg)


class DTDConflict(DTDError):
    def __init__(self):
        msg = 'DTD conflicts exist'
        super().__init__(msg)


class DTDTree(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DTDNode(DTDTree):
    def __init__(self, children=[], min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(**kwargs)
        self._expanded = None
        self._min_occurrence = None
        self._max_occurrence = None
        self.min_occurrence = min_occurrence
        self.max_occurrence = max_occurrence
        self._possibility_index = 0
        for child in children:
            if not isinstance(child, DTDTree):
                raise TypeError(
                    '{} can only have children of Type DTDTree not {}'.format(self.__class__.__name__, type(child)))
            self.add_child(child)

    @property
    def min_occurrence(self):
        return self._min_occurrence

    @min_occurrence.setter
    def min_occurrence(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('min_occurrence.value must be of type None or positive int not {}'.format(type(value)))
        if value is not None and value < 0:
            raise ValueError('min_occurrence.value must be positive'.format(type(value)))
        self._min_occurrence = value

    @property
    def max_occurrence(self):
        return self._max_occurrence

    @max_occurrence.setter
    def max_occurrence(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError('max_occurrence.value must be of type None or positive int not {}'.format(type(value)))
        if value is not None and value < 0:
            raise ValueError('max_occurrence.value must be positive'.format(type(value)))
        self._max_occurrence = value

    def __repr__(self):
        if isinstance(self, Element):
            return '{} type {} at {}'.format(self.__class__.__name__, self.type_.__name__, hex(id(self)))
        return '{} at {}'.format(self.__class__.__name__, hex(id(self)))

    def expand(self):
        return self

    @property
    def expanded(self):
        if self._expanded is None:
            self._expanded = self.expand()
            # self.repair_occurrences()
        return self._expanded

    @property
    def choices(self):
        output = []
        for ex in self.expanded:
            new_tree = self.__deepcopy__()
            for leaf in ex:
                new_tree.goto(leaf.index).trim = True

            for leaf in new_tree.traverse_leaves():
                try:
                    if leaf.trim:
                        branch = leaf.get_branch()
                        for index, node in enumerate(branch):
                            if isinstance(node, Choice):
                                if node.is_root:
                                    branch[index + 1]._up = None
                                    new_tree = branch[index + 1]
                                else:
                                    node.replace_node(branch[index + 1])
                except AttributeError:
                    pass

            output.append(new_tree)
        # for choice in output:
        #     print(choice)
        return output


    def next(self):
        try:
            self._possibility_index += 1
            return self.expanded[self._possibility_index]
        except IndexError:
            raise StopIteration()

    def get_current_combination(self):
        return self.expanded[self._possibility_index]

    def type_in_combination(self, ch):
        for index, t in enumerate([node.type_ for node in self.get_current_combination()]):
            if isinstance(ch, t):
                return [True, index]
        return [False, None]

    def check_dtd_type(self, child):
        for dtd_child in self.get_children():
            if isinstance(child, dtd_child.type_):
                return True
        return False

    def reduce_group_references(self):
        for node in self.traverse():
            if isinstance(node, GroupReference) and len(node.get_children()) == 1 and isinstance(node.get_children()[0],
                                                                                                 Sequence) and len(
                node.get_children()[0].get_children()) == 1 and isinstance(node.get_children()[0].get_children()[0],
                                                                           Element):

                el = node.get_children()[0].get_children()[0]
                new_parent = el.up.up.up
                el._up = new_parent
                new_parent._children = [el if child == node else child for child in new_parent.get_children()]

    def dtd_filter_children(self, xmltree):
        filtered_children = [child for child in xmltree.get_children() if self.check_dtd_type(child)]
        return filtered_children

    def non_element_dtd_children(self):
        for dtd_child in self.get_children():
            if not isinstance(dtd_child, Element):
                return True
        return False

    def get_current_node(self, child):
        index = self.type_in_combination(child)[1]
        if index is None:
            raise IndexError()
        else:
            return self.get_current_combination()[index]

    def check_max_occurrence(self, occurrence):
        if isinstance(self.up, Choice) and self.up.min_occurrence == 0 and self.up.max_occurrence is None:
            return True
        # todo: max_occurrence of group must be unified (check siblings appearances)
        if isinstance(self.up, Sequence) and not (self.up.max_occurrence == 1):
            self.max_occurence = self.up.max_occurrence

        if self.max_occurrence is not None and occurrence > self.max_occurrence:
            return False

        return True

    def check_child_type(self, parent, child):

        while not self.type_in_combination(child)[0]:
            try:
                self.next()
                for sibling in parent.get_children():
                    try:
                        self.check_child_type(parent, sibling)
                    except ChildTypeDTDConflict:
                        raise ChildTypeDTDConflict(child)
            except StopIteration:
                raise ChildTypeDTDConflict(child)

    def check_child_max_occurrence(self, xmltree, child):
        occurrence = len(xmltree.get_children_by_type(type(child)))
        try:
            dtd_node = self.get_current_node(child)
        except IndexError:
            raise ChildOccurrenceDTDConflict(child)

        while dtd_node.check_max_occurrence(occurrence + 1) is False:
            try:
                self.next()
                for sibling in xmltree.get_children():
                    try:
                        self.check_child_max_occurrence(xmltree, sibling)
                    except ChildOccurrenceDTDConflict:
                        raise ChildOccurrenceDTDConflict(child)
            except StopIteration:
                raise ChildOccurrenceDTDConflict(child)
            dtd_node = self.get_current_node(child)

    def check_children(self, xmltree):
        children = xmltree.get_children()
        xmltree._children = []
        for child in children:
            self.check_child_type(xmltree, child)
            self.check_child_max_occurrence(xmltree, child)
            xmltree._children.append(child)

    def check_non_optional(self, xmltree):
        current_combination = self.get_current_combination()
        for node in current_combination:
            if isinstance(node.up, Choice) and node.up.min_occurrence == 0 and node.up.max_occurrence is None:
                pass
            elif isinstance(node.up, Sequence) and node.up.min_occurrence == 0:
                pass
            elif isinstance(node.up, Sequence) and node.up.min_occurrence != 1:
                raise NotImplementedError('node.up.min_occurrence={}'.format(node.up.min_occurrence))
            else:
                selected = xmltree.get_children_by_type(node.type_)
                if len(selected) == 0 and node.min_occurrence != 0:
                    raise ChildIsNotOptional(node, xmltree)

    def close(self, xmltree):
        try:
            self.check_non_optional(xmltree)
        except ChildIsNotOptional as e:
            try:
                self.next()
                self.check_children(xmltree)
                self.close(xmltree)
            except StopIteration:
                raise e

        xmltree.sort_children()

    def repair_occurrences(self):
        for node in self.traverse():
            if node.min_occurrence != 1:
                for child in node.get_children():
                    child.min_occurrence = node.min_occurrence

            if node.max_occurrence != 1:
                for child in node.get_children():
                    child.max_occurrence = node.max_occurrence
        # for branch in [leaf.get_branch() for leaf in self.traverse_leaves()]:
        #     for node in branch:
        #         if node.min_occurrence != 1:
        #             for child in node.get_children():
        #                 child.min_occurrence = node.min_occurrence
        #
        #         if node.max_occurrence != 1:
        #             for child in node.get_children():
        #                 child.max_occurrence = node.max_occurrence


class DTDLeaf(DTDNode):
    def __init__(self, type_, min_occurrence=1, max_occurrence=1, *args, **kwargs):
        super().__init__(min_occurrence=min_occurrence, max_occurrence=max_occurrence, *args, **kwargs)
        self._type = None
        self.type_ = type_

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, value):
        if not isinstance(value, type):
            raise TypeError('type_.value must be of type type not{}'.format(type(value)))
        self._type = value

    def add_child(self, child):
        raise Exception('DTDLeaf can have no children')


class Choice(DTDNode):
    """"""

    def __init__(self, *children, min_occurrence=1, max_occurrence=1):
        super().__init__(children=children, min_occurrence=min_occurrence, max_occurrence=max_occurrence)

    def expand(self):
        if (self.min_occurrence, self.max_occurrence) == (1, 1):
            if not self.get_children():
                output = []
            else:
                x = self.get_children()[0]
                xs = self.get_children()[1:]
                ex = x.expand()
                exs = Choice(*xs, min_occurrence=self.min_occurrence, max_occurrence=self.max_occurrence).expand()
                output = ex + exs

        elif (self.min_occurrence, self.max_occurrence) == (0, None):
            if not self.get_children():
                output = [[]]
            else:
                x = self.get_children()[0]
                xs = self.get_children()[1:]
                ex = x.expand()
                exs = Choice(*xs, min_occurrence=self.min_occurrence, max_occurrence=self.max_occurrence).expand()
                output = [a + b for a in ex for b in exs]
        else:
            raise ValueError(
                'Choice with min_occurrence {} and max_occurrence {} is not valid'.format(self.min_occurrence,
                                                                                          self.max_occurrence))
        self.repair_parenthood()
        # self.repair_occurrences()
        return output

    def sort_children(self, xmltree):
        # print('sorting {} with children {}'.format(self, self.get_children()))
        # print()
        if self.min_occurrence == 0 and self.max_occurrence is None:

            def find_current_dtd_child(child):
                current_combination = xmltree.dtd.get_current_combination()
                for dtd_child in current_combination:
                    if isinstance(child, dtd_child.type_):
                        return dtd_child

            if not self.non_element_dtd_children():
                for child in self.dtd_filter_children(xmltree):
                    if child not in xmltree._sorted_children:
                        xmltree._sorted_children.append(child)
            else:
                # todo if children are Groups with only ONE Element

                warnings.warn(
                    '{} {} sort still not possible for Choice with min_occurrence 0 and max_occurrence None if non Element DTDChild exists'.format(
                        self, self.get_leaves()))



        elif self.min_occurrence == 1 and self.max_occurrence == 1:

            def get_current_child():
                current_branches = [node.get_branch() for node in xmltree.dtd.get_current_combination()]
                for ch in self.get_children():
                    for branch in current_branches:
                        if ch in branch:
                            return ch

            current_child = get_current_child()
            if current_child:
                current_child.sort_children(xmltree)
            else:
                pass
        else:
            raise DTDError()


class Sequence(DTDNode):
    """"""

    def __init__(self, *children, min_occurrence=1, max_occurrence=1):
        super().__init__(children=children, min_occurrence=min_occurrence, max_occurrence=max_occurrence)

    def expand(self):

        if not self.get_children():
            output = [[]]
        else:
            x = self.get_children()[0]
            xs = self.get_children()[1:]
            ex = x.expand()
            exs = Sequence(*xs, min_occurrence=self.min_occurrence, max_occurrence=self.max_occurrence).expand()
            output = [a + b for a in ex for b in exs]
        self.repair_parenthood()
        # self.repair_occurrences()
        return output

    def sort_children(self, xmltree):
        # print('sorting {} with children {}'.format(self, self.get_children()))
        # print()

        # if all dtd_children are Elements. Sequence can have max_occurrence larger than 1
        if not self.non_element_dtd_children():
            list_of_children = [xmltree.get_children_by_type(child.type_) for child in self.get_children()]
            if self.max_occurrence is None or self.max_occurrence > 1:
                sorted_children = list(roundrobin(*list_of_children))
                xmltree._sorted_children.extend(sorted_children)
            else:
                xmltree._sorted_children.extend(flatten(list_of_children))

        # for mixed children of Sequence.  max_occurrence larger than 1 is not allowed!
        else:
            if self.max_occurrence is None or self.max_occurrence > 1:
                raise DTDError('sorting of Sequence is still not possible if max_occurrence is larger than 1 and non '
                               'Element children exist')
            for dtd_child in self.get_children():
                dtd_child.sort_children(xmltree)


class Element(DTDLeaf):
    """"""

    def __init__(self, type_, min_occurrence=1, max_occurrence=1, **kwargs):
        super().__init__(type_, min_occurrence=min_occurrence, max_occurrence=max_occurrence, **kwargs)

    def expand(self):
        output = [[self]]
        self.repair_parenthood()
        # self.repair_occurrences()
        return output

    def sort_children(self, xmltree):
        # print('sorting', self)
        # print()
        children = xmltree.get_children_by_type(self.type_)
        children = [child for child in children if child not in xmltree._sorted_children]
        children = children[:self.max_occurrence]
        xmltree._sorted_children.extend(children)

    def __deepcopy__(self):
        return Element(type_=self.type_, min_occurrence=self.min_occurrence, max_occurrence=self.max_occurrence)


class GroupReference(DTDNode):
    """"""

    def __init__(self, child, min_occurrence=1, max_occurrence=1):
        # self.child = copy.deepcopy(child)
        self.child = child.__deepcopy__()
        super().__init__(children=[self.child], min_occurrence=min_occurrence, max_occurrence=max_occurrence)

    def __deepcopy__(self):
        return GroupReference(self.child.__deepcopy__(), min_occurrence=self.min_occurrence, max_occurrence=self.max_occurrence)

    def expand(self):
        output = self.child.expand()
        return output

    def sort_children(self, xmltree):
        # print('sorting {} with children {}'.format(self, self.get_children()))
        # print()
        self.child.sort_children(xmltree)
