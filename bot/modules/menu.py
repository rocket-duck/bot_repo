from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.config.links import LINKS
import logging


def create_main_menu(user_id):
    """
    Создаёт главное меню на основе LINKS.
    :param user_id: ID пользователя (для уникальных callback_data)
    :return: InlineKeyboardMarkup с кнопками и название меню
    """
    logging.debug(f"Создание главного меню. user_id={user_id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for section, content in LINKS.items():
        key = content.get("key")
        url = content.get("url")
        if "subsections" not in content and url:  # Нет подразделов, есть ссылка
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(text=section,
                                      url=url)]
            )
        elif key:  # Есть подразделы или просто ключ
            callback_data = f"menu:{user_id}:{key}"
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(text=section,
                                      callback_data=callback_data)]
            )
        else:
            logging.warning(f"Пропущен раздел "
                            f"'{section}' из-за некорректной структуры.")

    return keyboard, "Главное меню"


def create_submenu(menu_key, user_id):
    """
    Создаёт подменю для указанного раздела.
    :param menu_key: Ключ раздела
    :param user_id: ID пользователя (для уникальных callback_data)
    :return: InlineKeyboardMarkup с кнопками и название раздела
    """
    logging.debug(f"Создание подменю. menu_key={menu_key}, user_id={user_id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # Поиск данных для подменю
    data = next((v for k, v in LINKS.items() if v.get("key") == menu_key), None)
    section_name = next((k for k, v in LINKS.items() if
                         v.get("key") == menu_key), menu_key)

    if not data:
        logging.error(f"Раздел '{menu_key}' отсутствует в LINKS.")
        return keyboard, section_name

    subsections = data.get("subsections", {})
    for subsection, content in subsections.items():
        url = content.get("url")
        key = content.get("key")
        if url:  # Ссылка в подразделе
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(text=subsection,
                                      url=url)]
            )
        elif key:  # Подраздел с ключом
            callback_data = f"menu:{user_id}:{key}"
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(text=subsection,
                                      callback_data=callback_data)]
            )
        else:
            logging.warning(f"Пропущен подраздел "
                            f"'{subsection}' из-за некорректной структуры.")

    # Добавляем кнопку "Назад", если это подменю
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="⬅️ Назад",
                              callback_data=f"menu:{user_id}:main")]
    )

    return keyboard, section_name


def create_menu(menu_key=None, user_id=None):
    """
    Создаёт меню (главное или подменю) на основе LINKS.
    :param menu_key: Ключ раздела для подменю (None для главного меню)
    :param user_id: ID пользователя (для уникальных callback_data)
    :return: InlineKeyboardMarkup с кнопками и название раздела
    """
    logging.debug(f"Создание меню. menu_key={menu_key}, user_id={user_id}")
    if menu_key is None:
        return create_main_menu(user_id)
    return create_submenu(menu_key, user_id)
