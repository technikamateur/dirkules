# dirkules
Ein kleines, aber feines, Programm zur Überwachung von Servern. Es ist auf meine Bedürfnisse zugeschnitten und sollte nicht im Produktiven Umfeld verwendet werden.

## Vorraussetzungen
Debian basiertes Betriebssystem mit folgenden installierten Paketen:
- smartmontools
- python3
- python3-pip
- gunicorn3
- hwinfo

## Installation
Bitte einen eigenen Benutzer anlegen. Diesem folgende root-Rechte (ohne Passwort) einräumen:
- ausführen von `smartctl`

Als dieser Nutzer folgende Befehle ausführen:
- `git clone https://github.com/technikamateur/dirkules.git`
- `cd dirkules`
- `pip3 install .`
- `gunicorn3 dirkules:app`