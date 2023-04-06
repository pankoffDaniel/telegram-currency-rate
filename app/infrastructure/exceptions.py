class CannotGetCurrencyRateError(Exception):
    """Ошибка получения курса валюты."""

    def __init__(self) -> None:
        super().__init__('Cannot get currency rate')
