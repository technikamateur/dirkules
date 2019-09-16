from logging import Handler

import requests


class TelegramHandler(Handler):
    def __init__(self, token=None, chat_id=None):
        Handler.__init__(self)
        self.communicator = TelegramCom(token, chat_id)

    def emit(self, record):
        self.communicator.send_logging_emit(self.format(record).split("#"))


class TelegramCom:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.api_url = "https://api.telegram.org/bot"

    def _send_message(self, message):
        # try handels dirty problem if no internet connection is available
        try:
            my_url = self.api_url + self.token + "/sendMessage?chat_id=" + self.chat_id + "&parse_mode=Markdown" + \
                     "&text=" + message
            response = requests.get(my_url)
            # response.text contains ok with value true/false
        except:
            pass

    def send_logging_emit(self, record):
        message = '*{}*%0AWhere: `{}`%0AWhat: `{}`'.format(record[0], record[1], record[2])
        self._send_message(message)
