import flet as ft

from system.account_actions.reactions.reactions import reaction_gui, record_the_number_of_accounts, \
    recording_link_channel
from system.menu.app_banner import program_version, date_of_program_change
from system.menu.app_gui import output_the_input_field
from system.setting.setting import recording_the_time_to_launch_an_invite_every_day, \
    recording_text_for_sending_messages, create_main_window, \
    creating_the_main_window_for_proxy_data_entry, record_device_type, \
    writing_api_id_api_hash, record_setting
from system.sqlite_working_tools.sqlite_working_tools import DatabaseHandler

line_width = 580  # Ширина окна и ширина строки


def mainss(page: ft.Page):
    page.title = f"TelegramMaster: {program_version} (Дата изменения {date_of_program_change})"
    page.window_width = line_width  # window's ширина is 200 px
    page.window_height = 700  # window's высота is 200 px
    page.window_resizable = False  # window is not resizable

    # width - ширина,  # height - высота
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View("/", [ft.AppBar(title=ft.Text("Главное меню"),
                                    bgcolor=ft.colors.SURFACE_VARIANT),
                          ft.Text(spans=[ft.TextSpan(
                              "TelegramMaster 2.0",
                              ft.TextStyle(
                                  size=40,
                                  weight=ft.FontWeight.BOLD,
                                  foreground=ft.Paint(
                                      gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                           ft.colors.PURPLE])), ), ), ], ),
                          ft.Text(disabled=False,
                                  spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                         ft.TextSpan("https://t.me/PyAdminRU",
                                                     ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                                                     url="https://t.me/PyAdminRU", ), ], ),
                          ft.Text(disabled=False,
                                  spans=[ft.TextSpan("Канал Telegram: "),
                                         ft.TextSpan("https://t.me/master_tg_d",
                                                     ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                                                     url="https://t.me/master_tg_d", ), ], ),
                          ft.ElevatedButton(width=line_width, height=30, text="Инвайтинг",
                                            on_click=lambda _: page.go("/inviting")),
                          ft.ElevatedButton(width=line_width, height=30, text="Парсинг",
                                            on_click=lambda _: page.go("/parsing")),
                          ft.ElevatedButton(width=line_width, height=30, text="Работа с контактами",
                                            on_click=lambda _: page.go("/contacts")),
                          ft.ElevatedButton(width=line_width, height=30, text="Подписка, отписка",
                                            on_click=lambda _: page.go("/subscribe_unsubscribe")),
                          ft.ElevatedButton(width=line_width, height=30, text="Подключение аккаунтов",
                                            on_click=lambda _: page.go("/store")),
                          ft.ElevatedButton(width=line_width, height=30, text="Рассылка сообщений",
                                            on_click=lambda _: page.go("/sending_messages")),
                          ft.ElevatedButton(width=line_width, height=30, text="Работа с реакциями",
                                            on_click=lambda _: page.go("/reaction")),
                          ft.ElevatedButton(width=line_width, height=30, text="Настройки",
                                            on_click=lambda _: page.go("/settings")),
                          ft.ElevatedButton(width=line_width, height=30, text="Проверка аккаунтов",
                                            on_click=lambda _: page.go("/store")),
                          ft.ElevatedButton(width=line_width, height=30, text="Создание групп (чатов)",
                                            on_click=lambda _: page.go("/store")),
                          ft.ElevatedButton(width=line_width, height=30, text="Редактирование BIO",
                                            on_click=lambda _: page.go("/bio")),
                          ], ))
        if page.route == "/inviting":
            # db_handler = DatabaseHandler()  # Создаем объект для работы с БД
            page.views.append(
                ft.View("/inviting", [ft.AppBar(title=ft.Text("Главное меню"),
                                                bgcolor=ft.colors.SURFACE_VARIANT),
                                      ft.ElevatedButton(width=line_width, height=30, text=f"Инвайтинг без лимитов",
                                                        on_click=lambda _: page.go("/inviting_without_limits")),
                                      ft.ElevatedButton(width=500, height=30, text="В начальное меню",
                                                        on_click=lambda _: page.go("/")), ], ))
        elif page.route == "/inviting_without_limits":
            print("Инвайтинг без лимитов")


        elif page.route == "/parsing":
            page.views.append(
                ft.View("/parsing", [ft.AppBar(title=ft.Text("Главное меню"),
                                               bgcolor=ft.colors.SURFACE_VARIANT),
                                     ft.ElevatedButton(width=line_width, height=30, text=f"Parsing одной групп",
                                                       on_click=lambda _: page.go("/")),
                                     ft.ElevatedButton(width=line_width, height=30, text=f"Выбор группы из подписанных",
                                                       on_click=lambda _: page.go("/")),
                                     ft.ElevatedButton(width=line_width, height=30, text=f"Parsing активных участников",
                                                       on_click=lambda _: page.go("/")),
                                     ft.ElevatedButton(width=line_width, height=30,
                                                       text=f"Parsing списка: групп, каналов аккаунтов",
                                                       on_click=lambda _: page.go("/")),
                                     ft.ElevatedButton(width=line_width, height=30, text=f"Очистка parsing списка",
                                                       on_click=lambda _: page.go("/")),
                                     ft.ElevatedButton(width=line_width, height=30, text="Формирование списка",
                                                       on_click=lambda _: page.go("/")), ], ))
        elif page.route == "/contacts":
            page.views.append(
                ft.View("/contacts", [ft.AppBar(title=ft.Text("Главное меню"),
                                                bgcolor=ft.colors.SURFACE_VARIANT),
                                      ft.ElevatedButton(width=line_width, height=30,
                                                        text=f"Формирование списка контактов",
                                                        on_click=lambda _: page.go("/")),
                                      ft.ElevatedButton(width=line_width, height=30, text=f"Показать список контактов",
                                                        on_click=lambda _: page.go("/")),
                                      ft.ElevatedButton(width=line_width, height=30, text=f"Удаление контактов",
                                                        on_click=lambda _: page.go("/")),
                                      ft.ElevatedButton(width=line_width, height=30, text=f"Добавление контактов",
                                                        on_click=lambda _: page.go("/")), ], ))
        elif page.route == "/subscribe_unsubscribe":
            page.views.append(
                ft.View("/subscribe_unsubscribe", [ft.AppBar(title=ft.Text("Главное меню"),
                                                             bgcolor=ft.colors.SURFACE_VARIANT),
                                                   ft.ElevatedButton(width=line_width, height=30,
                                                                     text=f"Формирование списка и подписка",
                                                                     on_click=lambda _: page.go("/")),
                                                   ft.ElevatedButton(width=line_width, height=30, text=f"Отписываемся",
                                                                     on_click=lambda _: page.go("/")), ], ))
        elif page.route == "/sending_messages":
            page.views.append(
                ft.View("/sending_messages", [ft.AppBar(title=ft.Text("Главное меню"),
                                                        bgcolor=ft.colors.SURFACE_VARIANT),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text=f"Отправка сообщений в личку",
                                                                on_click=lambda _: page.go("/")),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text=f"Отправка файлов в личку",
                                                                on_click=lambda _: page.go("/")),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text=f"Рассылка сообщений по чатам",
                                                                on_click=lambda _: page.go("/")),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text=f"Рассылка сообщений по чатам, по времени",
                                                                on_click=lambda _: page.go("/")),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text=f"Рассылка файлов по чатам",
                                                                on_click=lambda _: page.go("/")),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text="Рассылка сообщений + файлов по чатам",
                                                                on_click=lambda _: page.go("/")),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text=f"Формирование списка чатов",
                                                                on_click=lambda _: page.go("/")),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text="Отправка сообщений в личку (с лимитами)",
                                                                on_click=lambda _: page.go("/")),
                                              ft.ElevatedButton(width=line_width, height=30,
                                                                text="Отправка файлов в личку (с лимитами)",
                                                                on_click=lambda _: page.go("/")), ], ))
        elif page.route == "/reaction":  # Работа с реакциями
            page.views.append(
                ft.View("/reaction", [ft.AppBar(title=ft.Text("Главное меню"),
                                                bgcolor=ft.colors.SURFACE_VARIANT),
                                      ft.ElevatedButton(width=line_width, height=30, text=f"Ставим реакцию на 1 пост",
                                                        on_click=lambda _: page.go("/")),
                                      ft.ElevatedButton(width=line_width, height=30,
                                                        text="Накручиваем просмотры постов",
                                                        on_click=lambda _: page.go("/")), ], ))
        elif page.route == "/settings":  # Настройки
            page.views.append(
                ft.View("/settings",
                        [ft.AppBar(title=ft.Text("Главное меню"),
                                   bgcolor=ft.colors.SURFACE_VARIANT),
                         ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                             ft.ElevatedButton(width=line_width, height=30,
                                               text="✔️ Запись количества аккаунтов для реакций",
                                               on_click=lambda _: page.go("/recording_number_accounts_reactions")),

                             ft.Row([ft.ElevatedButton(width=270, height=30, text="✔️ Выбор реакций",
                                                       on_click=lambda _: page.go("/choice_of_reactions")),
                                     ft.ElevatedButton(width=270, height=30, text="✔️ Запись proxy",
                                                       on_click=lambda _: page.go("/proxy_entry"))]),

                             ft.ElevatedButton(width=line_width, height=30,
                                               text="✔️ Запись времени между сообщениями",
                                               on_click=lambda _: page.go("/recording_the_time_between_messages")),
                             ft.ElevatedButton(width=line_width, height=30,
                                               text="✔️ Время между инвайтингом, рассылка сообщений",
                                               on_click=lambda _: page.go("/time_between_invites_sending_messages")),

                             ft.Row([ft.ElevatedButton(width=270, height=30, text="✔️ Смена аккаунтов",
                                                       on_click=lambda _: page.go("/changing_accounts")),
                                     ft.ElevatedButton(width=270, height=30, text="✔️ Запись api_id, api_hash",
                                                       on_click=lambda _: page.go("/recording_api_id_api_hash"))]),

                             ft.Row([ft.ElevatedButton(width=270, height=30, text="✔️ Запись времени",
                                                       on_click=lambda _: page.go("/time_between_subscriptions")),
                                     ft.ElevatedButton(width=270, height=30, text="✔️  Запись сообщений",
                                                       on_click=lambda _: page.go("/message_recording"))]),

                             ft.Row([ft.ElevatedButton(width=270, height=30, text="✔️ Запись имени аккаунта",
                                                       on_click=lambda _: page.go("/record_your_account_name")),
                                     ft.ElevatedButton(width=270, height=30, text="✔️ Время между подпиской",
                                                       on_click=lambda _: page.go("/time_between_subscriptionss"))]),

                             ft.ElevatedButton(width=line_width, height=30, text="✔️ Запись ссылки для реакций",
                                               on_click=lambda _: page.go("/recording_reaction_link")),
                             ft.ElevatedButton(width=line_width, height=30,
                                               text="✔️ Формирование списка чатов / каналов",
                                               on_click=lambda _: page.go("/forming_list_of_chats_channels")),

                             ft.Row([ft.ElevatedButton(width=270, height=30, text="✔️ Запись ссылки",
                                                       on_click=lambda _: page.go("/link_entry")),
                                     ft.ElevatedButton(width=270, height=30, text="✔️ Лимиты на аккаунт",
                                                       on_click=lambda _: page.go("/account_limits"))]),

                             ft.Row([ft.ElevatedButton(width=270, height=30, text="✔️ Лимиты на сообщения",
                                                       on_click=lambda _: page.go("/message_limits")),
                                     ft.ElevatedButton(width=270, height=30, text="✔️ Смена типа устройства",
                                                       on_click=lambda _: page.go("/changing_device_type"))]),

                         ])]))
        elif page.route == "/recording_api_id_api_hash":  # ✔️ Запись api_id, api_hash
            writing_api_id_api_hash(page)
        elif page.route == "/changing_device_type":  # ✔️ Смена типа устройства
            record_device_type(page)
        elif page.route == "/message_limits":  # ✔️ Лимиты на сообщения
            record_setting(page, "message_limits", "Введите лимит на сообщения")
        elif page.route == "/account_limits":  # ✔️ Лимиты на аккаунт
            record_setting(page, "account_limits", "Введите лимит на аккаунт")
        elif page.route == "/link_entry":  # ✔️ Запись ссылки
            record_setting(page, "link_to_the_group", "Введите ссылку на группу")
        elif page.route == "/forming_list_of_chats_channels":  # ✔️ Формирование списка чатов / каналов
            output_the_input_field(page, DatabaseHandler())
        elif page.route == "/recording_reaction_link":  # ✔️ Запись ссылки для реакций
            recording_link_channel(page)
        elif page.route == "/recording_number_accounts_reactions":  # ✔️ Запись количества аккаунтов для реакций
            record_the_number_of_accounts(page)
        elif page.route == "/choice_of_reactions":  # ✔️ Выбор реакций
            reaction_gui(page)
        elif page.route == "/proxy_entry":  # ✔️ Запись времени между сообщениями
            creating_the_main_window_for_proxy_data_entry(page, DatabaseHandler())
        elif page.route == "/recording_the_time_between_messages":  # ✔️ Запись времени между сообщениями
            create_main_window(page, variable="time_sending_messages")
        elif page.route == "/time_between_invites_sending_messages":  # ✔️ Время между инвайтингом, рассылка сообщений
            create_main_window(page, variable="time_inviting")
        elif page.route == "/changing_accounts":  # ✔️ Смена аккаунтов
            create_main_window(page, variable="time_changing_accounts")
        elif page.route == "/time_between_subscriptions":  # ✔️ Запись времени
            recording_the_time_to_launch_an_invite_every_day(page)
        elif page.route == "/message_recording":  # ✔️ Запись сообщений
            recording_text_for_sending_messages(page)
        elif page.route == "/record_your_account_name":  # ✔️ Запись имени аккаунта
            record_setting(page, "account_name_newsletter", "Введите название аккаунта для отправки сообщений по чатам")
        elif page.route == "/time_between_subscriptionss":  # ✔️ Время между подпиской
            create_main_window(page, variable="time_subscription")
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=mainss)
