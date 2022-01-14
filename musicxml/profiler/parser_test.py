import datetime
from pathlib import Path

from musicxml.parser.parser import parse_musicxml

start_reading = datetime.datetime.now()
print("start reading score")
score = parse_musicxml(Path(__file__).parent / 'parser_test.xml')
start_writing = datetime.datetime.now()
print(f"start writing score :{start_writing - start_reading}")
score.write(Path(__file__).parent / 'parser_test_create.xml')
end = datetime.datetime.now()
print(f"end writing score :{end - start_writing}")


