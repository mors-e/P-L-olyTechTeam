from aiogram import Dispatcher, types


async def set_main_menu(dp: Dispatcher) -> None:
    main_menu_commands = [
        types.BotCommand(command="/start_test", description="Начало анкетирования для работника"),
        types.BotCommand(command="/begin", description="Просмотреть пример чекпоинта road map"),
        types.BotCommand(command="/cancel", description="Отменить анкетирование"),
        types.BotCommand(command="/feedback", description="чат от имени staff"),
        types.BotCommand(command="/start_request", description="чат от имени hr"),
        types.BotCommand(command="ban_list", description="Посмотреть заявки на статус сотрудника")
    ]
    await dp.bot.set_my_commands(main_menu_commands)