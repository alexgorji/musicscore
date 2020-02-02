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

todo:
update documentation