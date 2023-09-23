import cProfile
import timeit
from contextlib import redirect_stdout
from pathlib import Path

from musicscore import Score, Part, Chord, Id


def hello():
    s = Score()
    p = s.add_child(Part('p1'))
    p.add_chord(Chord(60, 4))
    s.to_string()
    Id.__refs__.clear()


def time_hello():
    print(timeit.timeit(hello, number=1000))


with open(Path(__file__).with_suffix('.txt'), '+w') as f:
    with redirect_stdout(f):
        cProfile.run('time_hello()', sort="tottime")
