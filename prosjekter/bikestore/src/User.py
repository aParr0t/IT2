import copy
import random


class HistoryItem:
    def __init__(
        self,
        user_id: int,
        rental_bike_id: int,
        bike_id: int,
        bike_name: str,
        from_date: str,
        to_date: str,
        price: int,
        action: str,
    ):
        self.user_id = user_id
        self.rental_bike_id = rental_bike_id
        self.bike_id = bike_id
        self.bike_name = bike_name
        self.from_date = from_date
        self.to_date = to_date
        self.price = price
        self.action = action

    def __repr__(self):
        return f"HistoryItem({self.user_id}, {self.bike_id}, {self.bike_name}, {self.from_date}, {self.to_date}, {self.price})"

    def __str__(self):
        divider = "----------------------------------------"
        return f"{divider}\nAction: {self.action}\nBike: {self.bike_id}\nFrom: {self.from_date}\nTo: {self.to_date}\nPrice: {self.price}\n"


class User:
    def __init__(self, name: str, id: int = None):
        self.id = id or random.randint(0, 1000000)
        self.name = name
        self.history: list[HistoryItem] = []

    def __repr__(self):
        return f"User({self.id}, {self.name})"

    def save_to_history(
        self,
        rental_bike_id: int,
        bike_id: int,
        bike_name: str,
        from_date: str,
        to_date: str,
        price: int,
        action: str,
    ):
        h = HistoryItem(
            self.id,
            rental_bike_id,
            bike_id,
            bike_name,
            from_date,
            to_date,
            price,
            action,
        )
        self.history.append(h)

    def return_bike(self, rental_bike_id: int):
        history_item = next(
            (x for x in self.history if x.rental_bike_id == rental_bike_id)
        )
        history_item = copy.deepcopy(history_item).__dict__
        del history_item["user_id"]
        history_item["action"] = "return"

        self.save_to_history(**history_item)
