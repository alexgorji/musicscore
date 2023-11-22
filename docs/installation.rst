Installation
============

.. warning::
   This documentation is still under construction!


Tested with python 3.9, 3.10 and 3.11

musicscore
**********

1. Check the version of python on your computer: `python \--version`. This library has been developed under ``python 3.9``. Possibly you
have to install this version or newer on your system (for example via Homebrew or whatever way you choose.)

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