import logging
from functools import wraps
from json import JSONDecodeError

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from starlette.requests import Request

import db_methods.user
import local_extensions.db_methods.user
from local_extensions.models import Create, NewUser, Get, GetUser, Transaction, NewTransaction

formatted_router = APIRouter()
token_auth_scheme = HTTPBearer()


def check_credentials(f):
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        data = request.headers.get('Authorization')
        if data is None:
            raise HTTPException(401, detail='Please check the entry of the api key in the Authorization header ')

        if data.split(" ")[1] != '$HIG#IRHRF#gn3ljpgHEIROF42IGHPOWJF':
            raise HTTPException(401, detail='Please check the entry of the api key in the Authorization header ')
        return await f(request, *args, **kwargs)

    return decorated_function


@formatted_router.post("/add_user", tags=["Додати юзера"], response_model=NewUser, status_code=201)
@check_credentials
async def add_user(request: Request, data: Create):
    try:
        json_data = await request.json()
    except JSONDecodeError:
        raise HTTPException(400, detail='Please send a valid json')

    username = json_data.get("username")

    if username is None:
        raise HTTPException(400, detail='Please send a valid parametr of username')

    record_id = await local_extensions.db_methods.user.get(username)
    if record_id:
        raise HTTPException(400, detail='User exist')
    user_id = await local_extensions.db_methods.user.create(username)
    return NewUser(user_id=user_id)


@formatted_router.post("/get_user", tags=["Дані користувача"], response_model=GetUser, status_code=200)
@check_credentials
async def get_user(request: Request, data: Get):
    try:
        json_data = await request.json()
    except JSONDecodeError:
        raise HTTPException(400, detail='Please send a valid json')

    user_id = json_data.get("user_id")
    user = await local_extensions.db_methods.user.get_by_record(user_id)
    if not user:
        raise HTTPException(400, detail='User does not exist')
    transactions = await local_extensions.db_methods.transaction.get(user_id)
    return GetUser(user_id=user_id, username=user.username, transactions=transactions)


@formatted_router.get("/get_all_users", tags=["Всі користувачі та дані"], response_model=list[GetUser], status_code=200)
@check_credentials
async def get_all_users():
    all_users = await db_methods.user.get_all()
    new_list = []

    for user in all_users:
        transaction = await db_methods.transaction.get(user.user_id)
        new_list.append(GetUser(user_id=user.user_id, username=user.username, transactions=transaction))
    return new_list


@formatted_router.post("/add_transactions", tags=["Додати транзакцію"], response_model=Transaction, status_code=201)
@check_credentials
async def add_transaction(request: Request, data: NewTransaction):
    try:
        json_data = await request.json()
    except JSONDecodeError:
        raise HTTPException(400, detail='Please send a valid json')
    try:
        transaction = NewTransaction(
            user_id=json_data["user_id"],
            transaction_type=json_data["transaction_type"],
            amount=json_data["amount"])
    except Exception as e:
        logging.error(e)
        raise HTTPException(400, detail='Please send a valid json')
    data = await db_methods.transaction.new(transaction)
    return data
