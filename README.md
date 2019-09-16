# dirkules
Ein kleines, aber feines, Programm zur Überwachung von Servern. Es ist auf meine Bedürfnisse zugeschnitten und sollte nicht im Produktiven Umfeld verwendet werden.

## Vorraussetzungen
Debian basiertes Betriebssystem mit folgenden installierten Paketen:
- smartmontools
- python3
- python3-pip
- gunicorn3
- curl

## Installation
Bitte einen eigenen Benutzer anlegen. Diesem folgende root-Rechte (ohne Passwort) einräumen:
- `smartctl`
- `lsblk`
- `btrfs`
- `find`

Als dieser Nutzer folgende Befehle ausführen:
- `git clone https://github.com/technikamateur/dirkules.git`
- `cd dirkules`
- `pip3 install .`
- `gunicorn3 dirkules:app`

## Integrierte Projekte und Frameworks
- [Semantic UI](https://github.com/Semantic-Org/Semantic-UI) - licensed under MIT
- [UI-Icon](https://github.com/Semantic-Org/UI-Icon/) - licensed under MIT
- [CodePen Error Page](https://codepen.io/saransh/pen/aezht) - licensed under MIT
