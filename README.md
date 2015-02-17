# Vclient web

A simple web interface built in Python for [vcontrold](http://openv.wikispaces.com/vcontrold) and [vclient](http://openv.wikispaces.com/vclient).
It provides the ability to control the Viessmann Vito heating system over the web. 

## Goals

* Easy
* Lightweight
* Hackable
* Nice on [Raspberry Pi](http://www.raspberrypi.org/)

## Dependencies

* Python (already shipped with Raspbian)
* [CherryPy](http://www.cherrypy.org/) (`sudo apt-get install python-cherrypy3`)
* [Python sqlite3](https://docs.python.org/2/library/sqlite3.html) (`sudo apt-get install python-sqlite`) 

## Dev dependencies

* [Bower](http://bower.io/)

## Install

1. Install `vcontrol` and `vclient` and make them available in `$PATH`.
2. Download this app and extract it in your home directory.
3. Add the following to your crontab: `*/10 * * * * vclient -h localhost:3002 -t ~/vclient-web/vito.tmpl -f ~/vclient-web/command.txt -x ~/vclient-web/vito.sh`
4. Run: `python server.py` from the `vclient-web` directory

## Credits

Week-end (not even) project by [Kévin Dunglas](http://dunglas.fr).

