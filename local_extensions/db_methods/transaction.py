import datetime

from local_extensions.db_methods.base import create_con
from local_extensions.models import Transaction, NewTransaction


async def get(user_id: int) -> list:
    con, cur = await create_con()
    await cur.execute('SELECT user_id, transaction_id, date_created, type_transaction, amount '
                      'FROM transactions WHERE user_id = %s', (user_id,))
    transactions = await cur.fetchall()
    await con.ensure_closed()
    return [Transaction(user_id=transaction[0],
                        transaction_id=transaction[1],
                        date_created=transaction[2],
                        type_transaction=transaction[3],
                        amount=transaction[4]) for transaction in transactions]


async def new(transaction: NewTransaction) -> Transaction:
    con, cur = await create_con()
    await cur.execute("INSERT INTO transactions (user_id, date_created, type_transaction, amount) "
                      "values (%s, %s, %s, %s)", (transaction.user_id, datetime.datetime.now(),
                                                  transaction.transaction_type, transaction.amount))
    await con.commit()
    lastrow = cur.lastrowid
    await cur.execute('SELECT user_id, transaction_id, date_created, type_transaction, amount '
                      'from transactions WHERE transaction_id = %s ', (lastrow,))
    full_transaction = await cur.fetchone()
    await con.ensure_closed()

    return Transaction(user_id=full_transaction[0],
                       transaction_id=full_transaction[1],
                       date_created=full_transaction[2],
                       type_transaction=full_transaction[3],
                       amount=full_transaction[4])
