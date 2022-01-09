# NameChar ::= Letter | Digit | '.' | '-' | '_' | ':' | CombiningChar | Extender
# Letter ::= BaseChar | Ideographic
# Extender ::= · | ː | ˑ | · | ـ | ๆ | ໆ | 々 | [〱-〵] | [ゝ-ゞ] | [ー-ヾ]
# CombiningChar ::= [̀-ͅ] | [͠-͡] | [҃-҆] | [֑-֡] | [֣-ֹ] | [ֻ-ֽ] | ֿ | [ׁ-ׂ] | ׄ | [ً-ْ] | ٰ | [ۖ-ۜ] | [۝-۟] | [۠-ۤ] | [ۧ-ۨ] | [۪-ۭ] | [ँ-ः]
# | ़ | [ा-ौ] | ् | [॑-॔] | [ॢ-ॣ] | [ঁ-ঃ] | ় | া | ি | [ী-ৄ] | [ে-ৈ] | [ো-্] | ৗ | [ৢ-ৣ] | ਂ | ਼ | ਾ | ਿ |
# [ੀ-ੂ] | [ੇ-ੈ] | [ੋ-੍] | [ੰ-ੱ] | [ઁ-ઃ] | ઼ | [ા-ૅ] | [ે-ૉ] | [ો-્] | [ଁ-ଃ] | ଼ | [ା-ୃ] | [େ-ୈ] | [ୋ-୍] |
# [ୖ-ୗ] | [ஂ-ஃ] | [ா-ூ] | [ெ-ை] | [ொ-்] | ௗ | [ఁ-ః] | [ా-ౄ] | [ె-ై] | [ొ-్] | [ౕ-ౖ] | [ಂ-ಃ] | [ಾ-ೄ]
# | [ೆ-ೈ] | [ೊ-್] | [ೕ-ೖ] | [ം-ഃ] | [ാ-ൃ] | [െ-ൈ] | [ൊ-്] | ൗ | ั | [ิ-ฺ] | [็-๎] | ັ | [ິ-ູ] | [ົ-ຼ] | [່-ໍ] |
# [༘-༙] | ༵ | ༷ | ༹ | ༾ | ༿ | [ཱ-྄] | [྆-ྋ] | [ྐ-ྕ] | ྗ | [ྙ-ྭ] | [ྱ-ྷ] | ྐྵ | [⃐-⃜] | ⃡ | [〪-〯] | ゙ | ゚

name_character = "[-.0-9:A-Z_a-z\u00B7\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u037D\u037F-\u1FFF\u200C-\u200D\u203F\u2040\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]"
xml_name_first_character = "[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]"

name_character_without_colon = "[-.0-9A-Z_a-z\u00B7\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u037D\u037F-\u1FFF\u200C-\u200D\u203F\u2040\u2070" \
                               "-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]"
xml_name_first_character_without_colon = "[A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070" \
                                         "-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]"
