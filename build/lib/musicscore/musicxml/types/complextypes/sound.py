from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.mididevice import ComplexTypeMidiDevice
from musicscore.musicxml.types.complextypes.midiinstrument import ComplexTypeMidiInstrument
from musicscore.musicxml.types.complextypes.offset import ComplexTypeOffset
from musicscore.musicxml.types.complextypes.play import ComplexTypePlay


class Tempo(AttributeAbstract):
    def __init__(self, tempo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('tempo', tempo, 'TypeNonNegativeDecimal')


class Dynamics(AttributeAbstract):
    def __init__(self, dynamics=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('dynamics', dynamics, 'TypeNonNegativeDecimal')


class Dacapo(AttributeAbstract):
    def __init__(self, dacapo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('dacapo', dacapo, 'TypeYesNo')


class Segno(AttributeAbstract):
    def __init__(self, segno=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('segno', segno, 'Token')


class Dalsegno(AttributeAbstract):
    def __init__(self, dalsegno=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('dalsegno', dalsegno, 'Token')


class Coda(AttributeAbstract):
    def __init__(self, coda=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('coda', coda, 'Token')


class Tocoda(AttributeAbstract):
    def __init__(self, tocoda=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('tocoda', tocoda, 'Token')


class Divisions(AttributeAbstract):
    def __init__(self, divisions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('divisions', divisions, 'TypeDivisions')


class ForwardRepeat(AttributeAbstract):
    def __init__(self, forward_repeat=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('forward-repeat', forward_repeat, 'TypeYesNo')


class Fine(AttributeAbstract):
    def __init__(self, fine=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('fine', fine, 'Token')


class TimeOnly(AttributeAbstract):
    def __init__(self, time_only=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('time-only', time_only, 'TypeTimeOnly')


class Pizzicato(AttributeAbstract):
    def __init__(self, pizzicato=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('pizzicato', pizzicato, 'TypeYesNo')


class Pan(AttributeAbstract):
    def __init__(self, pan=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('pan', pan, 'TypeRotationDegrees')


class Elevation(AttributeAbstract):
    def __init__(self, elevation=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('elevation', elevation, 'TypeRotationDegrees')


class DamperPedal(AttributeAbstract):
    def __init__(self, damper_pedal=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('damper-pedal', damper_pedal, 'TypeYesNoNumber')


class SoftPedal(AttributeAbstract):
    def __init__(self, soft_pedal=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('soft-pedal', soft_pedal, 'TypeYesNoNumber')


class SostenutoPedal(AttributeAbstract):
    def __init__(self, sostenuto_pedal=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('sostenuto-pedal-pedal', sostenuto_pedal, 'TypeYesNoNumber')


class MidiDevice(ComplexTypeMidiDevice):
    _TAG = 'midi-device'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class MidiInstrument(ComplexTypeMidiInstrument):
    _TAG = 'midi-instrument'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Play(ComplexTypePlay):
    _TAG = 'play'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Offset(ComplexTypeOffset):
    _TAG = 'offset'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeSound(ComplexType, Tempo, Dynamics, Dacapo, Segno, Dalsegno, Coda, Tocoda, Divisions, ForwardRepeat,
                       Fine, TimeOnly, Pizzicato, Pan, Elevation, DamperPedal, SoftPedal, SostenutoPedal,
                       OptionalUniqueId):
    """The sound element contains general playback parameters. They can stand alone within a part/measure, or be a
    component element within a direction.

    Tempo is expressed in quarter notes per minute. If 0, the sound-generating program should prompt the user at the
    time of compiling a sound (MIDI) file.

    Dynamics (or MIDI velocity) are expressed as a percentage of the default forte value (90 for MIDI 1.0).

    Dacapo indicates to go back to the beginning of the movement. When used it always has the value "yes".

    Segno and dalsegno are used for backwards jumps to a segno sign; coda and tocoda are used for forward jumps to a
    coda sign. If there are multiple jumps, the value of these parameters can be used to name and distinguish them. If
    segno or coda is used, the divisions attribute can also be used to indicate the number of divisions per quarter
    note. Otherwise sound and MIDI generating programs may have to recompute this.

    By default, a dalsegno or dacapo attribute indicates that the jump should occur the first time through, while a
    tocoda attribute indicates the jump should occur the second time through. The time that jumps occur can be changed
    by using the time-only attribute.

    Forward-repeat is used when a forward repeat sign is implied, and usually follows a bar line. When used it always
    has the value of "yes".

    The fine attribute follows the final note or rest in a movement with a da capo or dal segno direction. If numeric,
    the value represents the actual duration of the final note or rest, which can be ambiguous in written notation and
    different among parts and voices. The value may also be "yes" to indicate no change to the final duration.

    If the sound element applies only particular times through a repeat, the time-only attribute indicates which times
    to apply the sound element.

    Pizzicato in a sound element effects all following notes. Yes indicates pizzicato, no indicates arco.

    The pan and elevation attributes are deprecated in Version 2.0. The pan and elevation elements in the midi-
    instrument element should be used instead. The meaning of the pan and elevation attributes is the same as for the
    pan and elevation elements. If both are present, the mid-instrument elements take priority.

    The damper-pedal, soft-pedal, and sostenuto-pedal attributes effect playback of the three common piano pedals and
    their MIDI controller equivalents. The yes value indicates the pedal is depressed; no indicates the pedal is
    released. A numeric value from 0 to 100 may also be used for half pedaling. This value is the percentage that the
    pedal is depressed. A value of 0 is equivalent to no, and a value of 100 is equivalent to yes.

    MIDI devices, MIDI instruments, and playback techniques are changed using the midi-device, midi-instrument, and play
    elements. When there are multiple instances of these elements, they should be grouped together by instrument using
    the id attribute values.

    The offset element is used to indicate that the sound takes place offset from the current score position. If the
    sound element is a child of a direction element, the sound offset element overrides the direction offset element if
    both elements are present. Note that the offset reflects the intended musical position for the change in sound. It
    should not be used to compensate for latency issues in particular hardware configurations."""

    _DTD = Sequence(
        Sequence(
            Element(MidiDevice, min_occurrence=0),
            Element(MidiInstrument, min_occurrence=0),
            Element(Play, min_occurrence=0),
            min_occurrence=0,
            max_occurrence=None
        ),
        Element(Offset, min_occurrence=0)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, * args, **kwargs)
