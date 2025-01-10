import logging
from aiogram.filters import Command
from aiogram.types import Message
from bot.utils.chat_manager import get_chat_list
from bot.config.flags import ANNOUNCE_ENABLE


async def send_announce_to_chat(chat,
                                bot,
                                announce_message=None,
                                reply_to_message=None):
    """
    Отправляет текст и/или пересылает сообщение в указанный чат.
    :param chat: Словарь с информацией о чате {'id': <int>, 'title': <str>}
    :param bot: Экземпляр бота
    :param announce_message: Текст для отправки
    :param reply_to_message: Сообщение для пересылки
    """
    chat_id = chat['id']
    try:
        if announce_message:
            await bot.send_message(chat_id, announce_message)
        if reply_to_message:
            await reply_to_message.forward(chat_id)
    except Exception as e:
        logging.warning(f"Не удалось отправить сообщение в чат "
                        f"{chat_id} ({chat['title']}): {e}")


async def prepare_announce(message: Message):
    """
    Подготавливает текст и/или сообщение для рассылки.
    :param message: Сообщение от пользователя
    :return: Кортеж (announce_message, reply_to_message)
    """
    announce_message = (
        message.text.split(maxsplit=1)[1]
        if len(message.text.split()) > 1
        else None
    )
    reply_to_message = message.reply_to_message

    if not announce_message and not reply_to_message:
        await message.answer(
            "Пожалуйста, укажите текст для рассылки или "
            "ответьте на сообщение для пересылки.\n"
            "Пример: /announce Текст рассылки или "
            "/announce в ответ на сообщение."
        )
        return None, None

    return announce_message, reply_to_message


async def send_announcements(chat_list,
                             bot,
                             announce_message,
                             reply_to_message):
    """
    Отправляет сообщения во все активные чаты.
    :param chat_list: Список чатов
    :param bot: Экземпляр бота
    :param announce_message: Текст для рассылки
    :param reply_to_message: Сообщение для пересылки
    """
    for chat in chat_list:
        await send_announce_to_chat(chat,
                                    bot,
                                    announce_message,
                                    reply_to_message)


async def handle_announce(message: Message):
    """
    Обрабатывает команду /announce.
    """
    if not ANNOUNCE_ENABLE:
        return await message.answer("Команда временно отключена.")

    # Получаем список активных чатов
    chat_list = [chat for chat in get_chat_list() if
                 not chat.get("deleted", False)]
    if not chat_list:
        return await message.answer("Нет активных чатов для отправки.")

    announce_message, reply_to_message = await prepare_announce(message)
    if not announce_message and not reply_to_message:
        return

    await send_announcements(chat_list,
                             message.bot,
                             announce_message,
                             reply_to_message)
    await message.answer("Сообщение отправлено во все активные чаты.")


def register_announce_handler(dp):
    """
    Регистрирует обработчик команды /announce.
    :param dp: Экземпляр Dispatcher
    """
    dp.message.register(handle_announce, Command(commands=["announce"]))
