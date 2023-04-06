import os
from dataclasses import dataclass

import toml

from app.core import constants


@dataclass(frozen=True)
class BotConfig:
    """Конфигурация бота."""
    token: str = os.environ['TOKEN']
    secret_key: str = os.environ['SECRET_KEY']
    webhook_url: str = os.environ['WEBHOOK_URL']
    webhook_path: str = os.environ['WEBHOOK_PATH']


def get_config() -> dict:
    """Сначала пробует прочитать дев-конфиг,
    но если его нет, то читает прод-конфиг."""
    if constants.DEVELOPMENT_CONFIG_PATH.exists():
        filepath = constants.DEVELOPMENT_CONFIG_PATH
    else:
        filepath = constants.PRODUCTION_CONFIG_PATH
    with filepath.open(encoding='utf-8') as file:
        return toml.load(file)
