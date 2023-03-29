from pydantic import BaseSettings


class BotConfig(BaseSettings):
    """Конфигурация бота."""
    token: str
    secret_key: str
    webhook_url: str
    webhook_path: str
