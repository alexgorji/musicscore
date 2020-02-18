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

todo:
update documentation
