import logging
from enum import Enum

from aiogram import (
    Bot,
    Dispatcher,
    executor,
)
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import Message, ReplyKeyboardMarkup

from app.application.settings.config import BotConfig
from app.core import constants
from app.domain.interfaces.repository import RepositoryInterface
from app.domain.interfaces.service import ServiceInterface
from app.domain.value_object import CurrencyRate
from app.infrastructure.exceptions import CannotGetCurrencyRateError

logger = logging.getLogger(__name__)


class CurrencyRateEnum(Enum):
    """Перечисление валют."""
    USD = '$'
    EUR = '€'


class TelegramBotService(ServiceInterface):
    """Telegram бот."""

    def __init__(
            self,
            *,
            bot_config: BotConfig,
            repository: RepositoryInterface[CurrencyRate],
    ) -> None:
        self.__bot_config = bot_config
        self.__bot = Bot(token=self.__bot_config.token)
        self.__dispatcher = Dispatcher(self.__bot)
        self.__repository = repository

    def __register_message_handlers(self) -> None:
        """Регистрация обработчиков сообщений."""
        self.__dispatcher.register_message_handler(
            callback=self.__setup_keyboard,
            commands=['start'],
        )
        self.__dispatcher.register_message_handler(
            callback=self.__send_currency_rate,
        )

    @staticmethod
    async def __setup_keyboard(message: Message) -> SendMessage:
        """Настройка клавиатуры."""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[currency.value for currency in CurrencyRateEnum])
        return SendMessage(
            chat_id=message.chat.id,
            text=constants.SELECT_CURRENCY_MESSAGE,
            reply_markup=keyboard,
        )

    def run(self) -> None:
        """Запуск бота."""
        self.__register_message_handlers()
        executor.start_webhook(
            dispatcher=self.__dispatcher,
            webhook_path=self.__bot_config.webhook_path,
            skip_updates=True,
            on_startup=self.__on_startup,
            on_shutdown=self.__on_shutdown,
        )

    async def __on_startup(self, _dispatcher: Dispatcher) -> None:
        """Обработчик запуска бота."""
        await self.__bot.set_webhook(
            url=self.__bot_config.webhook_url,
            secret_token=self.__bot_config.secret_key,
        )

    async def __on_shutdown(self, _dispatcher: Dispatcher) -> None:
        """Обработчик остановки бота."""
        await self.__bot.delete_webhook(drop_pending_updates=True)

    async def __send_currency_rate(self, message: Message) -> SendMessage:
        """Отправка курса валюты."""
        try:
            currency_rate_name = CurrencyRateEnum(message.text).name
        except ValueError:
            logger.info('Неверная валюта', {'currency_rate_name': message.text})
            return SendMessage(
                chat_id=message.chat.id,
                text=constants.INVALID_CURRENCY_MESSAGE,
            )
        try:
            currency_domain = await self.__repository.get_currency_rate_by_name(currency_rate_name)
        except CannotGetCurrencyRateError:
            logger.error(
                'Ошибка получения доменной модели курса валюты CurrencyRate', {
                    'currency_rate_name': currency_rate_name,
                })
            return SendMessage(
                chat_id=message.chat.id,
                text=constants.SERVICE_ERROR_MESSAGE,
            )
        return SendMessage(
            chat_id=message.chat.id,
            text=str(currency_domain.currency),
        )
