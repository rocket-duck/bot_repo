from aiogram import Bot
from aiogram.types import (BotCommand,
                           BotCommandScopeDefault,
                           BotCommandScopeAllGroupChats)
from bot.config import flags


def add_command(commands,
                command_name,
                description,
                flag,
                private_chat=True,
                group_chat=True,
                visible_in_help=True):
    """
    Добавляет команду в список, если флаг установлен в True.
    :param commands: Список команд (модифицируется).
    :param command_name: Название команды.
    :param description: Описание команды.
    :param flag: Флаг включения команды.
    :param private_chat: Флаг отображения команды в личных чатах.
    :param group_chat: Флаг отображения команды в групповых чатах.
    :param visible_in_help: Флаг видимости команды.
    """
    if flag:
        commands.append({
            "command": BotCommand(command=command_name,
                                  description=description),
            "private_chat": private_chat,
            "group_chat": group_chat,
            "visible_in_help": visible_in_help
        })


def get_commands_for_scope(commands, scope):
    """
    Фильтрует команды по-указанному scope (личный или групповой чат).
    :param commands: Полный список команд.
    :param scope: Тип чата (private_chat или group_chat).
    :return: Список команд для указанного scope.
    """
    return [cmd["command"] for cmd in commands if cmd[scope]]


def get_all_commands():
    """
    Возвращает полный список команд с их параметрами.
    :return: Полный список команд.
    """
    commands = []
    add_command(commands, "help",
                "Получить справку",
                flags.HELP_ENABLE,
                private_chat=True,
                group_chat=True,
                visible_in_help=False)
    add_command(commands, "docs",
                "Открыть документацию",
                flags.DOCS_ENABLE,
                private_chat=True,
                group_chat=True,
                visible_in_help=True)
    add_command(commands, "announce",
                "Сделать объявление",
                flags.ANNOUNCE_ENABLE,
                private_chat=True,
                group_chat=False,
                visible_in_help=True)
    add_command(commands, "search",
                "Спросить chatGPT о тестировании",
                flags.SEARCH_ENABLE,
                private_chat=True,
                group_chat=True,
                visible_in_help=True)
    add_command(commands, "add_chat",
                "Добавить чат в список рассылки анонсов",
                flags.ADD_CHAT_ENABLE,
                private_chat=False,
                group_chat=False,
                visible_in_help=False)
    add_command(commands, "remove_chat",
                "Удалить чат из списка рассылки анонсов",
                flags.REMOVE_CHAT_ENABLE,
                private_chat=False,
                group_chat=False,
                visible_in_help=False)
    add_command(commands, "best_qa",
                "Выбрать лучшего тестировщика дня",
                flags.BEST_QA_ENABLE,
                private_chat=False,
                group_chat=True,
                visible_in_help=True)
    add_command(commands, "best_qa_stat",
                "Получить список победителей тестировщика дня",
                flags.BEST_QA_STAT_ENABLE,
                private_chat=False,
                group_chat=True,
                visible_in_help=True)
    return commands


async def set_bot_commands(bot: Bot):
    """
    Устанавливает команды бота для личных чатов и групп.
    :param bot: Экземпляр Bot
    """
    commands = get_all_commands()

    # Устанавливаем команды для личных чатов
    private_commands = get_commands_for_scope(commands, "private_chat")
    await bot.set_my_commands(private_commands,
                              scope=BotCommandScopeDefault())

    # Устанавливаем команды для всех групп
    group_commands = get_commands_for_scope(commands, "group_chat")
    await bot.set_my_commands(group_commands,
                              scope=BotCommandScopeAllGroupChats())
