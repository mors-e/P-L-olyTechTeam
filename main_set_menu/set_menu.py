from aiogram import Dispatcher, types


async def set_main_menu(dp: Dispatcher) -> None:
    main_menu_commands = [
        types.BotCommand(command="/start", description="Начало работы с ботом и начало анкетирования для работника"),
        types.BotCommand(command="/begin", description="Просмотреть пример чекпоинта road map"),
        types.BotCommand(command="/cancel", description="Отменить анкетирование"),
        types.BotCommand(command="/feedback", description="чат от имени staff"),
        types.BotCommand(command="/start_request", description="чат от имени hr")
    ]
    await dp.bot.set_my_commands(main_menu_commands)