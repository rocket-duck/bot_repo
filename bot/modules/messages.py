import asyncio
from aiogram.types import Message
from datetime import datetime, timedelta
from bot.utils.message_parse import find_links_by_keyword
from bot.utils.who_request import handle_who_request
from bot.config.flags import (KEYWORD_RESPONSES_ENABLE,
                              TIMEOUT_RESPONSES_ENABLE,
                              WHO_REQUEST_ENABLE)
import logging


# Настройка времени таймаута (в минутах)
TIMEOUT_MINUTES = 5

# Хранилище для предотвращения повторных ответов (по чатам)
recent_links = {}  # Формат: {chat_id: {"url": время последнего ответа}}


async def handle_message(message: Message):
    """
    Основная функция для обработки текстовых сообщений пользователя.
    """

    # Проверка триггеров модуля who_request
    await handle_who_request(message, WHO_REQUEST_ENABLE)

    # Проверка включения функции обработки сообщений
    if not KEYWORD_RESPONSES_ENABLE:
        logging.debug("Функция парсинга сообщений отключена")
        return

    # Проверяем, содержит ли сообщение текст
    if not message.text:
        logging.debug("Сообщение не содержит текста, обработка пропущена.")
        return

    # Проверка на команду
    if is_command(message):
        return

    # Извлечение ключевого слова и обработка ссылок
    keyword = extract_keyword(message)
    if not keyword:
        return

    results = find_links_by_keyword(keyword)
    if results:
        await process_results(message, results)
    else:
        logging.debug("Совпадений не найдено.")


def is_command(message: Message) -> bool:
    """
    Проверяет, является ли сообщение командой.
    :param message: Сообщение от пользователя
    :return: True, если это команда; иначе False
    """
    if message.text and message.text.startswith("/"):
        logging.debug(f"Сообщение {message.text} "
                      f"игнорируется, так как это команда.")
        return True
    return False


def extract_keyword(message: Message) -> str:
    """
    Извлекает ключевое слово из сообщения.
    :param message: Сообщение от пользователя
    :return: Ключевое слово в нижнем регистре
    """
    if not message.text:
        logging.debug(f"Сообщение не содержит текста: {message}")
        return ""
    keyword = message.text.strip().lower()
    logging.debug(f"Извлечённое ключевое слово: {keyword}")
    return keyword


async def process_results(message: Message, results: list):
    """
    Обрабатывает результаты поиска ссылок.
    :param message: Сообщение от пользователя
    :param results: Найденные ссылки
    """
    filtered_results = filter_recent_links(message.chat.id,
                                           results) if (
        TIMEOUT_RESPONSES_ENABLE) else (
        results)

    if filtered_results:
        response = format_response(filtered_results)
        logging.debug(f"Отправка ссылки: {response}")
        await message.answer(response, reply_to_message_id=message.message_id)

        # Планируем удаление ссылок из recent_links
        # через таймаут, если он включён
        if TIMEOUT_RESPONSES_ENABLE:
            for _, url in filtered_results:
                asyncio.create_task(remove_link_after_timeout(message.chat.id,
                                                              url))
    else:
        logging.debug("Все ссылки уже были отправлены недавно.")


def filter_recent_links(chat_id: int, results: list) -> list:
    """
    Фильтрует ссылки, которые уже были отправлены недавно для конкретного чата.
    :param chat_id: ID чата
    :param results: Список найденных ссылок
    :return: Отфильтрованный список ссылок
    """
    filtered_results = []
    chat_recent_links = recent_links.setdefault(chat_id, {})
    for name, url in results:
        if (url in chat_recent_links and datetime.now() - chat_recent_links[url]
                < timedelta(minutes=TIMEOUT_MINUTES)):
            logging.debug(f"Пропуск отправки ссылки '{url}' "
                          f"для чата {chat_id}, так как она "
                          f"отправлялась недавно.")
        else:
            filtered_results.append((name, url))
            chat_recent_links[url] = datetime.now()
    return filtered_results


def format_response(results: list) -> str:
    """
    Форматирует ответ для пользователя.
    :param results: Список найденных ссылок
    :return: Строка ответа
    """
    return "Возможно это поможет разобраться:\n" + "\n".join([
        f"{name}: {url}" for name, url in results])


async def remove_link_after_timeout(chat_id: int, url: str):
    """
    Удаляет ссылку из recent_links для конкретного чата через указанный таймаут.
    :param chat_id: ID чата
    :param url: URL ссылки
    """
    await asyncio.sleep(TIMEOUT_MINUTES * 60)
    chat_recent_links = recent_links.get(chat_id, {})
    if url in chat_recent_links:
        del chat_recent_links[url]
        logging.debug(f"Ссылка '{url}' удалена из кэша для чата {chat_id}.")


def register_message_handlers(dp):
    """
    Регистрирует обработчик текстовых сообщений.
    :param dp: Экземпляр Dispatcher
    """
    dp.message.register(handle_message)
