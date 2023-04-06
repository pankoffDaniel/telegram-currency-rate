from pathlib import Path

SETTINGS_PATH = Path('app/application/settings')
PRODUCTION_CONFIG_PATH = SETTINGS_PATH / 'config.toml'
DEVELOPMENT_CONFIG_PATH = SETTINGS_PATH / 'config.dev.toml'
SELECT_CURRENCY_MESSAGE = 'Выберите валюту'
INVALID_CURRENCY_MESSAGE = 'Неверная валюта'
SERVICE_ERROR_MESSAGE = 'Произошла ошибка'
