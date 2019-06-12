class LinkAttributes(object):
    """
	<xs:attributeGroup name="link-attributes">
		<xs:annotation>
			<xs:documentation>The link-attributes group includes all the simple XLink attributes supported in the MusicXML format.
			</xs:documentation>
		</xs:annotation>
		<!--<xs:attribute ref="xmnls:xlink" fixed="http://www.w3.org/1999/xlink"/>-->
		<xs:attribute ref="xlink:href" use="required"/>
		<xs:attribute ref="xlink:type" fixed="simple"/>
		<xs:attribute ref="xlink:role"/>
		<xs:attribute ref="xlink:title"/>
		<xs:attribute ref="xlink:show" default="replace"/>
		<xs:attribute ref="xlink:actuate" default="onRequest"/>
	</xs:attributeGroup>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        NotImplementedError()
