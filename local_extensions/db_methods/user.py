import datetime
from dataclasses import dataclass
from typing import Optional

from local_extensions.db_methods.base import create_con
from models import User


async def get(username: str) -> Optional[int]:
    con, cur = await create_con()
    await cur.execute(
        "select record_id from user where user_name = %s",
        (username,),
    )
    record = await cur.fetchone()
    await con.ensure_closed()
    if record is None:
        return None
    return record[0]


async def create(username: str) -> int:
    con, cur = await create_con()
    await cur.execute("insert into user(user_name, date_created) values (%s, %s)", (username, datetime.datetime.now()))
    await con.commit()
    await cur.execute("select record_id from user where user_name = %s",(username,))
    record = await cur.fetchone()
    await con.ensure_closed()
    return record[0]


async def get_by_record(user_id: int) -> Optional[User]:
    con, cur = await create_con()
    await cur.execute("select record_id, user_name from user where record_id = %s", (user_id, ))
    data = await cur.fetchone()
    await con.ensure_closed()
    if data is None:
        return None
    return User(*data)


async def get_all() -> list[User]:
    con, cur = await create_con()
    await cur.execute("select record_id, user_name from user")
    records = await cur.fetchall()
    await con.ensure_closed()
    return [User(*record) for record in records]
