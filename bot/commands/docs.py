from aiogram.filters import Command
from aiogram.types import Message
from bot.modules.menu import create_menu
from bot.config.flags import DOCS_ENABLE
import logging


async def handle_docs(message: Message, state):
    """
    Обрабатывает команду /docs.
    """
    logging.debug(f"Команда /docs вызвана пользователем: "
                  f"{message.from_user.id}")

    if not DOCS_ENABLE:
        logging.warning("Команда /docs временно отключена.")
        return await message.answer("Команда временно отключена.")

    try:
        menu, _ = create_menu(user_id=message.from_user.id)  # Распаковка
        if not menu.inline_keyboard:
            logging.warning("Главное меню пустое. "
                            "Проверьте настройки LINKS.")
            return await message.answer("Меню временно недоступно. "
                                        "Обратитесь к администратору.")

        # Формируем текст главного меню
        main_menu_text = ("Вот какие ссылки я знаю."
                          "\nВыберите из меню ниже:")

        # Сохраняем текст главного меню в состоянии пользователя
        await state.update_data(main_menu_text=main_menu_text)

        await message.answer(
            main_menu_text,
            reply_markup=menu,
        )
    except Exception as e:
        logging.error(f"Ошибка при обработке команды /docs "
                      f"для пользователя {message.from_user.id}: {e}")
        await message.reply(f"Произошла ошибка: {e}")


def register_docs_handler(dp):
    """
    Регистрирует обработчик команды /docs.
    :param dp: Экземпляр Dispatcher
    """
    logging.debug("Регистрация обработчика команды /docs")
    dp.message.register(handle_docs, Command(commands=["docs"]))
