Examples
********

All example files can be found on GitHub under https://github.com/alexgorji/musicscore2/tree/master/docs/examples

Hello World (1)
---------------

  In this example one note is added to score step by step. At first you need to install musicscore2 (s. :doc:`usage`).
  After that follow the steps to create a simple musicxml file:

   #. import :obj:`musictree.score.Score`, :obj:`musictree.part.Part`, :obj:`musictree.measure.Measure`,
      :obj:`musictree.staff.Staff`, :obj:`musictree.voice.Voice`, :obj:`musictree.beat.Beat` and
      :obj:`musictree.chord.Chord`.

      Alternatively you can import all classes via ``from musictree import *``

   #. Create a :obj:`~musictree.score.Score`

       .. code-block::

          s = Score()

   #. Create and add a :obj:`~musictree.part.Part` to score. For creating a :obj:`~musictree.part.Part` object you
      have to pass a unique ``id`` (see :obj:`~musicxml.xsd.xsdsimpletype.XSDSimpleTypeIDREF` for further
      information) during initialization. If no ``name`` is set, part uses ``id`` as its ``name``.

       .. code-block::

          p = s.add_child(Part('P1', name='Part 1'))

   #. Create and add a :obj:`~musictree.measure.Measure` to part. ``number`` is required during initializing a measure
      object. Alternatively you can use part's method obj:`~musictree.part.Part.add_measure()` which takes care of
      number attribute and creates measure with the same :obj:`~musictree.key.Key` and :obj:`~musictree.time.Time`.
      It is also possible to add chord directly to part via :obj:`~musictree.part.Part.add_chord()` method. (s. next
      example).

       .. code-block::

          m = p.add_child(Measure(number=1))

   #. Create and add a :obj:`~musictree.staff.Staff` to measure.
      Alternatively you could use :obj:`~musictree.measure.Measure.add_staff()`. Measure has also other useful
      shortcut methods like :obj:`~musictree.measure.Measure.add_voice()`.


       .. code-block::

          st = m.add_child(Staff(number=1))

   #. Create and add a :obj:`~musictree.voice.Voice` to staff.
      Alternatively you could use staff's :obj:`~musictree.staff.Staff.add_voice()`.

       .. code-block::

          v = st.add_child(Voice(number=1))

   #. Create and add four :obj:`~musictree.beat.Beat` s with quarter_duration 1 to voice. (As alternative we can call
      :obj:`~musictree.voice.Voice.update_beats()` to add beets according to measure's time signature. Default value is 4/4.)

       .. code-block::

          for _ in range(4):
             v.add_child(Beat(quarter_duration=1))

   #. Select the first beat, create and add a :obj:`~musictree.chord.Chord` with midi value 60 (C4) and quarter duration 4 to this beat.

       .. code-block::

          beat = v.get_children()[0]
          beat.add_child(Chord(60, 4))

   #. Use score's :obj:`~musictree.score.Score.export_xml()` to generate a xml file. An absolute path for the file
      (with ``xml`` extension) must must be passed as a parameter to this method. In this example we use the
      `pathlib` library to get the path of the python file in which the code lives and change its extension from .py
      to .xml. You could use also ``os.path`` or even a hardcoded path as string (not really recommended).

       .. code-block::

          xml_path = Path(__file__).with_suffix('.xml')
          s.export_xml(xml_path)

   #. You have created your first xml file with musicscore2. Congrats! Now you can open it with a notation software
      and enjoy the sight ;-)

Hello World (2)
---------------

  In this example one note is added to score using part's :obj:`~musictree.part.Part.add_chord()` method. This method
  takes care of creating and adding all needed objects. The result is exactly the same as in ``Hello World (1)``

   #. Create a :obj:`~musictree.score.Score`

       .. code-block::

          s = Score()

   #. Create and add a :obj:`~musictree.part.Part` to score.

       .. code-block::

          p = s.add_child(Part('P1', name='Part 1'))

   #. Create and add a :obj:`~musictree.chord.Chord` with midi value 60 (C4) and quarter duration 4 as chord to the part
      (:obj:`~musictree.part.Part.add_chord()`).

       .. code-block::

          p.add_chord(Chord(60, 4))

   #. Use :obj:`~musictree.score.Score.export_xml()` to generate a xml file. An absolute path for the file (with
      ``xml`` extension) must be passed as a parameter to this method.

       .. code-block::

          xml_path = Path(__file__).with_suffix('.xml')
          s.export_xml(xml_path)