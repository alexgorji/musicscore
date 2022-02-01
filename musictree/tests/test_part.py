from unittest import TestCase

from musictree.exceptions import IdHasAlreadyParentOfSameTypeError, IdWithSameValueExistsError
from musictree.measure import Measure
from musictree.part import Part, ScorePart, Id


class TestWithId(TestCase):
    def setUp(self) -> None:
        Id.__refs__.clear()


class TestId(TestWithId):

    def test_id_refs(self):
        id1 = Id('p1')
        id2 = Id('p2')
        assert Id.__refs__ == [id1, id2]
        id3 = Id('p3')
        assert Id.__refs__ == [id1, id2, id3]
        id3.delete()
        assert Id.__refs__ == [id1, id2]
        Id('p3')

    def test_id_unique(self):
        Id('p1')
        id2 = Id('p2')
        with self.assertRaises(IdWithSameValueExistsError):
            Id('p1')
        id3 = Id('p3')
        with self.assertRaises(IdWithSameValueExistsError):
            Id('p2')
        with self.assertRaises(IdWithSameValueExistsError):
            id3.value = 'p2'
        assert id3.value == 'p3'
        id2.delete()
        id3.value = 'p2'
        assert id3.value == 'p2'

    def test_id_parents(self):
        id_ = Id('p1')
        assert id_.get_parents() == []
        p = Part(id=id_)
        assert id_.get_parents() == [p, p.score_part]
        with self.assertRaises(IdHasAlreadyParentOfSameTypeError):
            Part(id=id_)
        with self.assertRaises(IdHasAlreadyParentOfSameTypeError):
            ScorePart(part=p)
        assert p.xml_object.id == p.score_part.xml_object.id == 'p1'
        id_.value = 'p2'
        assert p.xml_object.id == p.score_part.xml_object.id == 'p2'
        p.id_ = 'p3'
        assert p.xml_object.id == p.score_part.xml_object.id == 'p3'


class TestPart(TestWithId):
    def test_part_init(self):
        p = Part(id='p1')
        p.add_child(Measure(1))
        expected = """<part id="p1">
    <measure number="1" />
</part>
"""
        assert p.to_string() == expected

    def test_part_name(self):
        p = Part(id='p1')
        assert p.name == 'p1'
        p = Part(id='p2', name='Part 1')
        assert p.name == 'Part 1'
        p.name = None
        assert p.name == 'p2'

    def test_part_and_score_part(self):
        p = Part(id='p1')
        assert isinstance(p.score_part, ScorePart)
        assert p.score_part.xml_object.id == p.xml_object.id


class TestScorePart(TestWithId):

    def test_score_part_name(self):
        p = Part(id='p1')
        assert p.score_part.xml_part_name.value == p.name == 'p1'
        p.name = 'Part 1'
        assert p.score_part.xml_part_name.value == p.name == 'Part 1'
        p.name = None
        assert p.score_part.xml_part_name.value == p.name == 'p1'

    def test_score_part_to_string(self):
        p = Part(id='p1')
        expected = """<score-part id="p1">
    <part-name>p1</part-name>
</score-part>
"""
        assert p.score_part.to_string() == expected
