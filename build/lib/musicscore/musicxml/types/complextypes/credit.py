from musicscore.dtd.dtd import Sequence, Element, Choice
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.bookmark import ComplexTypeBookmark
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.formattedsymbolid import ComplexTypeFormattedSymbolId
from musicscore.musicxml.types.complextypes.formattedtextid import ComplexTypeFormattedTextId
from musicscore.musicxml.types.complextypes.image import ComplexTypeImage
from musicscore.musicxml.types.complextypes.link import ComplexTypeLink
from musicscore.musicxml.types.simple_type import String


class CreditType(XMLElement, String):
    _TAG = 'credit-type'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Link(ComplexTypeLink):
    _TAG = 'link'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Bookmark(ComplexTypeBookmark):
    _TAG = 'bookmark'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class CreditImage(ComplexTypeImage):
    _TAG = 'credit-image'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class CreditWords(ComplexTypeFormattedTextId):
    _TAG = 'credit-words'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class CreditSymbol(ComplexTypeFormattedSymbolId):
    _TAG = 'credit-symbol'

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Page(AttributeAbstract):

    def __init__(self, page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('page', page, "PositiveInteger")


class ComplexTypeCredit(ComplexType, Page, OptionalUniqueId):
    """The credit type represents the appearance of the title, composer, arranger, lyricist, copyright, dedication, and
    other text, symbols, and graphics that commonly appear on the first page of a score. The credit-words,
    credit-symbol, and credit-image elements are similar to the words, symbol, and image elements for directions.
    However, since the credit is not part of a measure, the default-x and default-y attributes adjust the origin
    relative to the bottom left-hand corner of the page. The enclosure for credit-words and credit-symbol is none
    by default.

    By default, a series of credit-words and credit-symbol elements within a single credit element follow one another
    in sequence visually. Non-positional formatting attributes are carried over from the previous element by default.

    The page attribute for the credit element specifies the page number where the credit should appear. This is an
    integer value that starts with 1 for the first page. Its value is 1 by default. Since credits occur before the
    music, these page numbers do not refer to the page numbering specified by the print element's page-number attribute.

    The credit-type element indicates the purpose behind a credit. Multiple types of data may be combined in a single
    credit, so multiple elements may be used. Standard values include page number, title, subtitle, composer, arranger,
    lyricist, and rights."""
    _DTD = Sequence(
        Element(CreditType, min_occurrence=0, max_occurrence=None),
        Element(Link, min_occurrence=0, max_occurrence=None),
        Element(Bookmark, min_occurrence=0, max_occurrence=None),
        Choice(
            Element(CreditImage),
            Sequence(
                Choice(
                    Element(CreditWords),
                    Element(CreditSymbol)
                ),
                # Sequence(
                #     Element(Link, min_occurrence=0, max_occurrence=None),
                #     Element(Bookmark, min_occurrence=0, max_occurrence=None),
                #     Choice(
                #         Element(CreditWords),
                #         Element(CreditSymbol)
                #     ),
                #     min_occurrence=0,
                #     max_occurrence=None,
                # )
            )

        )
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
