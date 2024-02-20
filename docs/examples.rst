Examples
********

All example files can be found on GitHub under `examples <https://github.com/alexgorji/musicscore/tree/master/docs/examples>`_

.. seealso::
   `LilyPondUnofficialXMLTestSuite <https://github.com/alexgorji/musicscore/tree/master/musicscore/LilyPondUnofficialXMLTestSuite>`_, `MyXMLTestSuite <https://github.com/alexgorji/musicscore/tree/master/musicscore/MyXMLTestSuite>`_ and `unit/integrity tests <https://github.com/alexgorji/musicscore/tree/master/musicscore/tests>`_

Hello World (1)
---------------

  In this example one note is added to score step by step. At first you need to install musicscore (s. :doc:`installation`).
  After that follow the steps to create a simple musicxml file:

   #. import ``pathlib.Path and`` :obj:`musicscore.score.Score`, :obj:`musicscore.part.Part`, :obj:`musicscore.measure.Measure`,
      :obj:`musicscore.staff.Staff`, :obj:`musicscore.voice.Voice`, :obj:`musicscore.beat.Beat` and
      :obj:`musicscore.chord.Chord`.

       .. code-block::

          from pathlib import Path

          from musicscore.beat import Beat
          from musicscore.chord import Chord
          from musicscore.measure import Measure
          from musicscore.part import Part
          from musicscore.score import Score
          from musicscore.staff import Staff
          from musicscore.voice import Voice

      Alternatively you can import all classes via ``from musicscore import *``
          .. code-block::

            from pathlib import Path
            from musicscore import *

   #. Create a :obj:`~musicscore.score.Score`

       .. code-block::

          s = Score(title="Hello World 1")

   #. Create and add a :obj:`~musicscore.part.Part` to score. For creating a :obj:`~musicscore.part.Part` object you
      have to pass a unique ``id`` (see :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF` for further
      information) during initialization. If no ``name`` is set, part uses ``id`` as its ``name``.

       .. code-block::

          p = s.add_child(Part('hw1', name='HW1'))

   #. Create and add a :obj:`~musicscore.measure.Measure` to part. ``number`` is required during initializing a measure
      object. Alternatively you can use part's method obj:`~musicscore.part.Part.add_measure()` which takes care of
      number attribute and creates measure with the same :obj:`~musicscore.key.Key` and :obj:`~musicscore.time.Time`.
      It is also possible to add chord directly to part via :obj:`~musicscore.part.Part.add_chord()` method. (s. next
      example).

       .. code-block::

          m = p.add_child(Measure(number=1))

   #. Create and add a :obj:`~musicscore.staff.Staff` to measure.
      Alternatively you could use :obj:`~musicscore.measure.Measure.add_staff()`. Measure has also other useful
      shortcut methods like :obj:`~musicscore.measure.Measure.add_voice()`.


       .. code-block::

          st = m.add_child(Staff(number=1))

   #. Create and add a :obj:`~musicscore.voice.Voice` to staff.
      Alternatively you could use staff's :obj:`~musicscore.staff.Staff.add_voice()`.

       .. code-block::

          v = st.add_child(Voice(number=1))

   #. Create and add four :obj:`~musicscore.beat.Beat` s with quarter_duration 1 to voice. (As alternative we can call
      :obj:`~musicscore.voice.Voice.update_beats()` to add beets according to measure's time signature. Default value is 4/4.)

       .. code-block::

          for _ in range(4):
             v.add_child(Beat(quarter_duration=1))

   #. Select the first beat, create and add a :obj:`~musicscore.chord.Chord` with midi value 60 (C4) and quarter duration 4 to this beat.

       .. code-block::

          beat = v.get_children()[0]
          beat.add_child(Chord(60, 4))

   #. Use score's :obj:`~musicscore.score.Score.export_xml()` to generate a xml file. An absolute path for the file
      (with ``xml`` extension) must must be passed as a parameter to this method. In this example we use the
      `pathlib` library to get the path of the python file in which the code lives and change its extension from .py
      to .xml. You could use also ``os.path`` or even a hardcoded path as string (not really recommended).

       .. code-block::

          xml_path = Path(__file__).with_suffix('.xml')
          s.export_xml(xml_path)

   #. Congrats! You have created your first xml file with musicscore. Now you can open it with a notation software
      and enjoy the sight ;-)

Hello World (2)
---------------

  In this example one note is added to score using part's :obj:`~musicscore.part.Part.add_chord()` method. This method
  takes care of creating and adding all needed objects. The result is exactly the same as in ``Hello World (1)``,
  except for the updated ``hw2``-related IDs and no ``<staff>1</staff>`` element associated with the note. The latter is
  not implicitly added by default via :obj:`~musicscore.part.Part.add_chord()`, and is unnecessary for single-part
  XMLs in general (refer to the `MusicXML documentation for staff elements <1_>`_).

  .. _1: https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/staff/

   #. Create a :obj:`~musicscore.score.Score`

       .. code-block::

          s = Score(title="Hello World 2")

   #. Create and add a :obj:`~musicscore.part.Part` to score.

       .. code-block::

          p = s.add_child(Part('hw2', name='HW2'))

   #. Create and add a :obj:`~musicscore.chord.Chord` with midi value 60 (C4) and quarter duration 4 as chord to the part
      (:obj:`~musicscore.part.Part.add_chord()`).

       .. code-block::

          p.add_chord(Chord(60, 4))

   #. Use :obj:`~musicscore.score.Score.export_xml()` to generate a xml file. An absolute path for the file (with
      ``xml`` extension) must be passed as a parameter to this method.

       .. code-block::

          xml_path = Path(__file__).with_suffix('.xml')
          s.export_xml(xml_path)