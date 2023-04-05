from pathlib import Path
from typing import MutableMapping

import toml
from pydantic import BaseSettings

from app.core import constants


class BotConfig(BaseSettings):
    """Конфигурация бота."""
    token: str
    secret_key: str
    webhook_url: str
    webhook_path: str


def get_config() -> MutableMapping:
    """Сначала пробует прочитать дев-конфиг,
    но если его нет, то читает прод-конфиг."""
    if Path(constants.DEVELOPMENT_CONFIG_PATH).exists():
        filepath = constants.DEVELOPMENT_CONFIG_PATH
    else:
        filepath = constants.PRODUCTION_CONFIG_PATH
    with open(filepath, encoding='utf-8') as file:
        return toml.load(file)
