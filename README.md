# TextMagic-python-PRTG-integration
PRTG runs this Windows script in order to send a notification

This is made with the purpose of 
1) using a primary and backup gateway
2) Using the text to speech feature
3) You are using windows

This is a very niche oriented usage, and this code is probably not useful to most people.

This was written in PYTHON 3

REQUIRES DNS PYTHON http://www.dnspython.org/ - can be installed by "pip install dnspython"

REQUIRES textmagic python library https://www.textmagic.com/docs/api/python/ - The pip install did not work properly for me. You may need to download the zip, and place the textmagic folder in the same directory as the textmagic.py file.

REQUIRES httplib2 library https://pypi.python.org/pypi/httplib2  - textmagic depends on this, and will be installed if you run "pip install textmagic".

I recommend WinPython if you are using windows.


I've included the sources for the textmagic and dns python.  You should try and download these libraries from their respective sources.
