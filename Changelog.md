# Version 2.0

A fully new version of musicscore. The old version does not exist anymore on PyPI. The repository of the old version is
still accessible via https://github.com/alexgorji/musicscore_old. It is strongly recommended to use musicscore 2.0 or
higher instead.

# Version 2.0.1

* Method `Chord.add_lyric()` cannot be called after finalization.

* `Chord.add_after_note_xml_objects` deprecated. Use `add_xml_element_after_notes` instead.

* `Chord.add_grace_chord()`: `type_` argument renamed to `type` to avoid autodoc conflicts.

* `GraceChord:` `type_` property renamed to `type` to avoid autodoc conflicts.

* `QuarterDuration.get_beatwise_sections` renamed to private method `_get_beatwise_sections`

* `util.chord_is_in_a_repetition` renamed to private function `_chord_is_in_a_repetition`

* `Score.new_system` added. It will be automatically set to True if a `Measure` sets its `Measure.new_system` to
True. `<encoding>` in XMLScore's `<identification>` will have a `<support>` child with attribute `new-system` if `Score.new_system` is set to True.

# Version 2.0.2

* `Beat.quantize_quarter_durations` improved to remove chords with quarter_duration 0 properly. Quantization now takes place in `part.finalize` before the actual finalizing of all measures.

# Version 2.1.0

* New module `config.py` added. All needed setup dictionaries has been moved or added to this module (`SPLITTABLES`, `NOTETYPES` etc.)

* `Beat.fill_with_rests()` added. This will be called in `finalize()` method of beat if it is not filled;
`Measure.fill_with_rests()` added. This method is called in measure’s finalize method

* `Voice.fill_with_rests()` added

* `Note.update_type` removed

* `Note.update_dots()` removed
* `Note.number_of_dots` removed

* Chord: midis and quarter_durations are now required arguments.

* `Chord.type` property added. If `None` and QuarterDuration not 0 `QuarterDuration.get_type()` will be called. `Note` uses this type to create `XMLType` children

* `Chord.number_of_dots` new property and some other changes for dots.

* New Class: `Tuplet`. Can be added to Chord as its tuplet property.

* If `type`, `number_of_dots` and `tuplet` of Chord of all chords in a beat are set not updates are executed.

* `Beat.get_chord_group_subdivision()` added (instead of private method of Beat). Beat sets `chord.tuplet` properties instead of creating xml objects directly for Note. Note itself create necessary xml objects according to its parent_chord

* `Beat.subidivion` property added

* `beat.beam_chord_group()` is updated and is now a public function.

* `Chord.beams` (dict) added. Example: `beams = {1:'begin', 2:'forward'}` `Chord.beams` can be None (forced no beams mode)

* `Chord.set_beam()` added

* `QuarterDuration` methods for getting type, `number_of_dots` and `tuplet_ratio` updated or created

* `Chord.check_printed_duration` and check_number_of_beams added (for testing reasons)

* Tuplets upto 15 and also 64th and 128th are implemented. 

# Version 2.3.0
* Use nativ library fractions instead of quicktions. The performance problem is no longer an issue.

# Version 2.3.1
* Bug fix: `QuarterDurtion.value` accepts also int and float. A TypeError is raised if value cannot be set.

# Version 2.3.2
* Simplify Part and ScorePart id uniqueness. It is enough to check during score finalization if added parts have unique ids.

* Check if score has parts before finalization

* Bug fixes

# Version 2.3.3

* Bug fixes
