
class XSDSimpleTypeFontSize(XSDSimpleType):
    _UNION = [XSDSimpleTypeCssFontSize, XSDSimpleTypeDecimal]
    """The font-size can be one of the CSS font sizes (xx-small, x-small, small, medium, large, x-large, xx-large) or a numeric point size."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="font-size">
    <xs:annotation>
        <xs:documentation>The font-size can be one of the CSS font sizes (xx-small, x-small, small, medium, large, x-large, xx-large) or a numeric point size.</xs:documentation>
    </xs:annotation>
    <xs:union memberTypes="xs:decimal css-font-size" />
</xs:simpleType>
"""
                                     ))


class XSDSimpleTypeYesNoNumber(XSDSimpleType):
    _UNION = [XSDSimpleTypeYesNo, XSDSimpleTypeDecimal]
    """The yes-no-number type is used for attributes that can be either boolean or numeric values."""

    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="yes-no-number">
    <xs:annotation>
        <xs:documentation>The yes-no-number type is used for attributes that can be either boolean or numeric values.</xs:documentation>
    </xs:annotation>
    <xs:union memberTypes="yes-no xs:decimal" />
</xs:simpleType>
"""
                                     ))

class XSDSimpleTypePositiveIntegerOrEmpty(XSDSimpleTypePositiveInteger):
    """The positive-integer-or-empty values can be either a positive integer or an empty string."""
    _FORCED_PERMITTED = ['']
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="positive-integer-or-empty">
    <xs:annotation>
        <xs:documentation>The positive-integer-or-empty values can be either a positive integer or an empty string.</xs:documentation>
    </xs:annotation>
    <xs:union memberTypes="xs:positiveInteger">
        <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:enumeration value="" />
            </xs:restriction>
        </xs:simpleType>
    </xs:union>
</xs:simpleType>
"""
                                     ))

    def __init__(self, value='', *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class XSDSimpleTypeNumberOrNormal(XSDSimpleTypeDecimal):
    """The number-or-normal values can be either a decimal number or the string "normal". This is used by the line-height and letter-spacing attributes."""
    _FORCED_PERMITTED = ['normal']
    XSD_TREE = XSDTree(ET.fromstring("""
<xs:simpleType xmlns:xs="http://www.w3.org/2001/XMLSchema" name="number-or-normal">
    <xs:annotation>
        <xs:documentation>The number-or-normal values can be either a decimal number or the string "normal". This is used by the line-height and letter-spacing attributes.</xs:documentation>
    </xs:annotation>
    <xs:union memberTypes="xs:decimal">
        <xs:simpleType>
            <xs:restriction base="xs:token">
                <xs:enumeration value="normal" />
            </xs:restriction>
        </xs:simpleType>
    </xs:union>
</xs:simpleType>
"""
                                     ))
