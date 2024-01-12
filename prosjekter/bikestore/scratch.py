def custom_max(a, b):
    if a > b:
        return a

    if b > a:
        return b
    else:
        print("begge verdiene er like")


largest = custom_max(10, 5)
