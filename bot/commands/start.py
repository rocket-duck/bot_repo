from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot.commands.help import handle_help


async def handle_start(message: Message):
    """
    Обрабатывает команду /start.
    :param message: Сообщение от пользователя
    """
    # Создаём клавиатуру с кнопкой "Список команд"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список команд", callback_data="help")]
    ])

    await message.answer(
        "Привет! Я бот, который поможет найти ссылки на полезную документацию"
        "или разобраться в процессах тестирования МБ СМБ.\n"
        "Выберите 'Список команд' что бы узнать что я умею",
        reply_markup=keyboard,
    )


async def handle_help_callback(callback_query: Message):
    """
    Обрабатывает нажатие на кнопку "Список команд".
    :param callback_query: CallbackQuery от пользователя
    """
    # Вызываем уже существующий обработчик команды /help
    await handle_help(callback_query.message)


def register_start_handler(dp):
    """
    Регистрирует обработчики команды /start и кнопки "Список команд".
    :param dp: Экземпляр Dispatcher
    """
    dp.message.register(handle_start, Command(commands=["start"]))
    dp.callback_query.register(handle_help_callback, lambda c: c.data == "help")
