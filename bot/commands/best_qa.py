import random
import json
from pathlib import Path
from datetime import datetime, timezone
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hlink
from bot.config.flags import BEST_QA_ENABLE

# Путь к файлам
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STATS_FILE = DATA_DIR / "best_qa_stats.json"
LAST_WINNER_FILE = DATA_DIR / "last_winner.json"


def ensure_config_directory():
    """
    Создаёт папку config, если её нет.
    """
    DATA_DIR.mkdir(exist_ok=True)


def load_json(file_path):
    """
    Загружает данные из JSON-файла.
    """
    ensure_config_directory()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(file_path, data):
    """
    Сохраняет данные в JSON-файл.
    """
    ensure_config_directory()
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def update_last_winner(chat_id, chat_title, user_id, full_name, username):
    """
    Обновляет данные о последнем победителе в JSON-файле.
    """
    last_winner = load_json(LAST_WINNER_FILE)

    chat_id = str(chat_id)
    last_winner[chat_id] = {
        "chat_title": chat_title,
        "last_datetime": datetime.now(timezone.utc).isoformat(),
        "winner": {
            "user_id": user_id,
            "full_name": full_name,
            "username": username or ""
        }
    }

    save_json(LAST_WINNER_FILE, last_winner)


def update_stats(chat_id, chat_title, user_id, full_name, username):
    """
    Обновляет статистику победителей в JSON-файле.
    """
    stats = load_json(STATS_FILE)

    chat_id = str(chat_id)
    if chat_id not in stats:
        stats[chat_id] = {"chat_title": chat_title, "winners": {}}

    winners = stats[chat_id]["winners"]
    user_key = str(user_id)

    if user_key not in winners:
        winners[user_key] = {
            "full_name": full_name,
            "username": username or "",
            "wins": 0
        }

    winners[user_key]["wins"] += 1
    save_json(STATS_FILE, stats)


def get_last_winner(chat_id):
    """
    Получает данные о последнем победителе из JSON-файла.
    """
    last_winner = load_json(LAST_WINNER_FILE)
    return last_winner.get(str(chat_id))


def is_new_day(chat_id):
    """
    Проверяет, наступил ли новый день (в 00:00 UTC) для конкретного чата.
    :param chat_id: ID чата
    :return: True, если новый день; иначе False.
    """
    last_winner = get_last_winner(chat_id)
    if not last_winner:
        return True

    last_datetime = last_winner.get("last_datetime")
    if not last_datetime:
        return True

    last_date = datetime.fromisoformat(last_datetime).date()
    current_date = datetime.now(timezone.utc).date()

    # Проверяем, совпадает ли дата с текущей
    return current_date > last_date


async def get_random_participant(bot, chat_id):
    """
    Выбирает случайного участника из всех участников чата (исключая ботов).
    """
    members = []
    admin_list = await bot.get_chat_administrators(chat_id)

    for member in admin_list:
        if not member.user.is_bot:
            members.append(member.user)

    return random.choice(members) if members else None


async def check_group_chat(message: Message):
    """
    Проверяет, выполняется ли команда в групповом чате.
    """
    if message.chat.type == "private":
        await message.reply("Выбор лучшего тестировщика возможен "
                            "только в групповых чатах.")
        return False
    return True


async def notify_best_qa(message: Message):
    """
    Уведомляет о текущем выбранном тестировщике.
    """
    last_winner = get_last_winner(message.chat.id)

    if not last_winner:
        await message.reply("Данные о лучшем тестировщике отсутствуют. "
                            "Попробуйте выбрать заново.")
        return

    winner = last_winner["winner"]
    mention = hlink(winner["full_name"], f"tg://user?id={winner['user_id']}")
    await message.answer(f"Сегодня лучший тестировщик уже выбран: "
                         f"{mention} 🎉", parse_mode="HTML")


async def select_best_qa(message: Message):
    """
    Выбирает случайного участника и уведомляет чат.
    """
    best_qa = await get_random_participant(message.bot, message.chat.id)

    if not best_qa:
        await message.reply("Не нашёл участников для выбора.")
        return

    update_last_winner(
        chat_id=message.chat.id,
        chat_title=message.chat.title or "Личный чат",
        user_id=best_qa.id,
        full_name=best_qa.full_name,
        username=best_qa.username
    )

    update_stats(
        chat_id=message.chat.id,
        chat_title=message.chat.title or "Личный чат",
        user_id=best_qa.id,
        full_name=best_qa.full_name,
        username=best_qa.username
    )

    mention = hlink(best_qa.full_name, f"tg://user?id={best_qa.id}")
    await message.answer(f"Сегодня лучший тестировщик "
                         f"{mention} 🎉", parse_mode="HTML")


async def handle_best_qa(message: Message):
    """
    Обработчик команды /best_qa.
    """
    if not BEST_QA_ENABLE:
        return await message.answer("Команда временно отключена.")

    if not await check_group_chat(message):
        return

    if not is_new_day(message.chat.id):
        await notify_best_qa(message)
        return

    await select_best_qa(message)


def register_best_qa_handler(dp):
    """
    Регистрирует обработчик команды /best_qa.
    """
    dp.message.register(handle_best_qa, Command(commands=["best_qa"]))
