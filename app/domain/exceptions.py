class InvalidCurrencyRateError(Exception):
    """Неверный курс валюты."""

    def __init__(self, currency_rate: float) -> None:
        super().__init__(f'Currency rate {currency_rate} is not valid')
