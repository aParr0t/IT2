import random


class Bike:
    def __init__(self, name: str, description: str, hour_price: int, id: int = None):
        self.id = id or random.randint(0, 1000000)
        self.name = name
        self.description = description
        self.hour_price = hour_price

    def __repr__(self):
        return f"Bike({self.name}, {self.description[:10]}..., {self.hour_price})"
