import datetime
import random

from .Bike import Bike
from .User import User


class RentableBike:
    def __init__(
        self,
        bike_id: int,
        is_available: bool = True,
        id: int = None,
        renter: User = None,
        from_date: datetime = None,
        to_date: datetime = None,
    ):
        self.id = id or random.randint(0, 1000000)
        self.bike_id = bike_id
        self.is_available = is_available
        self.renter = renter
        self.from_date = from_date
        self.to_date = to_date

    def __repr__(self):
        return f"RentableBike(name: {self.bike_id}, is_available: {self.is_available})"


class Store:
    def __init__(
        self,
        name: str,
        inventory: list[Bike] = None,
        carts: dict = None,
        id: int = None,
    ):
        self.id = id or random.randint(0, 1000000)
        self.name = name
        self.inventory: list[RentableBike] = inventory or []
        self.carts = carts or {}

    def __repr__(self):
        return f"Store({self.name}, {self.inventory})"

    def add_to_cart(self, user: User, item: dict):
        user_id = str(user.id)
        if user_id not in self.carts:
            self.carts[user_id] = []
        self.carts[user_id].append(item)

    def add_inventory(self, bike_id: int, quantity: int = 1):
        for i in range(quantity):
            self.inventory.append(RentableBike(bike_id))

    def get_available_bikes(self):
        print("available bikes:")
        print([bike for bike in self.inventory if bike.is_available])
        return [bike for bike in self.inventory if bike.is_available]

    def rent(
        self, rental_bike_id: int, user: User, from_date: datetime, to_date: datetime
    ):
        bike = next(
            (bike for bike in self.inventory if bike.id == rental_bike_id), None
        )
        bike.is_available = False
        bike.renter = user
        bike.from_date = from_date
        bike.to_date = to_date

    def return_bike(self, rental_bike_id: int):
        bike = next(
            (bike for bike in self.inventory if bike.id == rental_bike_id), None
        )
        bike.is_available = True
        bike.renter = None
        bike.from_date = None
        bike.to_date = None

    def check_and_return_bikes(self, time: datetime) -> list[dict]:
        returns = []
        for bike in self.inventory:
            if not bike.is_available and time > bike.to_date:
                returns.append({"user_id": bike.renter.id, "rental_bike_id": bike.id})
                self.return_bike(bike.id)
        return returns
