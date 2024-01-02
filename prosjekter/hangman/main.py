def hidden_word(word: str, characters_to_show: str):
    encoded_word = ""
    for char in word:
        if char in characters_to_show:
            encoded_word += char
        else:
            encoded_word += "_"
    return encoded_word

def print_status(word, lives_left, characters_guessed):
    print(f"Ordet: {word}")
    print(f"{lives_left} liv igjen")
    print(f"Bokstaver du har gjettet: {characters_guessed}")
    print()

def validate_guess(guess: str, characters_guessed: str):
    message, is_valid = "", True
    if guess in characters_guessed:
        message = f"Du har allerede gjettet {guess}"
        is_valid = False
    elif len(guess) != 1:
        message = "Du kan gjette kun en bokstav"
        is_valid = False
    
    return {"message": message, "is_valid": is_valid}

def check_if_won(characters_guessed, word_to_guess):
    return set(word_to_guess).issubset(set(characters_guessed))

def handle_wrong_guess(lives_left):
    print("Du gjettet feil!")
    lives_left -= 1
    if lives_left == 0:
        print("du tapte")
    return lives_left

def handle_correct_guess(characters_guessed, word_to_guess):
    print("Du gjettet riktig!")
    has_won = check_if_won(characters_guessed, word_to_guess)
    if has_won:
        print(f"Du vant! Ordet var {word_to_guess}")
        return True
    return False


def start_game():
    word_to_guess = "elephant"
    lives_left = 6
    characters_guessed = ""

    while lives_left > 0:
        encoded_word = hidden_word(word_to_guess, characters_guessed)
        print_status(encoded_word, lives_left, characters_guessed)

        guess = input("Gjett en bokstav: ")
        valid_status = validate_guess(guess)
        if not valid_status["is_valid"]:
            print(valid_status["message"])
            continue

        characters_guessed += guess

        if guess in word_to_guess:
            has_won = handle_correct_guess(characters_guessed, word_to_guess)
            if has_won:
                break
        else:
            lives_left = handle_wrong_guess(lives_left)


start_game()