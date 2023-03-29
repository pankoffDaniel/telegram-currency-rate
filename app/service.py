import json
from abc import ABC, abstractmethod

from aiohttp import ClientSession


class AbstractCurrencyRateService(ABC):
    """Абстрактный класс для получения курса валюты."""

    @staticmethod
    @abstractmethod
    async def get_all_currency_rate() -> dict:
        """Получение всех курсов валют."""

    @abstractmethod
    async def get_currency_rate_by_name(self, currency_name: str) -> str:
        """Получение курса валюты по имени."""


class CentralBankCurrencyRateService(AbstractCurrencyRateService):
    """Класс для получения курса валюты с сайта ЦБ РФ."""

    @staticmethod
    async def get_all_currency_rate() -> dict:
        async with ClientSession() as session:
            url = 'https://www.cbr-xml-daily.ru/daily_json.js'
            async with session.get(url, ssl=False) as response:
                currency_rate = await response.text()
        return json.loads(currency_rate)

    async def get_currency_rate_by_name(self, currency_name: str) -> str:
        all_currency_rate = await self.get_all_currency_rate()
        currency_rate = all_currency_rate['Valute'][currency_name]['Value']
        return json.dumps(currency_rate, ensure_ascii=False)
