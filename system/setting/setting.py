# -*- coding: utf-8 -*-
import configparser
import getpass
from rich import print
from telethon import TelegramClient
from telethon.errors import *
import tkinter as tk
from system.auxiliary_functions.global_variables import console
from system.menu.baner import program_version, date_of_program_change
from system.notification.notification import app_notifications
from system.sqlite_working_tools.sqlite_working_tools import writing_data_to_the_db, save_proxy_data_to_db
from tkinter import ttk
config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)

creating_a_table = "CREATE TABLE IF NOT EXISTS config(id, hash, phone)"
writing_data_to_a_table = "INSERT INTO config (id, hash, phone) VALUES (?, ?, ?)"
config.read('setting_user/config.ini')


def record_account_limits() -> configparser.ConfigParser:
    """Запись лимитов на аккаунт"""
    limits = console.input("[bold green][+] Введите лимит на аккаунт : ")
    config.get('account_limits', 'limits')
    config.set('account_limits', 'limits', limits)
    return config


def writing_settings_to_a_file(config):
    """Запись данных в файл setting_user/config.ini"""
    with open('setting_user/config.ini', 'w') as setup:
        config.write(setup)


def writing_api_id_api_hash() -> configparser.ConfigParser:
    """Записываем api, hash полученный с помощью регистрации приложения на сайте https://my.telegram.org/auth"""
    api_id_data = console.input("[bold green][+] Введите api_id : ")
    config.get('telegram_settings', 'id')
    config.set('telegram_settings', 'id', api_id_data)
    api_hash_data = console.input("[bold green][+] Введите api_hash : ")
    config.get('telegram_settings', 'hash')
    config.set('telegram_settings', 'hash', api_hash_data)
    return config


def writing_link_to_the_group() -> configparser.ConfigParser:
    """Записываем ссылку для inviting групп"""
    target_group_entity_user = console.input("[bold green][+] Введите ссылку на группу : ")  # Вводим ссылку на группу
    # Находим ссылку в файле и меняем на свою
    config.get('link_to_the_group', 'target_group_entity')
    config.set('link_to_the_group', 'target_group_entity', target_group_entity_user)
    return config


def recording_limits_file(time_1, time_2, variable: str) -> configparser.ConfigParser:
    """Запись данных в файл setting_user/time_inviting.ini"""
    config.get(f'{variable}', f'{variable}_1')
    config.set(f'{variable}', f'{variable}_1', time_1)
    config.get(f'{variable}', f'{variable}_2')
    config.set(f'{variable}', f'{variable}_2', time_2)
    return config


def reading_the_id_and_hash():
    """Считываем id и hash"""
    config.read('setting_user/config.ini')  # Файл с настройками
    api_id_data = config['telegram_settings']['id']  # api_id с файла setting_user/api_id_api_hash.ini
    api_hash_data = config['telegram_settings']['hash']  # api_hash с файла setting_user/api_id_api_hash.ini
    return api_id_data, api_hash_data


def connecting_new_account() -> None:
    """Вводим данные в базу данных setting_user/software_database.db"""
    api_id_data, api_hash_data = reading_the_id_and_hash()
    phone_data = console.input("[bold green][+] Введите номер телефона : ")  # Вводим номер телефона
    entities = (api_id_data, api_hash_data, phone_data)
    writing_data_to_the_db(creating_a_table, writing_data_to_a_table, entities)
    # Подключение к Telegram, возвращаем client для дальнейшего отключения сессии
    client = telegram_connect(phone_data, api_id_data, api_hash_data)
    client.disconnect()  # Разрываем соединение telegram
    # Выводим уведомление, если операционная система windows 7, то выводим уведомление в консоль
    app_notifications(notification_text="Аккаунт подсоединился!")


def telegram_connect(phone, api_id, api_hash) -> TelegramClient:
    """Account telegram connect, с проверкой на валидность, если ранее не было соединения, то запрашиваем код"""
    client = TelegramClient(f"setting_user/accounts/{phone}", api_id, api_hash)
    client.connect()  # Подсоединяемся к Telegram
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            # Если ранее аккаунт не подсоединялся, то просим ввести код подтверждения
            client.sign_in(phone, code=console.input("[bold red][+] Введите код: "))
        except SessionPasswordNeededError:
            """
            https://telethonn.readthedocs.io/en/latest/extra/basic/creating-a-client.html#two-factor-authorization-2fa
            """
            # Если аккаунт имеет password, то просим пользователя ввести пароль
            client.sign_in(password=getpass.getpass())
        except ApiIdInvalidError:
            print("[bold red][!] Не валидные api_id/api_hash")
    return client


def creating_the_main_window_for_proxy_data_entry() -> None:
    """Создание главного окна для ввода дынных proxy"""
    print("Proxy IPV6 - НЕ РАБОТАЮТ")

    def recording_proxy_data() -> list:
        """Запись данных для proxy, Proxy IPV6 - НЕ РАБОТАЮТ"""
        proxy_types = proxy_type_entry.get()
        addr_types = addr_type_entry.get()
        port_types = port_type_entry.get()
        username_types = username_type_entry.get()
        password_types = password_type_entry.get()
        rdns_types = "True"
        proxy = [proxy_types, addr_types, port_types, username_types, password_types, rdns_types]
        root.destroy()
        return proxy

    root = tk.Tk()  # Создаем главное окно
    root.title("Telegram_BOT_SMM")
    root.geometry("300x250")  # Устанавливаем размер окна
    root.resizable(False, False)  # Запретить масштабирование окна
    # Создаем первое текстовое поле и связанный с ним текстовый метка
    proxy_type = tk.Label(root, text="Введите тип прокси, например SOCKS5: ")
    proxy_type.pack()
    proxy_type_entry = tk.Entry(root, width=45)
    proxy_type_entry.pack()
    # Создаем второе текстовое поле и связанный с ним текстовый метка
    addr_type = tk.Label(root, text="Введите ip адрес, например 194.67.248.9: ")
    addr_type.pack()
    addr_type_entry = tk.Entry(root, width=45)
    addr_type_entry.pack()
    # Создаем третье текстовое поле и связанный с ним текстовый метка
    port_type = tk.Label(root, text="Введите порт прокси, например 9795: ")
    port_type.pack()
    port_type_entry = tk.Entry(root, width=45)
    port_type_entry.pack()
    # Создаем четвертое текстовое поле и связанный с ним текстовый метка
    username_type = tk.Label(root, text="Введите username, например NnbjvX: ")
    username_type.pack()
    username_type_entry = tk.Entry(root, width=45)
    username_type_entry.pack()
    # Создаем пятое текстовое поле и связанный с ним текстовый метка
    password_type = tk.Label(root, text="Введите password, например ySfCfk: ")
    password_type.pack()
    password_type_entry = tk.Entry(root, width=45)
    password_type_entry.pack()

    # Создаем кнопку
    button = tk.Button(root, text="Готово", command=lambda: save_proxy_data_to_db(proxy=recording_proxy_data()))
    button.pack()
    result_label = tk.Label(root, text="")  # Создаем метку для вывода результата
    result_label.pack()
    root.mainloop()  # Запускаем главный цикл обработки событий


def create_main_window(variable) -> None:
    """Создание главного окна приложения"""

    def entering_the_time_between_actions() -> None:
        """Проверка введенных данных"""
        # Получаем значения из полей ввода
        smaller_time = smaller_time_entry.get()
        larger_time = larger_time_entry.get()
        # Проверяем, что оба поля были заполнены целыми числами
        try:
            smaller_time = int(smaller_time)
            larger_time = int(larger_time)
        except ValueError:
            # Если пользователь ввел не число, выводим сообщение об ошибке
            result_label.config(text="Пожалуйста, введите целые числа!")
            return
        # Проверяем, что первое время меньше второго
        if smaller_time < larger_time:
            # Если условие прошло проверку, то возвращаем первое и второе время
            result_label.config(
                text="Вы ввели:\n{} секунд (меньшее время)\n{} секунд (большее время)".format(smaller_time,
                                                                                              larger_time))
            config = recording_limits_file(str(smaller_time), str(larger_time), variable=variable)
            writing_settings_to_a_file(config)
            root.destroy()
        else:
            # Если первое время больше второго, выводим сообщение об ошибке
            result_label.config(text="Пожалуйста, введите корректные значения времени!")

    root = tk.Tk()  # Создаем главное окно
    root.title(f"Telegram_BOT_SMM: {program_version} от {date_of_program_change}")
    root.geometry("300x110")  # Устанавливаем размер окна
    root.resizable(False, False)  # Запретить масштабирование окна
    # Установка стиля оформления
    s = ttk.Style()
    s.theme_use('winnative')
    # Создаем первое текстовое поле и связанный с ним текстовый метка
    smaller_time_label = ttk.Label(root, text="Время в секундах (меньшее):")
    smaller_time_label.pack()
    smaller_time_entry = ttk.Entry(root, width=45)
    smaller_time_entry.pack()
    # Создаем второе текстовое поле и связанный с ним текстовый метка
    larger_time_label = ttk.Label(root, text="Время в секундах (большее):")
    larger_time_label.pack()
    larger_time_entry = ttk.Entry(root, width=45)
    larger_time_entry.pack()
    # Создаем кнопку
    button = ttk.Button(root, text="Готово", command=entering_the_time_between_actions)
    button.pack()
    result_label = ttk.Label(root, text="")  # Создаем метку для вывода результата
    result_label.pack()
    root.mainloop()  # Запускаем главный цикл обработки событий


if __name__ == "__main__":
    connecting_new_account()
    writing_link_to_the_group()
    # recording_proxy_data()
    creating_the_main_window_for_proxy_data_entry()
