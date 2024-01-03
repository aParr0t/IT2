from src.App import App

if __name__ == "__main__":
    app = App()
    app.run()

# todo
# - there's a lot of code duplication for screens that allow the user
#       to go back to the previous screen
# - create a class CartItem that contains a Bike and a quantity, to_date, from_date, etc.
# - there are too many functions of the form "get_bike_by_id" and "get_user_by_id".
#   create a function that queries a list of objects by properties
