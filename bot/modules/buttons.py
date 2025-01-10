from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.modules.menu import create_menu
import logging


async def handle_button(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие на кнопки меню.
    """
    try:
        data = callback.data.split(":")
        if len(data) < 3:
            await callback.answer("Некорректные данные кнопки.")
            logging.error(f"Некорректные данные callback_data: {callback.data}")
            return

        user_id = data[1]
        menu_key = data[2]

        if menu_key == "main":  # Главное меню
            logging.debug(f"Открытие главного меню для user_id={user_id}")
            menu, _ = create_menu(user_id=user_id)

            # Получаем текст главного меню из контекста
            user_data = await state.get_data()
            main_menu_text = user_data.get("main_menu_text", "Главное меню:")

            await callback.message.edit_text(
                main_menu_text,
                reply_markup=menu,
            )
        else:  # Подменю
            logging.debug(f"Открытие подменю "
                          f"'{menu_key}' для user_id={user_id}")
            menu, section_name = create_menu(menu_key=menu_key,
                                             user_id=user_id)
            if menu.inline_keyboard:
                await callback.message.edit_text(
                    f"Раздел: {section_name}:\n"
                    f"Выберите из меню ниже:",
                    reply_markup=menu,
                )
            else:
                await callback.answer("Этот раздел пуст.",
                                      show_alert=True)

    except Exception as e:
        logging.error(f"Ошибка при обработке кнопки: {e}")
        await callback.answer("Произошла ошибка. "
                              "Попробуйте снова.",
                              show_alert=True)


def register_button_handlers(dp):
    """
    Регистрирует обработчик нажатий на кнопки.
    :param dp: Экземпляр Dispatcher
    """
    dp.callback_query.register(
        handle_button,
        lambda callback: callback.data.startswith("menu:")
    )
