Step 1: virtualenv

  * open a Terminal (Mac —> Applications —> Utilities)
  * check if you have python3:
    * type in following command in Terminal: “which python3” 
    * if python3 is not installed, install it. (google it!)
  * check if you have pip3 
    * type in following command in Terminal: “which pip3”
    * if pip3 is not installed: https://pip.pypa.io/en/stable/installing
  * install virtualenv package 
    * pip3 install virtualenv
  * create the virtual environment
    * go to your desired path in Terminal
    * make a folder i.e. “testmusicscore” (“mkdir testmusicscore”)
    * change the path to testmusicscore (“cd testmusicscore”)
    * type in following command in Terminal: “virtualenv venv”
  * activate virtual environment
    * Mac OS / Linux
      * source venv/bin/activate
    * Windows
      * venv \Scripts\activate”

Step 2: install requirements

  * type in following command in Terminal:
    * pip3 install quicktions==1.9
    * pip3 install lxml==4.3.1

Step 3: install musicscore package (testversion)

  * type in following command in Terminal:
    *pip3 install --index-url https://test.pypi.org/simple/ --no-deps musicscore-alexgorji
  * To reinstall type in following command first in Terminal:
    * pip3 uninstall musicscore-alexgorji

Step4: test musicscore

  * type in following commands in Terminal: 
      * python3
      * from musicscore.musicstream import SimpleFormat
      * from musicscore.musictree.treescoretimewise import TreeScoreTimewise
      * score = TreeScoreTimewise()
      * sf = SimpleFormat(durations = [1, 2, 3, 2, 1], midis=[60, [54, 58], 70, 80, 48])
      * sf.auto_clef()
      * voice = sf.to_voice(1)
      * voice.add_to_score(score=score, first_measure=1, part_number=1)
      * score.write('test_1')


