# ftp2telegram

`ftp2telegram` is an FTP server that forwards all uploaded files to preconfigured [Telegram](https://telegram.org/)
contacts.
It was developed with the specific goal of retrofitting a Telegram interface into older devices or software that
exclusively support FTP upload for file transfer.

**Caution:** `ftp2telegram` has not undergone security testing. Avoid exposing it to untrusted networks or the public
internet without implementing proper security measures.

## Quick Navigation

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Features

* Multiple telegram recipients
* User authorization
* Lightweight and fast (uses `pyftpdlib` underneath)
* Easy YAML configuration

## Installation

Requires Python version 3.9 or higher and pip.

```bash
pip install ftp2telegram
```

## Configuration

To configure `ftp2telegram`, a configuration file is required. By default, the program looks for it
in `~/.ftp2telegram.conf` or `/etc/ftp2telegram`. Create a sample configuration file with:

```bash
ftp2telegram --create-example-config
```

### Example Configuration File

```yaml
---
ftp:
  host: 127.0.0.1
  port: 21

telegram:
  token: MY_TOKEN

users:
  - name: alice
    hashed_password: |
      $6$Zfgtsr/z3RLvOEKj$D2s4w51WiFiCgyrRD.gxEeMtXxMkgas1OGkSU2c.XMKDdaJ2iOt72yFXM1rvzb7YuoOJ3.i9lMn1qQ7oVEDEm1
    telegram_id: 123
```

- FTP server configuration (`ftp`):
    - `host`: Specifies the FTP server's IP address or hostname.
    - `port`: Specifies the FTP server's port.
- Telegram configuration (`telegram`):
    - `token`: Replace `MY_TOKEN` with the actual token of your Telegram bot. Create one
      using [BotFather](https://core.telegram.org/bots#botfather).
- User configuration (`users`):
    - Each user in the list is defined by:
        - `name`: The username for FTP server authentication.
        - `hashed_password`: The SHA512-hashed password of the FTP user. Generate a hashed password
          using `openssl passwd -6`.
        - `telegram_id`: The Telegram user ID associated with the FTP user. Obtain it using bots such
          as [@userinfobot](https://telegram.me/userinfobot).

## Usage

Run the server:

```bash
ftp2telegram
```

### File Upload

Log into the server using any of the configured user credentials, and then upload a file. The uploaded file will be
automatically sent to the Telegram user linked to the corresponding FTP user in the config file.

### Caveats

- There are no subfolders on the FTP server, nor does it allow the creation of any. Thus, all files must be directly
  uploaded to the root directory.
- Using interactive FTP browsers to access the server may result in errors, as they are restricted from reading the
  contents of the root directory.
- Since Telegram bots cannot initiate conversations with users, recipients must add the bot and send them a message
  first before they can receive any files from the bot.

## License

`ftp2telegram` is distributed under the terms of the MIT License.
