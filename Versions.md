# Version 1.0

This version is the first uploaded version to PyPI

# Version 1.1
musicxml as submodule

# Version 1.1.1
musicxml and quicktions as requirements

# Version 1.2
`Beat.add_child` and consequently `Beat.add_chord`, `Voice.add_chord` and `Measure.add_chord` return always a list of Chords. `Part.add_chord` returns still None.

`Score.update()`, `Part.update()`, `Measure().update()`, `Beat._update_xml_notes()` and `Chord._update_xml_notes()` refactored and renamed 
to x.final_updates(). final_updates added to Staff and Voice. This method undertakes the last steps for creating musicxml tree and can 
only be called once. If to_string(), exists it checks if final_updates is already called. If not it will be called first.

`Measure._update_divisions` rename to `update_divisions()` and is only called by `Measure.finale_updates()`

`MusicTree.get_beats()` added
`MusicTree.get_part()`, get_staff() etc. refactored.

`MusicTree.quantize` attribute: Default is False, if quantization is necessary it must be set to True. 
  * If quantize is set to None the first quantize of ancestors which is `False` or `True` will be returned.
  * If `Score.quantize` is set to None it will be converted to `False`
  * `Measure.final_updates()` loops over all beats. If `Beat.quantize` returns True `Beat.quantize_quarter_durations()` is called.

# Version 1.2.1
``__all__`` added to musictree modules and to ``musictree.__init__``

# Version 1.3
bugfix: ``measure.add_chord()`` adds beats to voice first if needed. 
``tree`` folder removed. Use musicxml.tree instead for consistency.
