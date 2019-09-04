import urllib.request
from dirkules import app


class TelegramCom:
    def __init__(self, app):
        self.token = app.config["TOKEN"]
        self.chat_id = app.config["CHAT_ID"]
        self.api_url = "https://api.telegram.org/bot"

    def send_message(self, message):
        my_url = self.api_url + self.token + "/sendMessage?chat_id=" + self.chat_id + "&text=" + message
        response = urllib.request.urlopen(my_url).read()
        app.logger.info('Nachricht gesendet: %s', message)

    def missing_drive(self, drive):
        message = "Folgende Festplatte wurde nicht gefunden: " + str(drive)
        self.send_message(message)

    def smart_changed(self, drive, new):
        message = "Die SMART Werte der Festplatte " + str(drive) + " wurden geaendert zu "
        if new:
            message = message + "GUT."
        else:
            message = message + "SCHLECHT."
        self.send_message(message)
