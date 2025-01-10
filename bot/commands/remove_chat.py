import logging
from datetime import datetime
from aiogram.filters import Command
from aiogram.types import Message
from bot.utils.chat_manager import get_chat_list, save_chat_list, is_user_admin
from bot.config.flags import REMOVE_CHAT_ENABLE

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)


def mark_chat_as_deleted(chat_id: int, deleted_by: str) -> bool:
    """
    Помечает чат как удалённый.
    :param chat_id: ID чата для удаления.
    :param deleted_by: Кто удалил (username или имя пользователя).
    :return: True, если чат был найден и помечен, False, если чат не найден.
    """
    chat_list = get_chat_list()
    for chat in chat_list:
        if chat["id"] == chat_id:
            if chat.get("deleted", False):  # Чат уже помечен как удалённый
                logging.debug(f"Чат {chat_id} ({chat['title']}) "
                              f"уже помечен как удалённый.")
                return False
            chat["deleted"] = True
            chat["deleted_by"] = deleted_by
            chat["deleted_at"] = datetime.now().isoformat()
            save_chat_list(chat_list)
            logging.info(f"Чат {chat_id} ({chat['title']}) "
                         f"помечен как удалённый пользователем {deleted_by}.")
            return True
    logging.debug(f"Чат {chat_id} не найден в списке.")
    return False


async def handle_remove_chat(message: Message):
    """
    Обработчик команды /remove_chat.
    """
    # Удаляем сообщение пользователя
    try:
        await message.delete()
    except Exception as e:
        logging.error(f"Не удалось удалить сообщение пользователя: {e}")

    if not REMOVE_CHAT_ENABLE:
        logging.debug("Команда /remove_chat временно отключена.")
        return

    # Проверяем, является ли пользователь администратором
    if not await is_user_admin(message):
        logging.debug("Команда /remove_chat доступна "
                      "только администраторам чата.")
        return

    chat_id = message.chat.id
    deleted_by = message.from_user.username or message.from_user.full_name

    if mark_chat_as_deleted(chat_id, deleted_by):
        logging.info(f"Чат {chat_id} успешно обработан.")
    else:
        logging.debug(f"Чат {chat_id} уже был удалён или не найден.")


def register_remove_chat_handler(dp):
    """
    Регистрирует обработчик команды /remove_chat.
    """
    dp.message.register(handle_remove_chat,
                        Command(commands=["remove_chat"]))
