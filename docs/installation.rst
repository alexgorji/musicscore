Installation
============

.. warning::
   This documentation is still under construction!


Requires Python 3.11 or newer.

musicscore
**********

1. Check the version of python on your computer: `python \--version`. This library requires ``python 3.11`` or newer. Possibly you
have to install a supported version on your system (for example via Homebrew or whatever way you choose.)

2. Make a new folder and create a virtual environment for your project and install musicscore via pip:
    * mkdir <project>
    * cd <project>
    * python3 -m venv venv
    * source venv/bin/activate
    * pip install --upgrade pip

.. code-block:: console

    (.venv) $ pip install musicscore

musicxml
********

**musicscore** depends heavily on the library **musicxml** which allows an object oriented and comprehensive approach to MusicXML format. **musicxml** can also be found in a separate repository under: `<https://github.com/alexgorji/musicxml>`__ and be installed separately via pip:

.. code-block:: console

    (.venv) $ pip install musicxml