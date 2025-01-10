import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

# Абсолютный путь к файлу chat_list.json
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHAT_LIST_FILE = DATA_DIR / "chat_list.json"


def ensure_data_directory():
    """
    Убедиться, что папка данных существует.
    """
    DATA_DIR.mkdir(exist_ok=True)


def get_chat_list() -> List[Dict[str, Any]]:
    """
    Загружает список чатов из файла.
    :return: Список чатов или пустой список,
    если файл отсутствует или повреждён.
    """
    ensure_data_directory()
    try:
        with open(CHAT_LIST_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.debug(f"Файл {CHAT_LIST_FILE} не найден. "
                      f"Возвращён пустой список.")
        return []
    except json.JSONDecodeError:
        logging.error(f"Ошибка чтения файла {CHAT_LIST_FILE}. "
                      f"Возвращён пустой список.")
        return []


def save_chat_list(chat_list: List[Dict[str, Any]]) -> None:
    """
    Сохраняет список чатов в файл.
    """
    ensure_data_directory()
    with open(CHAT_LIST_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_list, file, indent=4, ensure_ascii=False)
    logging.debug(f"Список чатов сохранён в файл {CHAT_LIST_FILE}.")


async def is_user_admin(message: Message) -> bool:
    """
    Проверяет, является ли пользователь администратором чата.
    """
    try:
        chat_administrators = await message.bot.get_chat_administrators(
            message.chat.id)
        return any(admin.user.id == message.from_user.id for
                   admin in chat_administrators)
    except Exception as e:
        logging.error(f"Ошибка при проверке администратора: {e}")
        return False
