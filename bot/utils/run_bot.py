import logging
from aiogram import Bot, Dispatcher
from bot.config.tokens import API_TOKEN
from bot.utils.handlers import register_handlers
from bot.modules.commands_list import set_bot_commands


async def run_bot():
    """
    Главная функция для запуска бота.
    """
    # Настройка логирования
    logging.basicConfig(level=logging.DEBUG)

    # Инициализация бота и диспетчера
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Регистрация обработчиков
    register_handlers(dp)

    # Запуск бота
    logging.info("Запуск бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    await set_bot_commands(bot)
    await dp.start_polling(bot)
