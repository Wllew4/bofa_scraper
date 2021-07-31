import json

class Transaction:
    data: tuple
    def __init__(self, date: str, amount: float, desc: str):
        self.data = (date, float(amount), desc)

    def getDate(self):
        return self.data[0]

    def getAmount(self):
        return self.data[1]

    def getDesc(self):
        return self.data[2]

    def toJSON(self):
        d = dict()
        d["date"] = self.getDate()
        d["amount"] = self.getAmount()
        d["desc"] = self.getDesc()
        return json.dumps(d)