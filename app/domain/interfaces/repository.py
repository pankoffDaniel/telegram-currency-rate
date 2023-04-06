from abc import abstractmethod, ABC

from typing import Generic, TypeVar

CurrencyRate = TypeVar('CurrencyRate')


class RepositoryInterface(Generic[CurrencyRate], ABC):
    """Интерфейс репозитория."""

    @staticmethod
    @abstractmethod
    async def get_all_currency_rates() -> dict:
        """Получение всех курсов валют."""
        raise NotImplementedError

    @abstractmethod
    async def get_currency_rate_by_name(self, currency_name: str) -> CurrencyRate:
        """Получение курса валюты по имени."""
        raise NotImplementedError
