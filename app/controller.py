from enum import Enum

from aiogram import (
    Bot,
    Dispatcher,
    executor,
)
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import Message, ReplyKeyboardMarkup

from app.core.settings.config import BotConfig
from app.service import AbstractCurrencyRateService


class CurrencyRateEnum(Enum):
    """Перечисление валют."""
    USD = '$'
    EUR = '€'


class TelegramBotController:
    """Telegram бот."""

    def __init__(
            self,
            *,
            bot_config: BotConfig,
            service: AbstractCurrencyRateService,
    ) -> None:
        self._bot_config = bot_config
        self._bot = Bot(token=self._bot_config.token)
        self._dispatcher = Dispatcher(self._bot)
        self._service = service

    def _register_message_handlers(self) -> None:
        """Регистрация обработчиков сообщений."""
        self._dispatcher.register_message_handler(
            callback=self._setup_keyboard,
            commands=['start'],
        )
        self._dispatcher.register_message_handler(
            callback=self._send_currency_rate,
        )

    @staticmethod
    async def _setup_keyboard(message: Message) -> SendMessage:
        """Настройка клавиатуры."""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[currency.value for currency in CurrencyRateEnum])
        return SendMessage(
            chat_id=message.chat.id,
            text='Выберите валюту',
            reply_markup=keyboard,
        )

    def run(self) -> None:
        """Запуск бота."""
        self._register_message_handlers()
        executor.start_webhook(
            dispatcher=self._dispatcher,
            webhook_path=self._bot_config.webhook_path,
            skip_updates=True,
            on_startup=self._on_startup,
            on_shutdown=self._on_shutdown,
        )

    async def _on_startup(self, _dispatcher: Dispatcher) -> None:
        """Обработчик запуска бота."""
        await self._bot.set_webhook(
            url=self._bot_config.webhook_url,
            secret_token=self._bot_config.secret_key,
        )

    async def _on_shutdown(self, _dispatcher: Dispatcher) -> None:
        """Обработчик остановки бота."""
        await self._bot.delete_webhook(drop_pending_updates=True)

    async def _send_currency_rate(self, message: Message) -> SendMessage:
        """Отправка курса валюты."""
        try:
            currency_rate_name = CurrencyRateEnum(message.text).name
        except ValueError as _exception:
            return SendMessage(
                chat_id=message.chat.id,
                text='Неверная валюта',
            )
        currency_rate_value = await self._service.get_currency_rate_by_name(currency_rate_name)
        return SendMessage(
            chat_id=message.chat.id,
            text=currency_rate_value,
        )
