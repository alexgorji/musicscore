Package musicscore  
containing musicxml, musictree, musicstream

see documentation on
https://github.com/alexgorji/musicscore.git  


v 1.0.1:  
TreeScoreTimewise().extend: bug fixed: \_add_identification() deleted

v 1.1.0:  
PartGroup() and needed children: added 
TreeScorePart().add_part_group(): added

v 1.1.1:  
PartList().dtd: Choice added 

    _DTD = Sequence(
        Choice(Element(PartGroup, min_occurrence=0, max_occurrence=None),
               Element(ScorePart)
               ),
        Choice(
            Element(PartGroup),
            Element(ScorePart),
            min_occurrence=0, max_occurrence=None
        )
    )
It is now possible to use goto_next_dtd_choice() to go to second Choice()  
see: test_part_list.py


v. 1.2.1:   
TreeInstrument().standard_clef: attribute added  
TreePart().chord_to_notes(): renamed to: chords_to_notes  
TreeChord().FingerTremolo(): removed  
TreePart().chords_to_notes(): optimised to set clef to TreeInstrument().standard_clef
TreeMeasure().previous: added: if not self.up: return None

v. 1.2.2:  
musictree.Midi().\__name__: added

v. 1.2.3:   
TreeChordFlag.implement(): added
TreeBeat.implement_flags(): bug fix (more tests are necessary)
TreeBeat.split_not_notatable(): 5/2 position 0.5 changed to (1,4)

v. 1.2.4:  
TreeBeat.split_not_notatable(): bug fixes

v. 1.2.5:  
quantization problem bug #3 solved: Beat._correct_deviations() was added.

v. 1.2.6:
add_words(): accept text and words
wordsymbols: SALTANDO added


v. 1.2.7:
Midi(): comparison methods for <, =<, > and >= added
TreeClef().optimal_range: attribute added
SimpleFormat().auto_clef(): argument added: clefs


v. 1.2.8:
issue #4 bug fixed: vanishing clef in score
issue #5
add method: TreeChord().remove_dynamic() 

v. 1.2.9
TreeChord().set_manual_dots: method added
TreeChord().add_grace_chords()

v. 1.2.10
issue #7 bug fixed: fill_with_rest() rest zero_mode is now 'remove'

v. 1.2.11
issue #8 bug fixed: TreeChord().quarter_duration --> Fraction().limiter omitted

v. 1.2.12
SimpleFormat().quarter_duration added
SimpleFormat().quarter_durations omitted
SimpleFormat(): minor changes


v. 1.2.13  
build conflicts resolved

todo:
update documentation
