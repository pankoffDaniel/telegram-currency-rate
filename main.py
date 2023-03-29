from app.controller import TelegramBotController
from app.core.settings.config import BotConfig
from app.service import CentralBankCurrencyRateService


def get_bot_application(
        *,
        bot_config,
) -> TelegramBotController:
    """Создание экземпляра бота."""
    return TelegramBotController(
        bot_config=bot_config,
        service=CentralBankCurrencyRateService(),
    )


if __name__ == '__main__':
    bot = get_bot_application(bot_config=BotConfig())  # type: ignore
    bot.run()
