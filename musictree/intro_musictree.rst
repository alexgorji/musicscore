musictree
*********

The goal of this package is to simplify the use of musicxml elements. The tree structure of a score plays here a fundamental role and is
being controlled via :obj:`~musictree.core.MusicTree` parent class. Most of the objects in this hierarchy are closely connected to
the corresponding objects in musicxml package and are descendents of :obj:`~musictree.xmlwrapper.XMLWrapper` class with an
:obj:`~musictree.xmlwrapper.XMLWrapper.xml_object` attribute. There are though some other important classes like :obj:`~musictree.beat.Beat` or :obj:`~musictree.chord.Chord` which don't have any direct equivalents in the musicxml structure.

A musictree consists of a root :obj:`~musictree.score.Score` and its 9 descending layers:

#. :obj:`musictree.score.Score` is the root of a musictree.

    * It is the parent of :obj:`musictree.part.Part` and has no parent itself.

    * It creates all necessary defaults:

        * Default layout objects inside the default can be changed directly via following properties:

            * scaling :obj:`musictree.layout.Scaling`
            * page_layout :obj:`musictree.layout.PageLayout`
            * system_layout :obj:`musictree.layout.StaffLayout`
            * staff_layout' :obj:`musictree.layout.StaffLayout`

    * :obj:`~musictree.score.Score.export_xml` method can be used to create the "end product" as a xml file.


#. :obj:`musictree.part.Part` is the first layer of a musictree.

    * It is the parent of :obj:`musictree.measure.Measure` and and the child of :obj:`musictree.score.Score`.

    * It must have a unique `id` during initialization. If no name is associated with the part its id will be used as its name.

    * Its method :obj:`~musictree.part.Part.add_measure()` can be used to conveniently add measures. It accepts two arguments:

        * ``number`` can be used to set the measure number. If ``None`` measure's number will be added automatically as one number higher
          than the previous measure (or 1 for the first measure).

        * ``time`` can be used to set the time signature. If ``None`` the previous time signature is adopted and set to hidden. The
          time signature of the first measure with time ``None`` is set to 4/4.


#. :obj:`musictree.measure.Measure` is the second layer of a musictree.

    * It is the parent of :obj:`musictree.staff.Staff` and the child of :obj:`musictree.part.Part`.

    * It must set its number during initialization.

    * It has three important properties which can be set to control measure's ``time signature``, its ``key`` and ``clefs`` of its staves.

        * :obj:`musictree.time.Time`

        * :obj:`musictree.clef.Clef`

        * :obj:`musictree.key.Key`

#. :obj:`musictree.staff.Staff` is the third layer of a musictree.

    * It is the parent of :obj:`musictree.voice.Voice` and the child of :obj:`musictree.staff.Staff`.

    * It has two properties: ``number`` and :obj:`musictree.clef.Clef`

#. :obj:`musictree.voice.Voice` is the fourth layer of a musictree.

    * It is the parent of :obj:`musictree.beat.Beat`  and and the child of :obj:`musictree.staff.Staff`

    * Each voice has its own independent beats which are created based on measure's time signature.

    * It has a ``number`` as property.

    * When its last beat is filled the ``is_filled`` property is ``true``.

    * If a :obj:`musictree.chord.Chord` is added to its beats which has a quarter duration greater than the sum of beats' quarter
      durations, the remaining Chord can be accessed via ``leftover`` property.

#. :obj:`musictree.beat.Beat` is the fifth layer of a musictree.

    * It is the parent of :obj:`musictree.chord.Chord` and and the child of :obj:`musictree.voice.Voice`.
    * Duration of a :obj:`~musictree.beat.Beat` can be 4, 2, 1 or 0.5 :obj:`~musictree.quarterduration.QuarterDuration`

    * Quarter duration of a beat's :obj:`~musictree.chord.Chord` child can exceed its own quarter duration. If a :obj:`~musictree.chord.Chord` is longer than the quarter duration of beat's parent :obj:`~musictree.voice.Voice`, a leftover :obj:`~musictree.chord.Chord` will be added as leftover property to the :obj:`~musictree.voice.Voice` which will be added to next measure's appropriate voice .

    * Beat manages splitting of each child :obj:`~musictree.chord.Chord` into appropriate tied :obj:`~musictree.chord.Chord` s if needed,
      for example if this chord has a non-writable quarter duration like 5/6.

    * The dots and tuplets are also added here to :obj:`~musictree.chord.Chord` or directly to their :obj:`~musictree.note.Note` children.

    * Beaming and quantization are also further important tasks of a beat.

#. :obj:`musictree.chord.Chord` is the sixth layer of a musictree.

    * It is the parent of :obj:`musictree.note.Note` and and the child of :obj:`musictree.beat.Beat`.
       
    * Chord is a sequence of one or more :obj:`~musicxml.xmlelement.xmlelement.XMLNote`s which occur at the same time in a :obj:`~musicxml.xmlelement.xmlelement.XMLMeasure` of a :obj:`~musicxml.xmlelement.xmlelement.XMLPart`.

     * :obj:`~musictree.lyric.Lyric`, :obj:`~musictree.dynamics.Dynamics`, :obj:`~musictree.clef.Clef` etc. can be added to a Chord via
       its add_x methods. The corresponding XMLElement objects will be added to :obj:`~musicxml.xmlelement.xmlelement.XMLNote` or
       :obj:`~musicxml.xmlelemen.xmlelement.XMLMeasure` as necessary.

    * Other useful add_x methods like :obj:`~musictree.chord.Chord.add_articulation(), :obj:`~musictree.chord.Chord.add_technical()` are
      available for adding other XMLElements to XMLNotes.


#. :obj:`musictree.note.Note` is the seventh layer of a musictree.

    * It is the parent of :obj:`musictree.midi.Midi` and the child of :obj:`musictree.chord.Chord`.

    * Although :obj:`~musictree.chord.Chord` offers a series of possibilities to add objects to notes, note objects
      can be also directly accessed and manipulated.

#. :obj:`musictree.midi.Midi` is the eighth layer of a musictree.

    * It is the parent of :obj:`musictree.accidental.Accidental` and the child of :obj:`musictree.note.Note`

    * Midi is the representation of a Pitch with its midi value, and accidental sign. This object is used to create a Chord consisting of
      one or more pitches. The midi representation of a rest is a Midi object with value 0.

#. :obj:`musictree.accidental.Accidental` is the ninth layer of a musictree.

    * It is the child of :obj:`~musictree.note.Note` and has not children itself.

    *  Accidental is the class for managing :obj:`musictree.midi.Midi`'s accidental sign and its pitch parameters: step, alter, octave.

    * The parameter mode (standard, flat, sharp, enharmonic_1 or enharmonic_2) can be used to set different enharmonic variants of the
      same pitch.


* :obj:`musictree.quarterduration.QuarterDuration`
    *  A Class specifically designed for durations measured in quarters. The core of this class is a value of type  quicktions.Fraction
       with a denominator limit of 1000, thus it can manage conversion of floats to fractions without usual inaccuracies of quintuples etc.

    * QuarterDuration has all needed magic methods for numeral comparison and conversion.


Quantization
------------

A central feature of musictree is Beat's :obj:`~musictree.beat.Beat.quantize()` method. A list of possible
subdivisions can be set and get on different levels in the musictree structure via
:obj:`~musictree.core.MusicTree.set_possible_subdivisions()` and
:obj:`~musictree.core.MusicTree.get_possible_subdivisions()`. Default values are set by
:obj:`~musictree.score.Score`: :obj:`~musictree.score.POSSIBLE_SUBDIVISIONS`. Each beat checks its own and its
ancestors subsequently until finding possible subdivisions for its quarter duration in a possible_subdivisions
dictionary. For example if beat has a 1 quarter duration length and the dictionary returned by
:obj:`~musictree.core.MusicTree.get_possible_subdivisions()` method of beat's ancestor
:obj:`~musictree.measure.Measure` has a QuarterDuration(1) key with a list [2, 3, 4, 6] as its associated item, the
quantization of the beat changes the quarter duration of its Chord children in a way that only 8ths, triplets,
16ths and sextuplets will be used. :obj:`~musictree.beat.Beat.quantize()` calculates always the most accurate
results according to the given possible subdivisions in which values with the smallest deviation from original
quarter duration values are chosen.