import logging
from aiogram.filters import Command
from aiogram.types import Message
from bot.modules.commands_list import get_all_commands


async def handle_help(message: Message):
    """
    Обрабатывает команду /help.
    Формирует текст на основе доступных команд для текущего типа чата.
    :param message: Сообщение от пользователя
    """
    # Получаем полный список команд
    commands = get_all_commands()

    # Логирование всех команд
    logging.debug(f"Все команды: {commands}")

    # Определяем тип чата
    chat_type = "private_chat" \
        if message.chat.type == "private" else "group_chat"

    # Фильтрация команд по типу чата и видимости
    visible_commands = [
        cmd["command"] for cmd in commands
        if cmd[chat_type] and cmd.get("visible_in_help", True)
    ]

    # Логирование доступных команд
    logging.debug(f"Доступные команды для {chat_type}: {visible_commands}")

    # Если список команд пустой
    if not visible_commands:
        await message.answer("Нет доступных команд для вашего чата.")
        return

    # Формируем текст помощи
    help_text = "Привет! Вот список доступных команд:\n\n"
    for command in visible_commands:
        help_text += f"/{command.command} — {command.description}\n"

    await message.answer(help_text)


def register_help_handler(dp):
    """
    Регистрирует обработчик команды /help.
    :param dp: Экземпляр Dispatcher
    """
    dp.message.register(handle_help, Command(commands=["help"]))
