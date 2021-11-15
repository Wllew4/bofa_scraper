from typing import TypedDict

class Transaction(TypedDict):
    date: str
    amount: float
    desc: str