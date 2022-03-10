from musicxml.xmlelement.xmlelement import XMLF, XMLFf, XMLFff, XMLFfff, XMLFffff, XMLFfffff, XMLFp, XMLFz, XMLMf, XMLMp, XMLP, XMLPf, \
    XMLPp, XMLPpp, XMLPppp, XMLPpppp, XMLPppppp, XMLRf, XMLRfz, XMLSf, XMLSffz, XMLSfp, XMLSfpp, XMLSfz, XMLSfzp

from musictree.xmlwrapper import XMLWrapper

__all__ = ['DYNAMICS', 'Dynamics']

#:
DYNAMICS = {"f": XMLF,
            "ff": XMLFf,
            "fff": XMLFff,
            "ffff": XMLFfff,
            "fffff": XMLFffff,
            "ffffff": XMLFfffff,
            "fp": XMLFp,
            "fz": XMLFz,
            "mf": XMLMf,
            "mp": XMLMp,
            "p": XMLP,
            "pf": XMLPf,
            "pp": XMLPp,
            "ppp": XMLPpp,
            "pppp": XMLPppp,
            "ppppp": XMLPpppp,
            "pppppp": XMLPppppp,
            "rf": XMLRf,
            "rfz": XMLRfz,
            "sf": XMLSf,
            "sffz": XMLSffz,
            "sfp": XMLSfp,
            "sfpp": XMLSfpp,
            "sfz": XMLSfz,
            "sfzp": XMLSfzp,
            }


class Dynamics(XMLWrapper):
    """
    This is a simple wrapper for dynamics objects. Value must be a key in :obj:`DYNAMICS`.
    """

    def __init__(self, value: str, *args, **kwargs):
        super().__init__()
        self.XMLClass = DYNAMICS[value]
        self._xml_object = self.XMLClass(*args, **kwargs)
