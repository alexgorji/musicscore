from unittest import TestCase

from musictree.midi import Midi
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
