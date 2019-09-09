from logging import Handler
import urllib.request


class TelegramHandler(Handler):
    def __init__(self, token=None, chat_id=None):
        Handler.__init__(self)
        self.communicator = TelegramCom(token, chat_id)
        self.test_number = 1

    def emit(self, record):
        if self.test_number != 0:
            self.communicator.send_logging_emit(self.format(record).split("#"))
            self.test_number = 0


class TelegramCom:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.api_url = "https://api.telegram.org/bot"

    def _send_message(self, message):
        my_url = self.api_url + self.token + "/sendMessage?chat_id=" + self.chat_id + "&text=" + message + "&parse_mode=Markdown"
        response = urllib.request.urlopen(my_url).read()

    def send_logging_emit(self, record):
        print(record)
        message = '*{}* %0A hi'.format(record[0])
        self._send_message(message)
