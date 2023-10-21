# Version 1.0

This version is the first uploaded version to PyPI

# Version 1.1

musicxml as submodule

# Version 1.1.1

musicxml and quicktions as requirements

# Version 1.2

`Beat.add_child` and consequently `Beat._add_chord`, `Voice._add_chord` and `Measure._add_chord` return always a list of
Chords. `Part._add_chord` returns still None.

`Score._update()`, `Part._update()`, `Measure()._update()`, `Beat._update_xml_notes()` and `Chord._update_xml_notes()`
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
* `Measure.finalize()` loops over all beats. If `Beat.quantize` returns True `Beat._quantize_quarter_durations()` is
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

/////////////////////////// CHANGE IN PACKAGING >>>>>>
musicscore2 was removed from pip. The old package musicscore has been reactivated. musicscore version 2.0 corresponds to
musicscore2. All older versions of musicscore2 are not anymore accessible via pip. The repository musicscore2 is however
still publicly reachable which contains a tag for each version.
``musictree`` has been renamed to musicscore for consistency reasons. All classes can be imported new with the
command``import musicscore.CLASS`` or ``from musicscore import *``.

# Version 2.0

``Accidental.mode`` changed to standard, enharmonic, sharp, flat, force-sharp and force-flat.

``add_chord()`` has been removed from ``Voice``, ``Measure`` and ``Beat``. Use ``Part.add_chord()`` instead!

``Chord.add_midi(), Chord._sort_midis()`` added.
``Chord.add_direction_type()`` added.
``Chord.add_wedge()`` added.
``Chord.add_words()`` added.
``Chord.add_after_note_xml_objects()`` added.
``Chord.get_voice_number()`` and ``Chord.get_staff_number()`` return None if no ``Voice`` or ``Staff`` ancestor exist.
``Chord.__deepcopy__()`` added. Only midi and quarter_duration are deepcopied.
``Chord.clef`` property added.
``Chord.arpeggio`` property added.
``Chord.get_x()`` added.
``Chord.get_words(), Chord.get_slurs(), Chord.get_wedges(), Chord.get_brackets()`` added.
``Chord.metronome`` property added.
``Chord.all_midis_are_tied_to_next`` and ``Chord.all_midis_are_tied_to_previous`` added.
``Chord.get_grace_chords()`` added.

``Clef`` argument default and property _default added (this will be True if Measure._update_default_clefs() set the
clef, otherwise it will be False).

``GraceChord()`` added.

``Lyrics`` added. A class to generate XMLLyrics and adding it to a list of chords.

``Measure.new_system`` property added.
``Measure.barline_style`` removed
``Measure.set_barline()`` added
``Measure.get_barline()`` added
``Measure().set_repeat_barline()`` method added.
``Measure.set_repeat_ending()`` added

``Metronome`` new Class.

``Midi`` is now the core object for adding or removing ties to ``Chord`` (and ``Note``).
``Midi.notehead`` property added.
``Midi.set_staff_number()`` and ``Midi.get_staff_number()`` added to make staff crossing possible.

``Note.parent_chord`` removed. ``Midi`` is now required. ``Midi`` must have a parent_chord.

``Part.abbreviation`` property added.

``PerucssionClef()`` added.

``QuarterDurartion.get_type()`` and ``QuarrterDurtion.get_number_of_dots()`` added.

``Rest`` class added.

``Score`` Inherited methode ``Score.write`` will throw an Exception (.export_xml should be used instead).
``Score.xml_identifacation.xml_encondings.xml_supports`` two support added for print new system and print new page.
``Score.group_parts(number, start_part_number, end_part_number, symbol='square', name=None, abbreviation=None)`` added
``Score.group_parts()`` **kwargs added. This will be added to ``XMLGroupSymbol``
``Score.set_multi_measure_rest()`` method added.

``SimpleFormat`` added. It is useful tool to generate list of chords and also do some simple algorithmic changes to it
if needed.

``Staff`` default clef argument is changed to None. If no clef is set, it will automatically be set to clef of staff in
previous measure. If clef is changed the new clef will have the same number as the old one.

``Time.signatures and Time.actual_signatures`` accept also strings to allow creating a complex time signature like
3+2+5/8 = ``Time('3+2+5', 8)``Automatically created ``Time.actual_sigatures`` has been updated: 2/8 = 2/8; 4/8 = 2/8 +
2/8; 5/8 = 3/8 + 2/8; 7/8 = 4/8 + 3/8

``util.slur_chords(), util.wedge_chords(), util.trill_chords(), util.bracket_chords(), util.octave_chords()`` added.

``Bug Fix``: adding staff to a measure will only set default clefs automatically if the new or old staves does not have
a from user manually set clef. It means that the manually set clefs won't be overwritten any more.
``Bug Fix``: a Chord with tied notes will keep its tie after splitting.
``Bug Fix``: ``Score`` with multiple parts creates ``XMLPartList`` accordingly.
``Bug Fix``: cautionary signs are removed in repetitions.
Some Exceptions added or renamed.


