import simplejson as json

from musicscore.musicstream.jsoninterface.chorddict import ChordDict
from musicscore.musicstream.streamvoice import SimpleFormat


class JsonInterface(object):
    def __init__(self, jason_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chord_dicts = []
        self._json_object = None
        self.json_object = jason_object


    @property
    def json_object(self):
        return self._json_object

    @json_object.setter
    def json_object(self, val):
        self._json_object = json.loads(str(val))
        self._set_chord_dicts()

    def _set_chord_dicts(self):
        self._chord_dicts = []
        for x in self.json_object:
            self._chord_dicts.append(ChordDict(x))

    def get_simple_format(self):
        sf = SimpleFormat()
        for chd in self._chord_dicts:
            sf.add_chord(chd.get_chord())
        return sf
