import json
import logging
from pathlib import Path
from aiogram.filters import Command
from aiogram.types import Message
from bot.config.flags import BEST_QA_STAT_ENABLE

# Путь к директории данных
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STATS_FILE = DATA_DIR / "best_qa_stats.json"

# Логирование
logging.basicConfig(level=logging.DEBUG)


def ensure_data_directory():
    """
    Убедиться, что папка data существует.
    """
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    logging.debug(f"Папка {DATA_DIR} проверена или создана.")


def load_stats():
    """
    Загружает статистику из JSON-файла.
    :return: Словарь статистики или пустой словарь.
    """
    ensure_data_directory()
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning(f"Файл {STATS_FILE} не найден. "
                        f"Возвращён пустой словарь.")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования JSON в {STATS_FILE}: {e}")
        return {}


async def handle_best_qa_stat(message: Message):
    """
    Обработчик команды /best_qa_stat.
    Показывает статистику победителей текущего чата.
    """
    if not BEST_QA_STAT_ENABLE:
        await message.answer("Команда временно отключена.")
        return

    # Команда доступна только в групповых чатах
    if message.chat.type == "private":
        await message.answer("Статистика доступна только для групповых чатов.")
        return

    stats = load_stats()
    chat_id = str(message.chat.id)

    # Проверка наличия данных для текущего чата
    chat_stats = stats.get(chat_id)
    if not chat_stats or not chat_stats.get("winners"):
        await message.answer("Статистика по лучшим тестировщикам пока пуста.")
        return

    # Формируем и отправляем текст статистики
    stat_message = [f"Статистика победителей для чата: "
                    f"{chat_stats['chat_title']}:"]
    for winner in chat_stats["winners"].values():
        username = f" (@{winner['username']})" if winner.get("username") else ""
        stat_message.append(f"• {winner['full_name']}{username}: "
                            f"{winner['wins']} побед(ы)")

    await message.answer("\n".join(stat_message))


def register_best_qa_stat_handler(dp):
    """
    Регистрирует обработчик команды /best_qa_stat.
    """
    dp.message.register(handle_best_qa_stat, Command(commands=["best_qa_stat"]))
