.. musicscore2 documentation master file, created by
   sphinx-quickstart on Tue Feb 22 11:32:10 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to musicscore2's documentation!
=======================================

**musicscore2** is a library consisting of two packages: **musicxml** and **musictree**.

musicxml
--------
The central class of this library is the `XMLElement` class. Each `XMLElement` class must set its `type_` to a `XSDComplexType` which
corresponds to xml scheme element complexType and controls the behavior of `XMLElement` in a comprehensive way. To be able to make full use of
OOP, all xsd information nodes (simpleType, complexType, group, attributeGroup) are wrapped automatically into XSDTreeElement classes (
XSDComplexType, XSDSimpleType, XSDGroup, XSDAttributeGroup) which themselves have a class attribute named XSD_TREE. XSD_TREE of type XSDTree
is only a small step away from the raw xsd information specified for each xml element in the musicxml.xsd file. XSDTree is a convenient
TreeRepresentation of each xsd element node which needs to receive the corresponding xsd information as a xml.tree.ElementTree.Element,
easily extracted after reading musicxml.xsd file into a root element of the same type.

`musicxml.xsd` ==> root of type `xml.tree.ElementTree.Element` (`ET.Element`) represents this file completely (see `musixml.util.core`) ==> each
xsd node or element can be found using the findall method of `ET.Element` searching for tags like simpleType, complexType etc. (see
musicxml.types.simpletype, musicxml.types.complextype etc.) ==> XSDTree(ET.Element) (see musicxml.xsdtree) can deliver all needed
information to create a ==> XSDTreeElement (like XSDSimpleType or XSDComplexType classes) ==>  An XMLElement (see musicxml.xmlelement) can
now be initiated using a XSDComplexType (for example XMLElement(type_=XSDComplexTypeOffset, value=-2, attributes={'sound': 'yes'})) and be
used in a musicxml structure corresponding exactly to musicxml.xsd.

musictree
---------


.. note::

   This project is under active development.

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Contents
--------

.. toctree::

   usage
   musictree