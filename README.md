gbxtool - GBX ROM Tool
======================

v1.0.0-beta

For GBX ROM format v1.0 - http://hhug.me/gbx/1.0

Major & minor versions will match the GBX version

Released under CC0 license. do what you like with this

Features
--------

For a file with a GBX footer, it can edit the footer, remove the footer and hash the data

For a file without a GBX footer, it can add a footer or hash the data

Usage
-----

Requires Python 3 interpreter to run - https://www.python.org/downloads/

Written using Python 3.8, not sure if it'll work with older 3.x versions

how you start the Python 3 interpreter depends on your platform and how Python is installed but you'll want to run it with the ROM filename as a parameter

e.g.

* ```py gbxtool.py romname.gb```
* ```python gbxtool.py romname.gb```
* ```python3 gbxtool.py romname.gb```
* ```python3.8 gbxtool.py romname.gb```

something like that

No other options, the rest is interactive
