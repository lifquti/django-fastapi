import datetime

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    user_id: int
    transaction_id: int
    date_created: datetime.datetime
    type_transaction: str
    amount: float


class User:
    user_id: int
    username: str

    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username


class NewUser(BaseModel):
    user_id: int


class GetUser(BaseModel):
    user_id: int
    username: str
    transactions: list[Transaction]


class Create(BaseModel):
    username: str = Field(
        description="Уникальный юзернейм пользователя"
    )


class Get(BaseModel):
    user_id: int = Field(
        description="Уникальный id пользователя"
    )


class NewTransaction(BaseModel):
    user_id: int
    transaction_type: str
    amount: float

