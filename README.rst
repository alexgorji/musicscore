INTRO
#####

musicscore2
===========
**musicscore2** is a python library to generate musicxml data in an intuitive and easy but nevertheless comprehensive way. The generated
files can be imported in several music notation programs and be processed further if necessary. The preferred software is Finale which
seems at the moment to have the best implementation of musicxml format files and supports the newest version 4.0.

**musicscore2** consists of two main packages: **musicxml** and **musictree**:

musicxml
========
The central class of this package is the :obj:`~musicxml.xmlelement.xmlelement.XMLElement` class. Each :obj:`~musicxml.xmlelement.xmlelement
.XMLElement` class must set its `type_` to a `XSDComplexType` which corresponds to xml scheme element complexType and controls the behavior of :obj:`~musicxml.xmlelement.xmlelement.XMLElement` in a comprehensive way. To be able to make full use of
OOP, all xsd information nodes (simpleType, complexType, group, attributeGroup) are wrapped automatically into XSDTreeElement classes (
XSDComplexType, XSDSimpleType, XSDGroup, XSDAttributeGroup) which themselves have a class attribute named XSD_TREE. XSD_TREE of type XSDTree
is only a small step away from the raw xsd information specified for each xml element in the musicxml.xsd file. XSDTree is a convenient
TreeRepresentation of each xsd element node which needs to receive the corresponding xsd information as a xml.tree.ElementTree.Element,
easily extracted after reading musicxml.xsd file into a root element of the same type.

How does it work?
-----------------
Each xml element can be used in a musicxml structure corresponding exactly to musicxml.xsd. For doing so the XMLElement is initiated
using a corresponding XSDComplexType or XSDSimpleType as its TYPE.


musictree
=========
The goal of this package is to simplify the use of musicxml elements. The tree structure of a score plays a very important role
and is being controlled via :obj:`~musictree.musictree.MusicTree` class. Some of the objects in this hierarchy are closely connected to the
corresponding objects in musicxml package and are descendents of  :obj:`~musictree.xmlwarpper.XMLWrapper` class with an ``~musictree
.xmlwarpper.XMLWrapper.xml_object`
attribute. There are although some fundamental differences between these two packages:

#. :obj:`musictree.score.Score` is the root of a musictree.
    - It is the parent of :obj:`musictree.part.Part`
    - It creates all necessary defaults:
        - Default layout objects inside the default can be changed directly via following properties:
            - scaling :obj:`musictree.layout.Scaling`
            - page_layout :obj:`musictree.layout.PageLayout`
            - system_layout :obj:`musictree.layout.StaffLayout`
            - staff_layout' :obj:`musictree.layout.StaffLayout`
    - :obj:`~musictree.score.Score.export_xml` method can be used to create the "end product" as a xml file.


#. :obj:`musictree.part.Part` is the first layer of a musictree.
    - It is the parent of :obj:`musictree.measure.Measure`
    - It must have a unique `id` during initialization. If no name is associated with the part its id will be used as its name.
    - Its method :obj:`~musictree.part.Part.add_measure()` can be used to conveniently add measures. It accepts two arguments:
        - ``number`` can be used to set the measure number. If ``None`` measure's number will be added automatically as one number higher
          than the previous measure (or 1 for the first measure).
        - ``time`` can be used to set the time signature. If ``None`` the previous time signature is adopted and set to hidden. The
          time signature of the first measure with time ``None`` is set to 4/4.


#. :obj:`musictree.measure.Measure` is the second layer of a musictree.
    - It is the parent of :obj:`musictree.staff.Staff`
        - :obj:`musictree.time.Time`
        - :obj:`musictree.clef.Clef`
        - :obj:`musictree.key.Key`

#. :obj:`musictree.staff.Staff` is the third layer of a musictree.
    - It is the parent of :obj:`musictree.voice.Voice`

#. :obj:`musictree.voice.Voice` is the fourth layer of a musictree.
    - It is the parent of :obj:`musictree.beat.Beat`

#. :obj:`musictree.beat.Beat` is the fifth layer of a musictree.
    - It is the parent of :obj:`musictree.chord.Chord`

#. :obj:`musictree.chord.Chord` is the sixth layer of a musictree.
    - It is the parent of :obj:`musictree.note.Note`
        - :obj:`musictree.dynamics.Dynamics`

#. :obj:`musictree.note.Note` is the seventh layer of a musictree.
    - It is the parent of :obj:`musictree.midi.Midi`

#. :obj:`musictree.midi.Midi` is the eighth layer of a musictree.
    - It is the parent of :obj:`musictree.accidental.Accidental`

#. :obj:`musictree.accidental.Accidental` is the ninth layer of a musictree.

QuarterDuration non-writables and quantizing
--------------------------------------------

- :obj:`musictree.quarterduration.QuarterDuration`

Layout
------

- :obj:`musictree.layout.Scaling`
- :obj:`musictree.layout.PageLayout`
- :obj:`musictree.layout.StaffLayout`
- :obj:`musictree.layout.StaffLayout`



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
