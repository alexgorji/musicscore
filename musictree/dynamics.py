from musicxml.xmlelement.xmlelement import XMLF, XMLFf, XMLFff, XMLFfff, XMLFffff, XMLFfffff, XMLFp, XMLFz, XMLMf, XMLMp, XMLP, XMLPf, \
    XMLPp, XMLPpp, XMLPppp, XMLPpppp, XMLPppppp, XMLRf, XMLRfz, XMLSf, XMLSffz, XMLSfp, XMLSfpp, XMLSfz, XMLSfzp

from musictree.xmlwrapper import XMLWrapper

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

    def __init__(self, value, *args, **kwargs):
        super().__init__()
        dynamics_class = DYNAMICS[value]
        self._xml_object = dynamics_class(*args, **kwargs)
