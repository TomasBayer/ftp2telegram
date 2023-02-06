import argparse
import logging
import sys
from pathlib import Path

import argparse
import logging
import os
import sys
import yaml

from ftp2telegram import FTP2Telegram



def build_argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-file', '-c', type=Path, help="config file")
    parser.add_argument('--verbose', '-v', action='store_true', help="verbose mode")

    return parser


def run():
    parser = build_argparser()
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)-15s %(levelname)-8s %(message)s')

    def get_config_file():
        if args.config_file:
            return os.path.expanduser(args.config_file)
        else:
            for file in map(os.path.expanduser, ("~/.ftp2telegram.conf", "/etc/ftp2telegram.conf")):
                if os.path.exists(file):
                    return file

    config_file = get_config_file()

    if not config_file:
        sys.exit("No configuration file found.")

    try:
        with open(config_file) as config_file:
            config = yaml.load(config_file)
    except yaml.YAMLError:
        sys.exit("Invalid YAML in configuration file: {}".format(config))

    ftp = FTP2Telegram(config)
    ftp.serve_forever()
