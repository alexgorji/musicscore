import cProfile
import timeit
from contextlib import redirect_stdout
from pathlib import Path
from xml.etree import ElementPath

from musicscore import Score, Part, Chord, Id
from musicxml.xmlelement.xmlelement import XMLScorePartwise, XMLLeftMargin


def hello_xml_score():
    XMLScorePartwise()


def time_hello_xml_score():
    print(timeit.timeit(hello_xml_score, number=1000))


with open(str(Path(__file__)) + 'xml_score.txt', '+w') as f:
    with redirect_stdout(f):
        cProfile.run('time_hello_xml_score()', sort="tottime")
