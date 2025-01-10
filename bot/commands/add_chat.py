import logging
from datetime import datetime
from aiogram.filters import Command
from aiogram.types import Message
from bot.utils.chat_manager import get_chat_list, save_chat_list, is_user_admin
from bot.config.flags import ADD_CHAT_ENABLE

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)


def add_chat(chat_id: int, chat_title: str, added_by: str) -> None:
    """
    Добавляет новый чат в список, если его там ещё нет.
    """
    chat_list = get_chat_list()

    # Проверяем, существует ли уже этот чат
    existing_chat = next((chat for chat in chat_list if
                          chat["id"] == chat_id), None)
    if existing_chat:
        if existing_chat.get("deleted", False):  # Если чат помечен как удалён
            existing_chat["deleted"] = False
            existing_chat["deleted_by"] = None
            existing_chat["deleted_at"] = None
            save_chat_list(chat_list)
            logging.info(f"Чат {chat_id} восстановлен.")
        else:
            logging.debug(f"Чат {chat_id} уже существует в списке.")
        return

    # Добавляем новый чат
    chat_list.append({
        "id": chat_id,
        "title": chat_title,
        "added_by": added_by,
        "added_at": datetime.now().isoformat(),
        "deleted": False,
        "deleted_by": None,
        "deleted_at": None
    })
    save_chat_list(chat_list)
    logging.info(f"Чат {chat_id} ({chat_title}) "
                 f"добавлен в список пользователем {added_by}.")


async def handle_add_chat(message: Message):
    """
    Обработчик команды /add_chat.
    """
    # Удаляем сообщение пользователя
    try:
        await message.delete()
    except Exception as e:
        logging.error(f"Не удалось удалить сообщение пользователя: {e}")

    if not ADD_CHAT_ENABLE:
        logging.debug("Команда /add_chat временно отключена.")
        return

    if not await is_user_admin(message):
        logging.debug("Команда /add_chat доступна только администраторам чата.")
        return

    chat_id = message.chat.id
    chat_title = message.chat.title or "Личный чат"
    added_by = message.from_user.username or message.from_user.full_name

    add_chat(chat_id, chat_title, added_by)


def register_add_chat_handler(dp):
    """
    Регистрирует обработчик команды /add_chat.
    """
    dp.message.register(handle_add_chat,
                        Command(commands=["add_chat"]))
