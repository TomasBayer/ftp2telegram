import hashlib
import logging
import telepot

from ftprelay import FTPRelay, AuthenticationFailedError
from ftp2telegram.config import build_configuration

logger = logging.getLogger(__name__)


class FTP2Telegram(FTPRelay):

    def __init__(self, raw_config):
        self.config = build_configuration(raw_config)
        self.bot = telepot.Bot(self.config['telegram']['token'])

        super().__init__((self.config['ftp']['host'], self.config['ftp']['port']), self._file_processor_creator)

    def _file_processor_creator(self, username, password):
        for user in filter(lambda user: user['name'] == username, self.config['users']):
            if user['password'] == hashlib.sha256((password + user['salt']).encode('utf8')).hexdigest():
                return lambda file: self._send_file(file, user['telegram_id'])

        raise AuthenticationFailedError()

    def _send_file(self, file, id):
        print(file, id)
        with open(file, 'rb') as fh:
            self.bot.sendDocument(id, fh)
