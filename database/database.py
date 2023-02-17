import asyncio
import pymysql
import aiomysql

from aiogram.types import Message, CallbackQuery

from config.config import Config, load_config

config: Config = load_config('.env')

loop = asyncio.get_event_loop()


async def add_user(message: Message):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password,
                                      db=config.database.database,
                                      loop=loop)
        async with conn.cursor() as cur:
            add_us = f'INSERT INTO all_users ' \
                     f'VALUES({message.from_user.id}, `staff`)'
            await cur.execute(add_us)
            add_us = f'INSERT INTO staff ' \
                     f'VALUES({message.from_user.id})'
            await cur.execute(add_us)
            await cur.commit()
        conn.close()
    except Exception as ex:
        print(ex)
    finally:
        print("Юзер уже добавлен")