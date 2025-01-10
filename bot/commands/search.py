import logging
import openai
from aiogram.filters import Command
from aiogram.types import Message
from bot.config.tokens import OPENAI_API_KEY
from bot.config.gpt_prompt import PROMPT

# Настройка OpenAI API
openai.api_key = OPENAI_API_KEY


async def handle_search(message: Message):
    """
    Обрабатывает команду /search.
    Принимает текст от пользователя,
    отправляет его в OpenAI GPT и возвращает ответ.
    :param message: Сообщение от пользователя
    """
    query = message.text.split(maxsplit=1)
    if len(query) < 2:
        await message.answer("Пожалуйста, "
                             "укажите текст запроса.\n"
                             "Пример: /search Как работает OpenAI?")
        return

    user_query = query[1]
    await message.answer("Обрабатываю ваш запрос...")

    try:
        # Отправляем запрос в OpenAI GPT
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": user_query}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Извлекаем ответ из результата
        answer = response.choices[0].message.content
        await message.answer(answer)

    except Exception as e:
        await message.answer("Произошла "
                             "ошибка при обработке запроса. "
                             "Попробуйте позже.")
        logging.error(f"Ошибка при запросе к OpenAI: {e}")


def register_search_handler(dp):
    """
    Регистрирует обработчик команды /search.
    :param dp: Экземпляр Dispatcher
    """
    dp.message.register(handle_search, Command(commands=["search"]))
