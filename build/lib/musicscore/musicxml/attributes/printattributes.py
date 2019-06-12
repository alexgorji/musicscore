'''
    <xs:attributeGroup name="print-attributes">
        <xs:annotation>

            </xs:documentation>
        </xs:annotation>
        <xs:attribute name="staff-spacing" type="tenths"/>
        <xs:attribute name="new-system" type="yes-no"/>
        <xs:attribute name="new-page" type="yes-no"/>
        <xs:attribute name="blank-page" type="xs:positiveInteger"/>
        <xs:attribute name="page-number" type="xs:token"/>
    </xs:attributeGroup>
'''

from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class StaffSpacing(AttributeAbstract):
    """"""

    def __init__(self, staff_spacing=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('staff-spacing', staff_spacing, "TypeTenths")


class NewSystem(AttributeAbstract):
    """"""

    def __init__(self, new_system=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('new-system', new_system, "TypeYesNo")


class NewPage(AttributeAbstract):
    """"""

    def __init__(self, new_page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('new-page', new_page, "TypeYesNo")


class BlankPage(AttributeAbstract):
    """"""

    def __init__(self, blank_page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('blank-page', blank_page, "PositiveInteger")


class PageNumber(AttributeAbstract):
    """"""

    def __init__(self, page_number=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('page-number', page_number, "Token")



class PrintAttributes(StaffSpacing, NewSystem, NewPage, BlankPage, PageNumber):
    """
    The print-attributes group is used by the print element. The new-system and new-page attributes indicate whether to 
    force a system or page break, or to force the current music onto the same system or page as the preceding music. 
    Normally this is the first music data within a measure. If used in multi-part music, they should be placed in the 
    same positions within each part, or the results are undefined. The page-number attribute sets the number of a new 
    page; it is ignored if new-page is not "yes". Version 2.0 adds a blank-page attribute. This is a positive integer 
    value that specifies the number of blank pages to insert before the current measure. It is ignored if new-page is 
    not "yes". These blank pages have no music, but may have text or images specified by the credit element. This is 
    used to allow a combination of pages that are all text, or all text and images, together with pages of music.

    The staff-spacing attribute specifies spacing between multiple staves in tenths of staff space. This is deprecated 
    as of Version 1.1; the staff-layout element should be used instead. If both are present, the staff-layout values 
    take priority.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
