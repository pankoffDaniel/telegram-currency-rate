from app.application.settings.config import BotConfig
from app.domain.interfaces.repository import RepositoryInterface
from app.domain.interfaces.service import ServiceInterface
from app.infrastructure.ioc.container import DependencyContainer


class DependencyProvider:
    """Провайдер зависимостей."""

    def __init__(
            self,
            *,
            container: DependencyContainer,
            bot_config: BotConfig,
    ) -> None:
        self.__container = container
        self.__bot_config = bot_config

    def provide_repository(self) -> RepositoryInterface:
        """Провайдер репозитория для получения курса валют."""
        return self.__container.get(RepositoryInterface)()

    def provide_service(self) -> ServiceInterface:
        """Провайдер сервиса Telegram-бота."""
        return self.__container.get(ServiceInterface)(
            bot_config=self.__bot_config,
            repository=self.provide_repository(),
        )
