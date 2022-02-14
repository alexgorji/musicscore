from musicxml.xmlelement.xmlelement import XMLF, XMLFf, XMLFff, XMLFfff, XMLFffff, XMLFfffff, XMLFp, XMLFz, XMLMf, XMLMp, XMLP, XMLPf, \
    XMLPp, XMLPpp, XMLPppp, XMLPpppp, XMLPppppp, XMLRf, XMLRfz, XMLSf, XMLSffz, XMLSfp, XMLSfpp, XMLSfz, XMLSfzp

from musictree.xmlwrapper import XMLWrapper

# DYNAMICS = {"f": {'class': XMLF, "sound": 100},
#             "ff": {"class": XMLFf, "sound": 111},
#             "fff": {"class": XMLFff, "sound": 122},
#             "ffff": {"class": XMLFfff, "sound": 133},
#             "fffff": {"class": XMLFffff, "sound": 138},
#             "ffffff": {"class": XMLFfffff, "sound": 141},
#             "fp": {"class": XMLFp, "sound": None},
#             "fz": {"class": XMLFz, "sound": None},
#             "mf": {"class": XMLMf, "sound": 84},
#             "mp": {"class": XMLMp, "sound": 70},
#             "p": {"class": XMLP, "sound": 55},
#             "pf": {"class": XMLPf, "sound": None},
#             "pp": {"class": XMLPp, "sound": 41},
#             "ppp": {"class": XMLPpp, "sound": 27},
#             "pppp": {"class": XMLPppp, "sound": 11},
#             "ppppp": {"class": XMLPpppp, "sound": 6},
#             "pppppp": {"class": XMLPppppp, "sound": 1},
#             "rf": {"class": XMLRf, "sound": None},
#             "rfz": {"class": XMLRfz, "sound": None},
#             "sf": {"class": XMLSf, "sound": None},
#             "sffz": {"class": XMLSffz, "sound": None},
#             "sfp": {"class": XMLSfp, "sound": None},
#             "sfpp": {"class": XMLSfpp, "sound": None},
#             "sfz": {"class": XMLSfz, "sound": None},
#             "sfzp": {"class": XMLSfzp, "sound": None},
#             }
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
