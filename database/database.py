import asyncio
import pymysql
import aiomysql

from aiogram.types import Message

from config.config import Config, load_config

config: Config = load_config('.env')

loop = asyncio.get_event_loop()


async def add_user(message: Message, post: str = 'staff'):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password,
                                      db=config.database.database,
                                      loop=loop)
        async with conn.cursor() as cur:
            add_us = f'INSERT INTO all_users ' \
                     f"VALUES({message.from_user.id}, %s)"
            await cur.execute(add_us, post)
            if post == 'staff':
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


async def add_message_db(data: dict, id_user, chat_id):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password,
                                      db=config.database.database,
                                      loop=loop)
        async with conn.cursor() as cur:
            add_mess = f'INSERT INTO message_chat (id_message, text, id_user, chat_id)' \
                       f"VALUES('{data['id_massage']}', '{data['text']}', '{id_user}', '{chat_id}')"
            await cur.execute(add_mess)
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


def is_message():
    try:
        conn = pymysql.connect(host=config.database.host,
                               user=config.database.user,
                               password=config.database.password,

                               database=config.database.database)
        with conn.cursor() as cur:
            is_user = f"SELECT * FROM message_chat" \
                      f" WHERE request_message = 0"
            cur.execute(is_user)
            temp = cur.fetchone()
        conn.close()
        return temp

    except Exception as ex:
        print(ex)
        return None


async def add_message_db_hr(data: dict):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password,
                                      db=config.database.database,
                                      loop=loop)
        async with conn.cursor() as cur:
            add_mess = f'INSERT INTO request_chat (text, id_message, id_user)' \
                       f"VALUES('{data['text']}', '{data['id_massage']}', '{data['id_user']}')"
            await cur.execute(add_mess)
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


async def change_status_questions(data: dict):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password,
                                      db=config.database.database,
                                      loop=loop)
        async with conn.cursor() as cur:
            add_mess = f"UPDATE message_chat " \
                       f"SET request_message = true " \
                       f"WHERE id_message={data}"
            await cur.execute(add_mess)
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


async def add_week_one(message: Message, *adata: tuple):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password, db=config.database.database,
                                      loop=loop)
        async with conn.cursor() as cur:

            add_week = f'INSERT INTO '
    except Exception as ex:
        print(ex)


def page_prez(id: int):
    try:
        conn = conn = pymysql.connect(host=config.database.host,
                                      user=config.database.user,
                                      password=config.database.password,
                                      database=config.database.database)
        count: int
        with conn.cursor() as cur:
            page = f'SELECT count FROM staff ' \
                   f'WHERE id_staff={int(id)}'
            cur.execute(page)
            count = cur.fetchone()
        print(count)
        conn.close()
        return count[0]
    except Exception as ex:
        print(ex)


async def update(id: int, count: int):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password, db=config.database.database,
                                      loop=loop)
        async with conn.cursor() as cur:
            up = f'UPDATE staff SET count=%s WHERE id_staff={id}'
            await cur.execute(up, count)
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


def get_photo(count: int) -> str:
    try:
        conn = conn = pymysql.connect(host=config.database.host,
                                      user=config.database.user,
                                      password=config.database.password,
                                      database=config.database.database)
        string: str = ''
        with conn.cursor() as cur:
            get_id = f"SELECT file_id FROM slides " \
                     f"WHERE idslides=%s"
            cur.execute(get_id, count)
            string = cur.fetchone()
        conn.close()
        return str(string[0])
    except Exception as ex:
        print(ex)


def select_all_pages() -> int:
    try:
        conn = conn = pymysql.connect(host=config.database.host,
                                      user=config.database.user,
                                      password=config.database.password,
                                      database=config.database.database)
        count: int
        with conn.cursor() as cur:
            select = f'SELECT * FROM slides'
            cur.execute(select)
            count = len(cur.fetchall())
        print(count)
        conn.close()
        return count
    except Exception as ex:
        print(ex)


async def add_ban_list(id: int):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                        password=config.database.password, db=config.database.database,
                                        loop=loop)
        async with conn.cursor() as cur:
            string = f"INSERT INTO ban_list VALUES (%s, %s)"
            await cur.execute(string, (id, 'staff'))
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


def watch_ban_list():
    try:
        conn = conn = pymysql.connect(host=config.database.host,
                                      user=config.database.user,
                                      password=config.database.password,
                                      database=config.database.database)
        data: str = ''
        with conn.cursor() as cur:
            string = f"SELECT id_user FROM ban_list WHERE post='staff'"
            cur.execute(string)
            data = cur.fetchone()
        conn.close()
        print(data)
        return int(data[0])
    except Exception as ex:
        print(ex)


async def update_ban_list(*data):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password, db=config.database.database,
                                      loop=loop)
        async with conn.cursor() as cur:
            if data[0]['apply'] == "Да":
                string = f"DELETE FROM ban_list WHERE id_user=%s"
                await cur.execute(string, int(data[0]['person']))
                string = f"UPDATE all_users SET post=%s WHERE id_user=%s"
                await cur.execute(string, ('staff', int(data[0]['person'])))
                await conn.commit()
            else:
                string = f"UPDATE ban_list SET post=%s WHERE id_user=%s"
                await cur.execute(string, ('ban', int(data[0]['person'])))
                string = f"UPDATE all_users SET post=%s WHERE id_user=%s"
                await cur.execute(string, ('ban', int(data[0]['person'])))
                await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


async def is_correct_quest(*data):
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password, db=config.database.database,
                                      loop=loop)
        count: int = 0
        async with conn.cursor() as cur:
            string = f"SELECT * FROM quest WHERE id_quest=1"
            await cur.execute(string)
            string = await cur.fetchall()
            print(string[0])
            for d in data[0]:
                if data[0][d] in string[0]:
                    count += 1
            string = f"UPDATE staff SET pound=%s"
            print(count, count / 5)
            await cur.execute(string, (count / 5))
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


def result_test(id: int) -> str:
    try:
        conn = conn = pymysql.connect(host=config.database.host,
                                      user=config.database.user,
                                      password=config.database.password,
                                      database=config.database.database)
        data: str = ''
        with conn.cursor() as cur:
            string = f"SELECT pound FROM staff WHERE id_staff=%s"
            cur.execute(string, id)
            data = cur.fetchone()
        conn.close()
        print("data = ", data)
        return data[0]
    except Exception as ex:
        print(ex)