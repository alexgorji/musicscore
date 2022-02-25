INTRO
#####

musicscore2
===========
**musicscore2** is a python library for generating musicxml data in an intuitive and easy but nevertheless exhaustive way. The generated
files can be imported in several music notation programs and be processed further if necessary. The preferred software is Finale which
seems at the moment to have the best implementation of musicxml format files and supports the newest version 4.0.

**musicscore2** consists of two main packages: **musicxml** and **musictree**:

musicxml
========

The central class of this package is the :obj:`~musicxml.xmlelement.xmlelement.XMLElement` class which is the parent of each individual
xml element class (like XMLScore, XMLPart etc.). The xml element classes (mainly created automatically) behave exactly as declared in the
musicxml schema file. The ``type_`` of Each :obj:`~musicxml.xmlelement.xmlelement.XMLElement` class is set to :obj:`~musicxml.xsd.xsdcomplextype.XSDComplexType` or :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleType` which correspond to xml schema elements ``complexType``
and
``simpleType``.
The documentation of this package covers only the information given in the musicxml schema file, including the structure of possible or
necessary children and attributes indicated by xsd elements and and cannot replace the more comprehensive documentation of `W3C Community Group <https://www.w3.org/2021/06/musicxml40/>`_ . The topic of xml and xml schema goes beyond the scope of this documentation. For further information see `here <https://www.w3schools.com/xml/default.asp>`_

musictree
=========

The goal of this package is to simplify the use of musicxml elements. The tree structure of a score plays here a fundamental role and is
being controlled via :obj:`~musictree.musictree.MusicTree` parent class. Most of the objects in this hierarchy are closely connected to
the corresponding objects in musicxml package and are descendents of :obj:`~musictree.xmlwarpper.XMLWrapper` class with an :obj:`~musictree
.xmlwarpper.XMLWrapper.xml_object` attribute. There are though some other important classes like :obj:`~musictree.beat.Beat` or
:obj:`~musictree.chord.Chord` which don't have any direct equivalents in the musicxml structure.

A musictree consists of a root :obj:`~musictree.score.Score` and its 9 descending layers:

#. :obj:`musictree.score.Score` is the root of a musictree.

    * It is the parent of :obj:`musictree.part.Part`

    * It creates all necessary defaults:

        * Default layout objects inside the default can be changed directly via following properties:

            * scaling :obj:`musictree.layout.Scaling`
            * page_layout :obj:`musictree.layout.PageLayout`
            * system_layout :obj:`musictree.layout.StaffLayout`
            * staff_layout' :obj:`musictree.layout.StaffLayout`

    * :obj:`~musictree.score.Score.export_xml` method can be used to create the "end product" as a xml file.


#. :obj:`musictree.part.Part` is the first layer of a musictree.

    * It is the parent of :obj:`musictree.measure.Measure`

    * It must have a unique `id` during initialization. If no name is associated with the part its id will be used as its name.

    * Its method :obj:`~musictree.part.Part.add_measure()` can be used to conveniently add measures. It accepts two arguments:

        * ``number`` can be used to set the measure number. If ``None`` measure's number will be added automatically as one number higher
          than the previous measure (or 1 for the first measure).

        * ``time`` can be used to set the time signature. If ``None`` the previous time signature is adopted and set to hidden. The
          time signature of the first measure with time ``None`` is set to 4/4.


#. :obj:`musictree.measure.Measure` is the second layer of a musictree.

    * It is the parent of :obj:`musictree.staff.Staff`

    * It must set its number by initialization.

    * It has three important properties which can be set to control measure's ``time signature``, the ``clefs`` of its staves and its
      ``key``.

        * :obj:`musictree.time.Time`

        * :obj:`musictree.clef.Clef`

        * :obj:`musictree.key.Key`

#. :obj:`musictree.staff.Staff` is the third layer of a musictree.

    * It is the parent of :obj:`musictree.voice.Voice`

    * It has two properties: ``number`` and :obj:`musictree.clef.Clef`

#. :obj:`musictree.voice.Voice` is the fourth layer of a musictree.

    * It is the parent of :obj:`musictree.beat.Beat`

    * Each voice has its own independent beats which are created based on measure's time signature.

    * It has a ``number`` as property.

    * When its last beat is filled the ``is_filled`` property is ``true``.

    * If a :obj:`musictree.chord.Chord` is added to its beats which has a quarter duration greater than the sum of beats' quarter
      durations, the remaining Chord can be accessed via ``leftover`` property.

#. :obj:`musictree.beat.Beat` is the fifth layer of a musictree.

    * It is the parent of :obj:`musictree.chord.Chord`

#. :obj:`musictree.chord.Chord` is the sixth layer of a musictree.

    * It is the parent of :obj:`musictree.note.Note`

        * :obj:`musictree.dynamics.Dynamics`

#. :obj:`musictree.note.Note` is the seventh layer of a musictree.

    * It is the parent of :obj:`musictree.midi.Midi`

#. :obj:`musictree.midi.Midi` is the eighth layer of a musictree.

    * It is the parent of :obj:`musictree.accidental.Accidental`

#. :obj:`musictree.accidental.Accidental` is the ninth layer of a musictree.

QuarterDuration non-writables and quantizing
--------------------------------------------

* :obj:`musictree.quarterduration.QuarterDuration`

Layout
------

* :obj:`musictree.layout.Scaling`

* :obj:`musictree.layout.PageLayout`

* :obj:`musictree.layout.StaffLayout`

* :obj:`musictree.layout.StaffLayout`



.. note::

   This project is under active development.

Check out the :doc:`usage` section for further information, including how to :ref:`install <installation>` the project.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
