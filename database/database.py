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
                     f"VALUES({message.from_user.id}, 'staff')"
            await cur.execute(add_us)
            add_us = f'INSERT INTO staff ' \
                     f'VALUES({message.from_user.id})'
            await cur.execute(add_us)
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)
    finally:
        print("Юзер уже добавлен")


def is_staff_user(id: int) -> str:
    try:
        conn = pymysql.connect(host=config.database.host,
                               user=config.database.user,
                               password=config.database.password,
                               database=config.database.database)
        temp: str
        with conn.cursor() as cur:
            is_user = f"SELECT post FROM all_users" \
                      f" WHERE id_user={id}"
            cur.execute(is_user)
            temp = cur.fetchone()[0]
        conn.close()
        return temp
    except Exception as ex:
        print(ex)
        return "none"