* Create one instance of XMLScore
    * ElementPath.py (388) find called 1x
    * ElementPath.py (260) select called 2x
    * ElementPath.py (133) select called 476x !
    * ElementPath.py (197) select_child called 4023x !!!

      ...

    * builtins.isinstance 4111x !!!

      ...

    * xml.etree.ElementTree.Element.get 475x!!!

* What is happening exactly in line 197 of ElementPath.py?

.. code:: python

   def prepare_descendant(next, token):
        try:
            token = next()
        except StopIteration:
            return
        if token[0] == "*":
            tag = "*"
        elif not token[0]:
            tag = token[1]
        else:
            raise SyntaxError("invalid descendant")

        if _is_wildcard_tag(tag):
            select_tag = _prepare_tag(tag)
            def select(context, result):
                def select_child(result):
                    for elem in result:
                        for e in elem.iter():
                            if e is not elem:
                                yield e
                return select_tag(context, select_child(result))
        else:
            if tag[:2] == '{}':
                tag = tag[2:]  # '{}tag' == 'tag'
            def select(context, result):
                for elem in result:
                    for e in elem.iter(tag):
                        if e is not elem:
                            yield e
        return select


* select_child is an inner function of prepare_descendant() function. Nothing to do there, if we want to continue using xml.etree

* Create one instance of XMLLeftMargin
    * ElementPath.py (388) find called 1x
    * ElementPath.py (260) select called 4/3x??
    * ElementPath.py (133) select called 444x !
    * ElementPath.py (197) select_child called 3949x !!!

      ...

    * builtins.isinstance 3970x !!!

      ...

    * xml.etree.ElementTree.Element.get 444x!!!

* Each XMLElement class has to create its xsd_tree only once!
  * profile_tuplets reduced running time from 27.215 to 11.895 seconds! Big success.