
**musicscore2** is a python library to generate musicxml data in an intuitive and easy but nevertheless comprehensive way. The generated
files can be imported in several music notation programs and be processed further if necessary. The preferred software is Finale which
seems at the moment to have the best implementation of musicxml format files and supports the newest version 4.0.

As dependency **musicscore2** needs the **musicxml** library. Its xml classes which are closely designed in relation to musicxml
schemes (4.0) are used to generate xml partials as strings.

musicxml
========

The central class of this library is the :obj:`~musicxml.xmlelement.xmlelement.XMLElement` class. Each :obj:`~musicxml.xmlelement.xmlelement.XMLElement` class must set its `type_` to a `XSDComplexType` which corresponds to xml scheme element complexType and controls the behavior of :obj:`~musicxml.xmlelement.xmlelement.XMLElement` in a comprehensive way. To be able to make full use of
OOP, all xsd information nodes (simpleType, complexType, group, attributeGroup) are wrapped automatically into XSDTreeElement classes (
XSDComplexType, XSDSimpleType, XSDGroup, XSDAttributeGroup) which themselves have a class attribute named XSD_TREE. XSD_TREE of type XSDTree
is only a small step away from the raw xsd information specified for each xml element in the musicxml.xsd file. XSDTree is a convenient
TreeRepresentation of each xsd element node which needs to receive the corresponding xsd information as a xml.tree.ElementTree.Element,
easily extracted after reading musicxml.xsd file into a root element of the same type.

How does it work?
-----------------
Each xml element can be used in a musicxml structure corresponding exactly to musicxml.xsd. For doing so the XMLElement is initiated
using a corresponding XSDComplexType or XSDSimpleType as its TYPE

musicxml.xsd ==> root of type ``xml.tree.ElementTree.Element`` (`ET.Element`) represents this file completely (see musixml.util.core) ==> each
xsd node or element can be found using the findall method of `ET.Element` searching for tags like simpleType, complexType etc. (see
musicxml.types.simpletype, musicxml.types.complextype etc.) ==> XSDTree(ET.Element) (see musicxml.xsdtree) can deliver all needed 
information to create a ==> XSDTreeElement (like XSDSimpleType or XSDComplexType classes) ==>  An XMLElement (see musicxml.xmlelement) can 
now be initiated using a XSDComplexType (for example XMLElement(type_=XSDComplexTypeOffset, value=-2, attributes={'sound': 'yes'})) and be 
used in a musicxml structure corresponding exactly to musicxml.xsd.

