import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config.config import Config, load_config
from handlers.handlers_main import register_handlers_main
from handlers.fsw import register_fsm_handlers
from chat.command_staff import register_chat_commands_staff
from chat.command_hr import register_chat_commands_hr

logger = logging.getLogger(__name__)
storage: RedisStorage2 = RedisStorage2()


def register_all_handlers(dp: Dispatcher) -> None:
    register_handlers_main(dp)
    register_fsm_handlers(dp)
    register_chat_commands_staff(dp)
    register_chat_commands_hr(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting Bot")

    config: Config = load_config('.env')

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot, storage=storage)

    #await set_main_menu(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.closed()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')