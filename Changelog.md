# Version 2.0

A fully new version of musicscore. The old version does not exist anymore on PyPI. The repository of the old version is
still accessible via https://github.com/alexgorji/musicscore_old. It is strongly recommended to use musicscore 2.0 or
higher instead.

# Version 2.0.1

Method Chord.add_lyric() cannot be called after finalization.
Chord.add_after_note_xml_objects deprecated. Use add_xml_element_after_notes instead.
Chord.add_grace_chord(): type_ argument renamed to type to avoid autodoc conflicts.
GraceChord: type_ property renamed to type to avoid autodoc conflicts.
QuarterDuration.get_beatwise_sections renamed to private method _get_beatwise_sections
util.chord_is_in_a_repetition renamed to private function _chord_is_in_a_repetition
Score.new_system added. It will be automatically set to True if a Measure sets its Measure.new_system to True. <encoding> in XMLScore`\'s <identification> will have a <support> child with attribute 'new-system' if Score.new_system is set to True.

# Version 2.0.2
Beat.quantize_quarter_durations improved to remove chords with quarter_duration 0 properly
Quantization now takes in Part.finalize before the actual finalizing of all measures.