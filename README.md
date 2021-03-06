# EPROM (27C010) reader for Raspberry Pi

Tested on a pi400.

Inspired by https://www.instructables.com/Raspberry-Pi-Python-EEPROM-Programmer/

See https://hackaday.io/project/182779-late-90s-gps-time-unit-repair-1024-week-bug-fix/log/201888-reverse-engineering-first-steps for context

Rough diagram of pinout:

![Pinouts](eprom-reader-pinout.png)

Note that pins 3&5 have hard wired pullup resistors and thus have to be used for CE# and OE# pins only.

Photo of quick and dirty circuit on connected to Pi400:

![Breadboard picture](eprom-reader-breadboard.png)

Added CC license because the original article on instructables was also CC


The eprom.sh was a experiment to do the same thing using bash.
It works, but very very very very slowly (e.g. takes over 10 hours to read!)
Also I had a bug with the data lines backwards at one point, so the flip.py program was used to fixup the image file.
