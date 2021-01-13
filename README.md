Package musicscore  
containing musicxml, musictree, musicstream

see documentation on
https://github.com/alexgorji/musicscore.git  

### v1.0.1:  
TreeScoreTimewise().extend: bug fixed: \_add_identification() deleted

### v1.1.0:  
PartGroup() and needed children: added 
TreeScorePart().add_part_group(): added

### v1.1.1:  
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

### v1.2.1:   
TreeInstrument().standard_clef: attribute added  
TreePart().chord_to_notes(): renamed to: chords_to_notes  
TreeChord().FingerTremolo(): removed  
TreePart().chords_to_notes(): optimised to set clef to TreeInstrument().standard_clef
TreeMeasure().previous: added: if not self.up: return None

### v1.2.2:  
musictree.Midi().\__name__: added

### v1.2.3:   
TreeChordFlag.implement(): added
TreeBeat.implement_flags(): bug fix (more tests are necessary)
TreeBeat.split_not_notatable(): 5/2 position 0.5 changed to (1,4)

### v1.2.4:  
TreeBeat.split_not_notatable(): bug fixes

### v1.2.5:  
quantization problem bug #3 solved: Beat._correct_deviations() was added.

### v1.2.6:  
add_words(): accept text and words
wordsymbols: SALTANDO added


### v1.2.7:  
Midi(): comparison methods for <, =<, > and >= added
TreeClef().optimal_range: attribute added
SimpleFormat().auto_clef(): argument added: clefs


### v1.2.8:  
issue #4 bug fixed: vanishing clef in score
issue #5
add method: TreeChord().remove_dynamic() 

### v1.2.9:  
TreeChord().set_manual_dots: method added
TreeChord().add_grace_chords()

### v1.2.10:   
issue #7 bug fixed: fill_with_rest() rest zero_mode is now 'remove'

### v1.2.11:   
issue #8 bug fixed: TreeChord().quarter_duration --> Fraction().limiter omitted

### v1.2.12:   
SimpleFormat().quarter_duration added
SimpleFormat().quarter_durations omitted
SimpleFormat(): minor changes


### v1.2.13:    
build conflicts resolved

### v1.2.14:   
issue#2 PageStyle(): by changing page_width and page_height: CreditWords default_x and default_y will be changed accordingly.

### v1.2.15:    
issue#11 bug fix: post grace chord  
issue#12 changes: Midi.accidental_mode flat and sharp: in this modes don't use b-sharp, e-sharp, f-flat and c-flat  

### v1.2.16:    
TreeChordFlags: TreeChordFlag3 deleted, some renaming took place

Midi.accidental: class Accidental() instead of accidental_mode. 
MidiNote().accidental renamed to accidental_sign
Midi.accidental.force_show: new feature
Midi.accidental.force_hide: new feature

### v1.2.17:    
musicxml.groups.musicdata.Attributes.staves: updated  
TreeChord().staff_number: property added   
TreeScorePart().number_of_staves: property added  
musicxml.types.complextypes.clef: missing attributes added  
tests: musicxml.types.complextype.clef: added  
TreePart().add_clef(): method added
StreamVoice().add_to_score(score, part_number=1, staff_number=None, first_measure=1): attribute staff_number added and order of attributes changed
TreePart().fill_with_rest(): _fill_with_voices() added
TreePart().add_chord(): attribute staff_number added

### v1.3:    
Minor and major changes
Tree structure was changed: TreePart ==> TreePartStaff ==> TreePartVoice
parts with more than one staves are now possible.

### v1.3.1:    
XMLChord was deleted  
TreeChord has all necessary methods for updating accidentals  
TreeNote's parent_chord is non optional  
TreeNote properties like quarter_duration, offset etc. calls parent_chord properties  
treenote deleted TreeNote etc. moved to treechord  

TreeInstrumnent: number_of_staves added  
TreeScoreTimewise: add_instrument() added  
TreeInstrument: standard_clef changed to standard_clefs  
New TreeInstruments Piano and Voice added  
etc.  

### v1.3.2:    
issue#19: bug fix staff 2: add_words(), add_dynamics() etc.

### v1.3.3:  
some minor bug fixes
musicxml.types.complextypes.staffdetails: added.

### v1.3.4:  
issue#20 bug fix:
* TreeChord().split_copy() => child of type Stem() will be copied
    
issu#22: SimpleFormat() canonical utility methods added:
* retrograde(), mirror(), multiply_quarter_durations() \[transpose() already existed]

SimpleFormat() change_chords(function) replaced change_chord_formula()

issue#24: simple_format.sum (static) added

### v1.3.5:  
TreeChord or TreeNote.add_lyric(): arguments syllabic and extend added
Extend() bug fix

### v1.3.6:
TreeChord().add_trill_mark(): function added
TreeChord().add_wavy_line(): function added

### v1.3.7
TreeChord().add_pedal(): function added

### v1.3.8
LyricFont() added 

### v1.3.9
TreeScoreTimewise().add_page_number(): function added 

### v1.3.10
Bug fixed: group beams: ignoring group of chords with only one chord 

### v1.3.12
Bug fixed: TreePartVoice._beats = [] instead fo None
TreeScoreTimewise().finish_til_flat_1 ...

### v1.3.13
Enhancement: TreeChord.add_dynamics accepts list of values

todo:
update documentation
