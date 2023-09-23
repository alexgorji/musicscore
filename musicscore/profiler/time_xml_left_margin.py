import cProfile
import timeit
from contextlib import redirect_stdout
from pathlib import Path

from musicxml.xmlelement.xmlelement import XMLLeftMargin


def hello_xml_left_margin():
    XMLLeftMargin(10)


def time_hello_xml_left_margin():
    print(timeit.timeit(hello_xml_left_margin, number=1000))


with open(str(Path(__file__)) + 'xml_left_margin.txt', '+w') as f:
    with redirect_stdout(f):
        cProfile.run('time_hello_xml_left_margin()', sort="tottime")
