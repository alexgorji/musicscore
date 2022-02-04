from difflib import Differ
from pathlib import Path
from unittest import TestCase

from musictree.part import Id


def check_notes(notes, midi_values, quarter_durations):
    if len(notes) != len(midi_values) or len(notes) != len(quarter_durations):
        raise ValueError
    for n, m, qd in zip(notes, midi_values, quarter_durations):
        assert n.midi.value == m
        assert n.quarter_duration == qd


class IdTestCase(TestCase):
    def setUp(self) -> None:
        Id.__refs__.clear()


def _create_expected_path(path):
    return Path(path.parent / f"{path.stem}_expected{path.suffix}")


def diff_xml(path_1, path_2=None):
    if path_2 is None:
        path_2 = _create_expected_path(path_1)

    with open(path_1) as f1, open(path_2) as f2:
        f_1 = [i.strip() for i in f1]
        f_2 = [i.strip() for i in f2]

    diff = Differ()
    difference = list(diff.compare(f_1, f_2))
    return [d for d in difference if d.startswith('-') or d.startswith('+')]
