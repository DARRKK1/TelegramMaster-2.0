from loguru import logger

from telethon.errors import *
from telethon.tl.functions.channels import LeaveChannelRequest

from system.telegram_actions.telegram_actions import telegram_connect_and_output_name


def unsubscribe_all(db_handler) -> None:
    """Отписываемся от групп, каналов, личных сообщений"""
    # Открываем базу данных для работы с аккаунтами user_settings/software_database.db
    records: list = db_handler.open_and_read_data("config")
    logger.info(f"Всего accounts: {len(records)}")
    for row in records:
        # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
        client, phone = telegram_connect_and_output_name(row, db_handler)
        for dialog in client.iter_dialogs():
            logger.info(f"{dialog.name}, {dialog.id}")
            client.delete_dialog(dialog)
            client.disconnect()


def unsubscribe_from_the_group(client, group_link) -> None:
    """
    Отписываемся от группы
    """
    try:
        entity = client.get_entity(group_link)
        if entity:
            client(LeaveChannelRequest(entity))
    except ChannelPrivateError:  # Аккаунт Telegram не может отписаться так как не имеет доступа
        logger.error(f'Группа или канал: {group_link}, является закрытым или аккаунт не имеет доступ  к {group_link}')
    finally:
        client.disconnect()  # Разрываем соединение с Telegram
