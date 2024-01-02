import datetime
import time

from InquirerPy import prompt
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from .GlobalState import GlobalState


class ScreenManager:
    def __init__(self, global_state: GlobalState, clear_display: bool):
        self.screens = {}
        self.global_state = global_state
        self.clear_display = clear_display
        self.history: list[str] = []
        self.start_screen: callable

    def _clear_display(self):
        if self.clear_display:
            n = 999
            print(f"\033[{n}F\033[0J", end="")

    def set_start_screen(self, function: callable):
        self.start_screen = function
    
    def start(self):
        to_run: callable = self.start_screen
        previous_function = None
        while to_run:
            self._clear_display()
            self.global_state.check_and_return_bikes()
            self.global_state.save("data.json")
        
            # handle history circular buffer
            if previous_function:
                history_names = [h.__name__ for h in self.history]
                if previous_function.__name__ in history_names:
                    self.history = self.history[: self.history.index(previous_function) + 1]
                else:
                    self.history.append(previous_function)

            previous_function = to_run
            to_run: callable = to_run()
 
    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            return self.history.pop()

    def stay(self):
        return self.history[-1]

    # region screens
    def _start_screen_function(self):
        questions = [
            {
                "type": "list",
                "message": "Hvordan vil du logge inn:",
                "name": "choices",
                "choices": [
                    "Logg inn som kunde",
                    "Logg inn på butikk",
                    "Logg inn som admin",
                ],
            },
        ]
        results = prompt(questions)

        if results["choices"] == "Logg inn som kunde":
            return self._user_sign_in_screen_function
        elif results["choices"] == "Logg inn på butikk":
            return self._store_sign_in_screen_function
        elif results["choices"] == "Logg inn som admin":
            return self._admin_screen_function

    def _user_sign_in_screen_function(self):
        questions = [
            {
                "type": "input",
                "message": "Skriv inn navn:",
                "name": "name",
            },
        ]
        name = prompt(questions)["name"]
        state = self.global_state
        does_user_exists = state.user_exists(name)
        if does_user_exists:
            self.props = {"user": state.get_user_by_name(name)}
            return self._sign_in_animation_screen_function
        else:
            self.props = {"name": name}
            return self._create_new_user_screen_function

    def _create_new_user_screen_function(self):
        questions = [
            {
                "type": "list",
                "message": "Denne brukeren finnes ikke fra før, vil du opprette en ny?",
                "name": "choice",
                "choices": [
                    "Ja",
                    "Nei (gå tilbake)",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Ja":
            user = self.global_state.add_user(self.props["name"])
            self.props = {"user": user}
            return self._sign_in_animation_screen_function
        elif choice == "Nei (gå tilbake)":
            return self.go_back

    def _sign_in_animation_screen_function(self):
        for i in range(3):
            print("Logger inn" + "." * i, end="\r")
            time.sleep(0.5)
        self.global_state.set_active_user(self.props["user"])
        return self._user_screen_function

    def _user_screen_function(self):
        username = self.global_state.active_user.name
        questions = [
            {
                "type": "list",
                "message": f"Du er logget inn som \"{username}\". Dine valg:",
                "name": "choice",
                "choices": [
                    "Velg butikk",
                    "Se historikk",
                    "Se mine sykler",
                    "Logg ut (gå tilbake)",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Logg ut (gå tilbake)":
            return self._start_screen_function
        elif choice == "Velg butikk":
            return self._user_pick_store_screen_function
        elif choice == "Se historikk":
            for history_item in self.global_state.active_user.history:
                print(history_item)
            print()
            input("Trykk enter for å gå tilbake")
            return self.stay
        elif choice == "Se mine sykler":
            user = self.global_state.active_user
            rental_bikes = self.global_state.get_user_rentals(user)
            bikes = []
            for rental_bike in rental_bikes:
                bike = self.global_state.get_bike_type_by_id(rental_bike.bike_id)
                bikes.append(
                    {
                        "name": bike.name,
                        "from_date": rental_bike.from_date,
                        "to_date": rental_bike.to_date,
                    }
                )
            for bike in bikes:
                from_date = bike["from_date"].strftime("%d.%m.%Y %H:%M")
                to_date = bike["to_date"].strftime("%d.%m.%Y %H:%M")
                print(f"{bike['name']} fra {from_date} til {to_date}")
            print()
            input("Trykk enter for å gå tilbake")
            return self.stay

    def _admin_screen_function(self):
        questions = [
            {
                "type": "list",
                "message": f"Du er logget inn som admin",
                "name": "choice",
                "choices": [
                    "Legge til sykkeltype",
                    "Sjekke sykkeltyper",
                    "Spol tid fremover",
                    "Sjekk brukere",
                    "Logg ut (gå tilbake)",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Legge til sykkeltype":
            return self._add_bike_type_screen_function
        elif choice == "Sjekke sykkeltyper":
            print("Sykkeltyper:")
            for bike_type in self.global_state.bike_types:
                print(bike_type)
            print()
            input("Trykk enter for å gå tilbake")
            return self.stay
        elif choice == "Spol tid fremover":
            return self._admin_time_screen_function
        elif choice == "Sjekk brukere":
            print("Brukere:")
            for user in self.global_state.users:
                print(user)
            print()
            input("Trykk enter for å gå tilbake")
            return self.stay
        elif choice == "Logg ut (gå tilbake)":
            return self.go_back

    def _admin_time_screen_function(self):
        print("Tid:", self.global_state.get_time().strftime("%d.%m.%Y %H:%M"))
        questions = [
            {
                "type": "list",
                "message": "Hva vil du gjøre?",
                "name": "choice",
                "choices": [
                    "Spol fremover",
                    "Reset tid",
                    "Gå tilbake",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Gå tilbake":
            return self.go_back
        elif choice == "Reset tid":
            offset = self.global_state.get_time() - datetime.datetime.now()
            seconds = datetime.timedelta.total_seconds(offset)
            days = seconds // (24 * 3600)
            hours = (seconds % (24 * 3600)) // 3600
            minutes = (seconds % 3600) // 60
            print(f"Resetet tiden med {days} dager, {hours} timer og {minutes} minutter")
            self.global_state.reset_time()
            time.sleep(1)
            return self.stay
        elif choice == "Spol fremover":
            questions = [
                {
                    "type": "input",
                    "message": "Antall timer å spole fremover (uttrykk tillatt):",
                    "name": "hours",
                },
            ]
            hours = eval(prompt(questions)["hours"])
            self.global_state.add_time(hours)
            print(f"Spolte fremover {hours} timer")
            time.sleep(1)
            return self.stay


    def _user_pick_store_screen_function(self):
        state = self.global_state
        stores = [s.name for s in state.stores]

        questions = [
            {
                "type": "list",
                "message": f"Dine valg:",
                "name": "choice",
                "choices": [*stores, "Logg ut (gå tilbake)"],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Logg ut (gå tilbake)":
            return self.go_back
        else:
            store_name = choice
            state.active_store = state.get_store(store_name)
            return self._user_store_screen_function

    def _user_store_screen_function(self):
        questions = [
            {
                "type": "list",
                "message": f"Dine valg:",
                "name": "choice",
                "choices": [
                    "Vis ledige sykler",
                    "Vis handlekurv",
                    "Logg ut (gå tilbake)",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Logg ut (gå tilbake)":
            return self.go_back
        elif choice == "Vis ledige sykler":
            return self._available_bikes_screen_function
        elif choice == "Vis handlekurv":
            return self._shopping_cart_screen_function

    def _shopping_cart_screen_function(self):
        shopping_cart = self.global_state.get_active_cart()
        bike_names = []
        for item in shopping_cart:
            bike_name = self.global_state.get_bike_type_by_id(item["bike_id"]).name
            bike_names.append(bike_name)
        
        if bike_names:
            longest_name = max([len(name) for name in bike_names])
        else:
            longest_name = 0

        items = []
        for item, name in zip(shopping_cart, bike_names):
            choice = Choice(item["rental_bike_id"], f"{name:<{longest_name+3}} {item["price"]:<7} kr")
            items.append(choice)
        
        choices = [*items, "Gå tilbake"]
        if len(choices) > 1:
            choices.append("Gå til kassen")
        questions = [
            {
                "type": "list",
                "message": "Handlekurven din (velg element for å slette):",
                "name": "choice",
                "choices": choices,
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Gå tilbake":
            return self.go_back
        elif choice == "Gå til kassen":
            return self._checkout_screen_function
        else:
            # remove item form cart
            cart = self.global_state.get_active_cart()
            for i, item in enumerate(cart):
                if item["rental_bike_id"] == choice:
                    print(f"Fjernet {item['bike_name']} fra handlekurven")
                    del cart[i]
                    break
            input("Trykk enter for å gå tilbake")
            return self.stay

    def _checkout_screen_function(self):
        shopping_cart = self.global_state.get_active_cart()
        pre_discount_price = sum([item["price"] for item in shopping_cart])

        discount = 0
        if len(shopping_cart) >= 3:
            discount = 0.3 * pre_discount_price

        total_price = pre_discount_price - discount

        bike_names = []
        for item in shopping_cart:
            bike_name = self.global_state.get_bike_type_by_id(item["bike_id"]).name
            bike_names.append(bike_name)
        longest_name = max([len(name) for name in bike_names])

        bikes = []
        for item in shopping_cart:
            from_date = item["from_date"].strftime("%d.%m.%Y %H:%M")
            to_date = item["to_date"].strftime("%d.%m.%Y %H:%M")
            price = f"{item["price"]:>15} kr"
            bikes.append(
                f"{item['bike_name']:<{longest_name}} {price}\n          fra {from_date} til {to_date}"
            )
        bikes = "\n".join(bikes)
        questions = [
            {
                "type": "list",
                "message": f"""
Oppsummering:\n
Sykler:\n
{bikes}\n
--------------------------------\n
Rabatt (3+ sykler): {discount} kr\n
--------------------------------\n
Totalpris: {total_price} kr\n""",
                "name": "choice",
                "choices": [
                    "Bekreft og betal",
                    "Avbryt",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Bekreft og betal":
            return self._payment_screen_function
        elif choice == "Avbryt":
            return self._user_store_screen_function

    def _create_store_screen_function(self):
        questions = [
            {
                "type": "input",
                "message": "Butikknavn:",
                "name": "name",
            },
        ]
        data = prompt(questions)
        self.global_state.add_store(data["name"])
        return self.go_back

    def _payment_screen_function(self):
        questions = [
            {
                "type": "list",
                "message": "Betal med:",
                "name": "choice",
                "choices": [
                    "Vipps",
                    "Kort",
                    "Gå tilbake",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Kort":
            return self._payment_card_screen_function
        elif choice == "Vipps":
            print("Vipps til dette nummeret: 12345678")
            input("Trykk Enter når du har vippset")
            return self._payment_complete_screen_function
        elif choice == "Gå tilbake":
            return self.go_back

    def _payment_card_screen_function(self):
        questions = [
            {
                "type": "input",
                "message": "Kortnummer:",
                "name": "card_number",
            },
            {
                "type": "input",
                "message": "Navn på kortholder:",
                "name": "card_name",
            },
            {
                "type": "input",
                "message": "MM/ÅÅ:",
                "name": "card_expiry",
            },
            {
                "type": "input",
                "message": "CVC:",
                "name": "card_cvc",
            },
        ]
        data = prompt(questions)
        self.props = data
        return self._payment_complete_screen_function

    def _payment_complete_screen_function(self):
        print("Betaling gjennomført!")
        shopping_cart = self.global_state.get_active_cart()
        store = self.global_state.active_store
        for item in shopping_cart:
            rental_bike_id = item["rental_bike_id"]
            store.rent(rental_bike_id, self.global_state.active_user, item["from_date"], item["to_date"])
            self.global_state.active_user.save_to_history(
                rental_bike_id,
                item["bike_id"],
                item["bike_name"],
                item["from_date"],
                item["to_date"],
                item["price"],
                "rent",
            )


        time.sleep(1)
        self.global_state.clear_active_cart()
        return self._user_store_screen_function

    def _store_sign_in_screen_function(self):
        questions = [
            {
                "type": "list",
                "message": f"Dine valg:",
                "name": "choice",
                "choices": ["Lag ny butikk", "Velg butikk", "Logg ut (gå tilbake)"],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Lag ny butikk":
            return self._create_store_screen_function
        elif choice == "Velg butikk":
            return self._store_pick_store_screen_function
        elif choice == "Logg ut (gå tilbake)":
            return self.go_back

    def _store_pick_store_screen_function(self):
        state = self.global_state
        stores = [s.name for s in state.stores]

        questions = [
            {
                "type": "list",
                "message": f"Dine valg:",
                "name": "choice",
                "choices": [*stores, "Logg ut (gå tilbake)"],
            },
        ]
        store_name = prompt(questions)["choice"]
        if store_name == "Logg ut (gå tilbake)":
            return self.go_back
        else:
            state.active_store = state.get_store(store_name)
            return self._store_screen_function

    def _store_screen_function(self):
        store_name = self.global_state.active_store.name
        questions = [
            {
                "type": "list",
                "message": f"Logget inn som {store_name}. Dine valg:",
                "name": "choice",
                "choices": [
                    "Vis lagerbeholdning",
                    "Endre lagerbeholdning",
                    "Logg ut (gå tilbake)",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Logg ut (gå tilbake)":
            return self.go_back
        elif choice == "Vis lagerbeholdning":
            print("Lagerbeholdning:")
            rentalBikes = self.global_state.active_store.inventory
            for rentalBike in rentalBikes:
                name = self.global_state.get_bike_type_by_id(rentalBike.bike_id).name
                available = "Ledig" if rentalBike.is_available else "Utleid"
                print(f"{name}, status: {available}")
            print()
            input("Trykk enter for å gå tilbake")
            return self.stay
        elif choice == "Endre lagerbeholdning":
            return self._change_stock_screen_function

    def _add_bike_type_screen_function(self):
        questions = [
            {
                "type": "input",
                "message": "Sykkeltype:",
                "name": "name",
            },
            {
                "type": "input",
                "message": "Beskrivelse:",
                "name": "description",
            },
            {
                "type": "input",
                "message": "Pris/time:",
                "name": "hour_price",
            },
        ]
        data = prompt(questions)
        data["hour_price"] = int(data["hour_price"])
        self.global_state.add_bike_type(**data)
        return self.go_back

    def _change_stock_screen_function(self):
        state = self.global_state
        store = state.active_store
        bike_names = [b.name for b in state.bike_types]
        questions = [
            {
                "type": "list",
                "message": "Hvilken sykkeltype vil du legge til?",
                "name": "bike_name",
                "choices": bike_names,
            },
            {
                "type": "input",
                "message": "Hvor mange vil du legge til?",
                "name": "quantity",
            },
        ]
        choices = prompt(questions)
        bike_name = choices["bike_name"]
        bike_id = self.global_state.get_bike_type_by_name(bike_name).id
        quantity = int(choices["quantity"])
        store.add_inventory(bike_id, quantity)
        return self.go_back

    def _available_bikes_screen_function(self):
        rentableBikes = self.global_state.active_store.get_available_bikes()
        bike_ids = [rentableBike.bike_id for rentableBike in rentableBikes]
        bikes = []
        for bike_id in set(bike_ids):
            bike = self.global_state.get_bike_type_by_id(bike_id)
            count = bike_ids.count(bike_id)
            bikes.append(f"({count}x) {bike.name} ({bike.hour_price} kr/t)")

        questions = [
            {
                "type": "list",
                "message": "Hvilken sykkel vil du leie?",
                "name": "bike_name",
                "choices": [*bikes, "Gå tilbake"],
            },
        ]
        choice = prompt(questions)["bike_name"]
        if choice == "Gå tilbake":
            return self.go_back
        else:
            bike_name = choice[choice.index(")") + 2 : choice.rfind("(") - 1]
            bike_id = self.global_state.get_bike_type_by_name(bike_name).id
        questions = [
            {
                "type": "list",
                "message": "Velg tidsintervall",
                "name": "time_interval",
                "choices": [
                    "timer",
                    "dager",
                    "uker",
                ],
            },
        ]
        time_interval = prompt(questions)["time_interval"]
        
        questions = [
            {
                "type": "input",
                "message": f"Hvor mange {time_interval} vil du leie?",
                "name": "duration",
            },
        ]
        duration = int(prompt(questions)["duration"])

        price = calculate_price(self.global_state, bike_name, duration, time_interval)

        from_date = self.global_state.get_time()
        total_hours = duration_to_hours(duration, time_interval)
        to_date = from_date + datetime.timedelta(hours=total_hours)
        from_date_formated = from_date.strftime("%d.%m.%Y %H:%M")
        to_date_formated = to_date.strftime("%d.%m.%Y %H:%M")

        questions = [
            {
                "type": "list",
                "message": f"""Oppsummering:\n
                Sykkeltype: {bike_name}\n
                Fra: {from_date_formated}\n
                Til: {to_date_formated}\n
                --------------------------------\n
                Pris: {price} kr\n""",
                "name": "choice",
                "choices": [
                    "Bekreft og legg til i handlekurv",
                    "Avbryt",
                ],
            },
        ]
        choice = prompt(questions)["choice"]
        if choice == "Bekreft og legg til i handlekurv":
            rental_bike_id = [b.id for b in rentableBikes if b.bike_id == bike_id and b.is_available][0]
            print("rental_bike_id")
            print(rental_bike_id)
            item = {
                "rental_bike_id": rental_bike_id,
                "bike_id": bike_id,
                "bike_name": bike_name,
                "from_date": from_date,
                "to_date": to_date,
                "price": price,
            }
            self.global_state.add_to_active_cart(item)
            return self._user_store_screen_function
        elif choice == "Avbryt":
            return self._user_store_screen_function

# endregion screens


def duration_to_hours(duration: int, time_interval: str):
    if time_interval == "timer":
        return duration
    elif time_interval == "dager":
        return duration * 24
    elif time_interval == "uker":
        return duration * 24 * 7


def calculate_price(
    global_state: GlobalState, bike_name: str, duration: int, time_interval: str
):
    bike = global_state.get_bike_type_by_name(bike_name)
    base_hour_price = bike.hour_price

    hours = duration_to_hours(duration, time_interval)
    if time_interval == "timer":
        scale = 1
    elif time_interval == "dager":
        scale = 0.8
    elif time_interval == "uker":
        scale = 0.6

    return base_hour_price * hours * scale
