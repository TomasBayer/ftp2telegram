import logging
from pathlib import Path
from typing import Annotated, Optional

import pkg_resources
import typer
import yaml
from click import ClickException

from ftp2telegram.config import build_configuration
from ftp2telegram.server import FTP2Telegram, User

app = typer.Typer()

DEFAULT_CONFIG_FILE_PATHS = (
    Path("~/.ftp2telegram.conf").expanduser(),
    Path("/etc/ftp2telegram.conf"),
)


@app.command()
def run(
        *,
        config_file: Annotated[Optional[Path], typer.Option(
            "--config", "-c",
            help="Path to config file.",
        )] = None,
        create_example_config: Annotated[bool, typer.Option(
            "--create-example-config",
            help=f"Create an example configuration at {DEFAULT_CONFIG_FILE_PATHS[0]}, then exit.",
        )] = False,
        verbose: Annotated[bool, typer.Option(
            "--verbose", "-v",
            help="Verbose mode.",
        )] = False,
):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)-15s %(levelname)-8s %(message)s')

    if create_example_config:
        if DEFAULT_CONFIG_FILE_PATHS[0].exists():
            raise ClickException(f"Error: A config file already exists at {DEFAULT_CONFIG_FILE_PATHS[0]}.")
        else:
            with DEFAULT_CONFIG_FILE_PATHS[0].open('wb') as fh:
                fh.write(pkg_resources.resource_string(__name__, 'resources/example-config.yml'))
            typer.echo(f"An example config file has been created at {DEFAULT_CONFIG_FILE_PATHS[0]}.")
            raise typer.Exit(0)

    # Find config file
    if config_file is None:
        for file in DEFAULT_CONFIG_FILE_PATHS:
            if file.exists():
                config_file = file
                break

    if config_file is None or not config_file.exists():
        raise ClickException("No configuration file found.")

    try:
        with config_file.open() as fh:
            config = build_configuration(yaml.safe_load(fh))
    except yaml.YAMLError as err:
        raise ClickException(f"Invalid YAML in configuration file: {config}") from err

    ftp = FTP2Telegram(
        telegram_bot_token=config['telegram']['token'],
        users=[User(**user) for user in config['users']],
        ftp_host=config['ftp']['host'],
        ftp_port=config['ftp']['port'],
    )
    ftp.start()
