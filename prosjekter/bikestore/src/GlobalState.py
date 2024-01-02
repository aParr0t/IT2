import datetime
import json
from typing import List

import jsonpickle

from .Bike import Bike
from .Store import Store
from .User import User


class GlobalState:
    def __init__(self, init_file: str = "") -> None:
        self.users: List[User] = []
        self.active_user: User = None
        self.stores: List[Store] = []
        self.active_store: Store = None
        self.bike_types: List[Bike] = []
        self.time_offset: datetime.timedelta = datetime.timedelta(hours=0)
        if init_file:
            self.load(init_file)

    def get_time(self):
        return datetime.datetime.now() + self.time_offset

    def add_time(self, hours: int):
        self.time_offset += datetime.timedelta(hours=hours)

    def reset_time(self):
        self.time_offset = datetime.timedelta(hours=0)

    def load(self, filename: str):
        with open(filename, "r") as file:
            if len(file.read()) == 0:
                return  # don't load if file is empty
            file.seek(0)  # reset file pointer

            data = jsonpickle.decode(file.read())
            self.__dict__.update(data)

    def save(self, filename: str):
        with open(filename, "w") as file:
            frozen = jsonpickle.encode(self.__dict__)  # object to string
            frozen = json.loads(frozen)  # string to dict
            json.dump(frozen, file, indent=2)

    def add_store(self, name: str):
        new_store = Store(name)
        self.stores.append(new_store)
        return new_store

    def user_exists(self, name: str):
        for user in self.users:
            if user.name == name:
                return True
        return False

    def add_user(self, name: str):
        new_user = User(name)
        self.users.append(new_user)
        return new_user

    def set_active_user(self, user: User):
        self.active_user = user

    def get_user_by_name(self, name: str):
        return next(
            (u for u in self.users if u.name == name), None
        )  # copilot is insane

    def get_user_by_id(self, id: int):
        return next((u for u in self.users if u.id == id), None)  # copilot is insane

    def get_store(self, name: str):
        return next(
            (s for s in self.stores if s.name == name), None
        )  # copilot is insane

    def add_bike_type(self, name: str, description: str, hour_price: int):
        bike = Bike(name, description, hour_price)
        self.bike_types.append(bike)
        return bike

    def get_bike_type_by_name(self, name: str):
        return next((b for b in self.bike_types if b.name == name), None)

    def get_bike_type_by_id(self, id: int):
        return next((b for b in self.bike_types if b.id == id), None)

    def get_active_cart(self):
        return self.get_cart(self.active_user.id)

    def get_cart(self, id: int):
        return self.active_store.carts.get(str(id), [])

    def add_to_active_cart(self, item: dict):
        self.active_store.add_to_cart(self.active_user, item)

    def clear_active_cart(self):
        active_cart = self.get_active_cart()
        active_cart[:] = []

    def check_and_return_bikes(self):
        time = self.get_time()
        for store in self.stores:
            returneds = store.check_and_return_bikes(time)
            for returned in returneds:
                user = self.get_user_by_id(returned["user_id"])
                user.return_bike(returned["rental_bike_id"])

    def get_user_rentals(self, user: User):
        bikes = []
        for store in self.stores:
            bikes.extend([bike for bike in store.inventory if bike.renter == user])
        return bikes
