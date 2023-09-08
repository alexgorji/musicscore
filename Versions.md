# Version 1.0

This version is the first uploaded version to PyPI

# Version 1.1

musicxml as submodule

# Version 1.1.1

musicxml and quicktions as requirements

# Version 1.2

`Beat.add_child` and consequently `Beat._add_chord`, `Voice._add_chord` and `Measure._add_chord` return always a list of
Chords. `Part._add_chord` returns still None.

`Score.update()`, `Part.update()`, `Measure().update()`, `Beat._update_xml_notes()` and `Chord._update_xml_notes()`
refactored and renamed
to x.finalize(). finalize added to Staff and Voice. This method undertakes the last steps for creating
musicxml tree and can
only be called once. If to_string(), exists it checks if finalize is already called. If not it will be called
first.

`Measure._update_divisions` rename to `update_divisions()` and is only called by `Measure.finale_updates()`

`MusicTree.get_beats()` added

`MusicTree.get_part()`, get_staff() etc. refactored.

`MusicTree.quantize` attribute: Default is False, if quantization is necessary it must be set to True.

* If quantize is set to None the first quantize of ancestors which is `False` or `True` will be returned.
* If `Score.quantize` is set to None it will be converted to `False`
* `Measure.finalize()` loops over all beats. If `Beat.quantize` returns True `Beat.quantize_quarter_durations()` is
  called.

# Version 1.2.1

``__all__`` added to musictree modules and to ``musictree.__init__``

# Version 1.3

bugfix: ``measure._add_chord()`` adds beats to voice first if needed.

``tree`` folder removed. Use musicxml.tree instead for consistency.

# Version 1.3.1

``__set__setattr__`` ignores all private attributes starting with _. No need to add them to ``_ATTRIBUTES`` anymore.

``Chord.add_x()`` added: This method can be used for adding xml_articulation, xml_technical, xml_ornaments,
xml_dynamics,
xml_other_notations objects.

``Chord.add_xml_articulation`` and ``Chord.add_xml_technicals`` removed

``Chord.add_x()`` accepts kwargs for ``XMLDynamics``, ``XMLOrnaments``, ``XMLArticulation``, ``XMLTechnicals``

``Score.add_part()`` added

important bug fix: ``XMLChord`` is added now correctly to all midis except the first one.

# Version 1.3.2

Problem with packaging of v1.3.1> In the last version there got an old tree folder of musicxml wrongly in dist folder.
During pip installation of musicscore2 this old folder has been substituting the needed newer version of musicxml
package.

# Version 1.3.3

Add `musictree.testing` to `musictree` package

# Version 1.4

``SimpleFormat`` added. It is useful tool to generate list of chords and also do some simple algorithmic changes to it
if needed.
``Note.parent_chord`` removed. ``Midi`` is now required. ``Midi`` must have a parent_chord.
``Midi`` is now the core object for adding or removing ties to ``Chord`` (and ``Note``).
``Midi.notehead`` property added.
``Chord.add_midi(), Chord._sort_midis()`` added.
``Chord.add_direction_type()`` added.
``Chord.add_wedge()`` added.
``Chord.get_voice_number()`` and ``Chord.get_staff_number()`` return None if no ``Voice`` or ``Staff`` ancestor exist.
``Chord.__deepcopy__()`` added. Only midi and quarter_duration are deepcopied.
``Chord.clef`` property added.
``Chord.all_midis_are_tied_to_next`` and ``Chord.all_midis_are_tied_to_previous`` added.
``GraceChord()`` added.
``Time.signatures and Time.actual_signatures`` accept also strings to allow creating a complex time signature like 3+2+5/8 = ``Time('3+2+5', 8)``
Automatically created ``Time.actual_sigatures`` has been updated: 2/8 = 2/8; 4/8 = 2/8 + 2/8; 5/8 = 3/8 + 2/8; 7/8 = 4/8 + 3/8
``Accidental.mode`` changed to standard, enharmonic, sharp, flat, force-sharp and force-flat.
``Score`` Inherited methode ``Score.write`` will throw an Exception (.export_xml should be used instead).
``Clef`` argument default and property _default added (this will be True if Measure._update_default_clefs() set the
clef, otherwise it will be False).
``Staff`` default clef argument is changed to None. If no clef is set, it will automatically be set to clef of staff in
previous measure. If clef is changed the new clef will have the same number as the old one.
``add_chord()`` has been removed from ``Voice``, ``Measure`` and ``Beat``. Use ``Part.add_chord()`` instead!

``Bug Fix``: adding staff to a measure will only set default clefs automatically if the new or old staves does not have
a from user manually set clef. It means that the manually set clefs won't be overwritten any more.
``Bug Fix``: a Chord with tied notes will keep its tie after splitting.
``Bug Fix``: ``Score`` with multiple parts creates ``XMLPartList`` accordingly.
``Bug Fix``: cautionary signs are removed in repetitions.


