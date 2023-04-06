from abc import ABC, abstractmethod


class ServiceInterface(ABC):
    """Интерфейс сервиса."""

    @abstractmethod
    def run(self) -> None:
        """Запуск бота."""
