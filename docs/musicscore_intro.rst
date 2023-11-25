Introduction
============

.. warning::
   This documentation is still under construction!


Tested with python 3.9, 3.10 and 3.11

**musicscore** is a python library for generating MusicXML data in an intuitive and easy but nevertheless exhaustive way. The generated files can be imported in several music notation programs and be processed further if necessary. The preferred software is Finale which seems at the moment to have the best implementation of MusicXML format files and supports version 4.0.

**musicscore** depends heavily on the library **musicxml** which allows an object oriented and comprehensive approach to MusicXML format.

The main classes of **musicscore** are arranged in a tree structure which is roughly based on the tree structure of the <score-partwise> element. The :obj:`~musicscore.musictree.MusicTree` (a child class of the absract class :obj:`~tree.tree.Tree`) is used as parent of all the following classes:

        - :obj:`~musicscore.score.Score` (root)
        - :obj:`~musicscore.part.Part` (1st layer)
        - :obj:`~musicscore.measure.Measure` (2nd layer)
        - :obj:`~musicscore.staff.Staff` (3rd layer)
        - :obj:`~musicscore.voice.Voice` (4th layer)
        - :obj:`~musicscore.beat.Beat` (5th layer)
        - :obj:`~musicscore.chord.Chord`, :obj:`~musicscore.chord.Rest` or :obj:`~musicscore.chord.GraceChord` (6th layer)
        - :obj:`~musicscore.note.Note` (7th layer)
        - :obj:`~musicscore.midi.Midi` (8th layer)
          Midi can represent a pitch or a rest (value=0) and controls accidental sign of the pitch if necessary.
        - :obj:`~musicscore.accidental.Accidental` (9th layer)


See also :ref:`installation` and :ref:`examples`.
