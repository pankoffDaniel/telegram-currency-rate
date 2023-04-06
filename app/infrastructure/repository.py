import logging
from json import JSONDecodeError

from aiohttp import (
    ClientSession,
    ClientConnectorError,
    ClientResponseError,
)

from app.domain.exceptions import InvalidCurrencyRateError
from app.domain.interfaces.repository import RepositoryInterface
from app.domain.value_object import CurrencyRate
from app.infrastructure.exceptions import CannotGetCurrencyRateError

logger = logging.getLogger(__name__)


class CentralBankRepository(RepositoryInterface[CurrencyRate]):
    """Репозиторий работы с курсом валютой ЦБ РФ."""

    @staticmethod
    async def get_all_currency_rates() -> dict:
        """Получение всех курсов валют."""
        async with ClientSession() as session:
            url = 'https://www.cbr-xml-daily.ru/daily_json.js'
            try:
                async with session.get(url, ssl=True) as response:
                    all_currency_rates = await response.json(
                        content_type='application/javascript',
                    )
            except (
                    ClientConnectorError,
                    ClientResponseError,
                    TimeoutError,
            ) as exception:
                logger.error('Ошибка установки соединения с ЦБ РФ АПИ')
                raise CannotGetCurrencyRateError from exception
            try:
                return all_currency_rates['Valute']
            except (JSONDecodeError, KeyError) as exception:
                logger.error('Ошибка в структуре полученных данных ЦБ РФ', {
                    'data': all_currency_rates,
                })
                raise CannotGetCurrencyRateError from exception

    async def get_currency_rate_by_name(self, currency_name: str) -> CurrencyRate:
        """Получение курса валюты по имени."""
        try:
            all_currency_rates = await self.get_all_currency_rates()
        except CannotGetCurrencyRateError as exception:
            logger.error('Ошибка получения списка курс валют')
            raise exception
        try:
            currency_rate_value = all_currency_rates[currency_name]['Value']
        except KeyError as exception:
            logger.error('Ошибка получения значения курса валюты', {
                'data': all_currency_rates,
                'currency_name': currency_name,
            })
            raise CannotGetCurrencyRateError from exception
        try:
            return CurrencyRate(currency_rate_value)
        except (TypeError, InvalidCurrencyRateError) as exception:
            logger.error('Ошибка создания доменной модели CurrencyRate', {
                'currency_rate_value': currency_rate_value,
            })
            raise CannotGetCurrencyRateError from exception
