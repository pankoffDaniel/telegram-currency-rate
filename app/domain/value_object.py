from app.domain.exceptions import InvalidCurrencyRateError


class CurrencyRate:
    """Модель курса валюты."""

    def __init__(self, currency: float | int) -> None:
        self.__validate(currency)
        self.__currency = currency

    @staticmethod
    def __validate(currency: float | int) -> None:
        """Валидация курса валюты."""
        if not isinstance(currency, (float, int)):
            raise TypeError
        if currency <= 0:
            raise InvalidCurrencyRateError(currency)

    @property
    def currency(self) -> float | int:
        """Получение значения курса валюты."""
        return self.__currency
