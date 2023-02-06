import logging
from dataclasses import dataclass, field
from pathlib import Path

import telepot
from ftprelay import AuthenticationFailedError, Authenticator, FileProcessor, FTPRelay
from passlib.hash import sha512_crypt

logger = logging.getLogger(__name__)


@dataclass
class User:
    name: str
    hashed_password: str
    telegram_id: int

    def authenticate(self, password: str) -> bool:
        return sha512_crypt.verify(password, self.hashed_password)


@dataclass
class TelegramFileSender(FileProcessor):
    bot_token: str
    recipient_id: int

    def process_file(self, file: Path) -> None:
        bot = telepot.Bot(self.bot_token)

        with file.open('rb') as fh:
            bot.sendDocument(self.recipient_id, fh)


@dataclass
class TelegramAuthenticator(Authenticator):
    telegram_bot_token: str
    users: list[User]

    def get_user(self, username: str) -> User:
        for user in self.users:
            if user.name == username:
                return user

        raise AuthenticationFailedError()

    def authenticate(self, username: str, password: str) -> FileProcessor:
        user = self.get_user(username)

        if user.authenticate(password):
            return TelegramFileSender(bot_token=self.telegram_bot_token, recipient_id=user.telegram_id)
        else:
            raise AuthenticationFailedError()


@dataclass
class FTP2Telegram:
    telegram_bot_token: str
    users: list[User]
    ftp_host: str
    ftp_port: int

    relay: FTPRelay = field(init=False, default=None)

    def __post_init__(self):
        self.relay = FTPRelay(
            authenticator=TelegramAuthenticator(self.telegram_bot_token, self.users),
            host=self.ftp_host,
            port=self.ftp_port,
        )

    def start(self):
        self.relay.start()

    def stop(self):
        self.relay.stop()
