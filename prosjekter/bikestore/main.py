import traceback

from src.App import App

if __name__ == "__main__":
    app = App()
    app.run()

# todo
# - add parameter called "alternative" to go_back() that points to some other
#   function for handling cases when the history is empty, but the page should
#   still point to some other page
# - add a reusable screen function for loading animations. should have
#   customizable text like "bygger butikk...", "laster inn butikk...", "laster inn bruker ...".
# - there's a lot of code duplication for screens that allow the user
#       to go back to the previous screen
# - refactor long chains like self.global_state.active_user.name into custom functions
# - create a class CartItem that contains a Bike and a quantity, to_date, from_date, etc.
# - there are too many functions of the form "get_bike_by_id" and "get_user_by_id".
#   create a function that queries a list of objects by properties
