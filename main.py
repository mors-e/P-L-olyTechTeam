import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config.config import Config, load_config

logger = logging.getLogger(__name__)


def register_all_handlers(dp: Dispatcher) -> None:
    pass


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting Bot")

    storage: RedisStorage2 = RedisStorage2()

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