import logging.config

from app.application.settings.config import BotConfig, get_config
from app.domain.interfaces.repository import RepositoryInterface
from app.domain.interfaces.service import ServiceInterface
from app.infrastructure.ioc.container import DependencyContainer
from app.infrastructure.ioc.provider import DependencyProvider
from app.infrastructure.repository import CentralBankRepository
from app.infrastructure.service import TelegramBotService


def get_bot_application(
        *,
        bot_config,
) -> ServiceInterface:
    """Создание экземпляра бота."""
    dependency_container = DependencyContainer()
    dependency_container.bind_multiple({
        RepositoryInterface: CentralBankRepository,
        ServiceInterface: TelegramBotService,
    })
    dependency_provider = DependencyProvider(
        container=dependency_container,
        bot_config=bot_config,
    )
    return dependency_provider.provide_service()


if __name__ == '__main__':
    config = get_config()
    logging.config.dictConfig(config['logger'])
    bot = get_bot_application(bot_config=BotConfig())  # type: ignore
    bot.run()
