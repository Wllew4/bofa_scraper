from .transaction import Transaction

class Account:
    name: str
    balance: float
    transactions: list[Transaction]

    def as_dict(self) -> dict:
        asDict: dict = dict()
        asDict["name"] = self.name
        asDict["balance"] = self.balance
        asDict["transactions"] = self.transactions
        return asDict

    def __str__(self) -> str:
        return self.as_dict.__str__()

    def __repr__(self) -> str:
        return self.__str__()