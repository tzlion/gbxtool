gbxtool - GBX ROM Tool

v1.0.dev (in-development version)

For GBX ROM format v1.0 - http://hhug.me/gbx/1.0

Requires Python 3 interpreter to run
Written using Python 3.8, not sure if it'll work with older 3.x versions

how you start the Python 3 interpreter depends on your platform and how Python is installed I think but you'll want to run it with the ROM filename as a parameter
e.g.
py pytool.py romname.gb
python pytool.py romname.gb
python3 pytool.py romname.gb
python3.8 pytool.py romname.gb
something like that

No other options, the rest is interactive

For a file with a GBX footer, it can edit the footer, remove the footer and hash the data
For a file without a GBX footer, it can add a footer or hash the data
