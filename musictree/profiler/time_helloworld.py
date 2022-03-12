import cProfile
import timeit
from xml.etree import ElementPath

from musictree import Score, Part, Chord, Id
from musicxml.xmlelement.xmlelement import XMLScorePartwise, XMLLeftMargin


def hello_xml_score():
    XMLScorePartwise()


def hello_xml_left_margin():
    XMLLeftMargin(10)


def hello():
    s = Score()
    p = s.add_child(Part('p1'))
    p.add_chord(Chord(60, 4))
    s.to_string()
    Id.__refs__.clear()


def time_hello_xml_score():
    print(timeit.timeit(hello_xml_score, number=1))


def time_hello_xml_left_margin():
    print(timeit.timeit(hello_xml_left_margin, number=100))


def time_hello():
    print(timeit.timeit(hello, number=100))


cProfile.run('time_hello()', sort="cumtime")
