class Game:
    _rolls = [0] * 21
    _current_roll = 0

    def roll(self, pins):
        self._rolls[self._current_roll] = pins
        self._current_roll += 1

    def score(self):
        score = 0
        frame_index = 0
        for frame in range(0, 10):
            if self._is_strike(frame_index):
                score += 10 + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                score += self._rolls[frame_index] + self._rolls[frame_index + 1]
                frame_index += 2
        return score

    def _sum_of_balls_in_frame(self, frame_index):
        return self._rolls[frame_index] + self._rolls[frame_index + 1]

    def _spare_bonus(self, frame_index):
        return self._rolls[frame_index + 2]

    def _strike_bonus(self, frame_index):
        return self._rolls[frame_index + 1] + self._rolls[frame_index + 2]

    def _is_spare(self, frame_index):
        return self._rolls[frame_index] + self._rolls[frame_index + 1] == 10

    def _is_strike(self, frame_index):
        return self._rolls[frame_index] == 10


import random

FRAME_COUNT = 10
PIN_COUNT = 10
EXIT_CODE = "x"


def render(frames: list):
    cell_width = len("|  1  |") - 1
    special_width = len("| Frame |  10   | total |")
    table_width = special_width + cell_width * (FRAME_COUNT - 1)

    # frame
    frame_cells = [f"{i}" for i in range(1, FRAME_COUNT)]
    frame_cells_row = "  |  ".join(frame_cells)
    frame_row = f"| Frame |  {frame_cells_row}  |  10   | Total |"

    # divider
    divider_row = "-" * table_width

    # throw
    throw_cells = []
    codes = throws_to_codes(frames)
    for i, code in enumerate(codes):
        row = " ".join([str(x) for x in code if x is not None])
        if i == FRAME_COUNT - 1:
            throw_cells.append(f"{row:<5}")
        else:
            throw_cells.append(f"{row:<3}")
    throw_cells_row = " | ".join(throw_cells)
    throw_row = f"| Score | {throw_cells_row} |       |"

    # score
    scores = calculate_scores(frames)
    score_repr = [x if x is not None else "" for x in scores]
    score_cells = [f"{t:^3}" for t in score_repr[:-1]]
    score_cells_row = " | ".join(score_cells)
    last_cell = f"{score_repr[-1]:^5}"
    total = get_total_from_scores(scores)
    total = total if total is not None else ""
    total = f"{total:^5}"
    score_row = f"|       | {score_cells_row} | {last_cell} | {total} |"

    table = [divider_row, frame_row, divider_row, throw_row, score_row, divider_row]

    print("\n".join(table))


def throw_to_code(throw: list):
    code = []
    pins_left = PIN_COUNT
    for i, pins in enumerate(throw):
        if pins is None:
            continue
        pins_left -= pins
        if pins_left == 0:
            was_previous_strike = throw[i - 1] == PIN_COUNT
            if i == 0 or was_previous_strike:
                code.append("X")
            else:
                code.append("/")
            pins_left = PIN_COUNT
        else:
            code.append(pins)
    return code


def get_total_from_scores(scores: list):
    if scores[-1] is not None:
        return scores[-1]

    try:
        index_of_total = scores.index(None) - 1
    except:
        index_of_total = -1
    return scores[index_of_total] if index_of_total >= 0 else None


def throws_to_codes(throws: list):
    codes = []
    for throw in throws:
        codes.append(throw_to_code(throw))
    return codes


def init_frames():
    frames = [[None, None] for _ in range(FRAME_COUNT)]
    frames[-1].append(None)
    return frames


def parse_user_input(user_input):
    is_valid = True
    value = None

    if user_input == EXIT_CODE:
        value = EXIT_CODE
    elif user_input == "":
        value = random.randint(0, pins_left)
    else:
        try:
            throw = int(user_input)
            if 0 <= throw <= pins_left:
                value = throw
            else:
                is_valid = False
        except:
            value = None

    return (value, is_valid)


def get_user_input(pins_left: int):
    is_input_valid = False
    while not is_input_valid:
        user_input = input(
            f"Kacst (0-{pins_left}, ENTER for random, {EXIT_CODE} for avslutte): "
        )
        user_input, is_input_valid = parse_user_input(user_input)

    return user_input


def go_to_next_throw(pins_left, current_throw, current_frame, last_frame_bonus):
    all_pins_knocked = pins_left <= 0
    is_last_frame = current_frame == FRAME_COUNT - 1
    throw_attempts = 3 if is_last_frame else 2

    # pins
    if all_pins_knocked:
        pins_left = PIN_COUNT

    # throw and frame
    previous_throw = current_throw
    current_throw += 1
    if all_pins_knocked:
        if is_last_frame:
            last_frame_bonus = True
        else:
            current_frame += 1
            current_throw = 0
    elif is_last_frame and previous_throw == 1 and not last_frame_bonus:
        current_frame += 1
        current_throw = 0

    # go to next frame
    if current_throw == throw_attempts:
        current_throw = 0
        pins_left = PIN_COUNT
        current_frame += 1

    return pins_left, current_throw, current_frame


def flatten_list(matrix):
    return [item for row in matrix for item in row]


def cum_sum(array):
    if len(array) == 0:
        return None

    sums = []
    cum = 0
    for element in array:
        cum += element
        sums.append(cum)
    return sums


def calculate_scores(_frames):
    frames = [*_frames, [0], [0]]
    scores = [None] * len(_frames)
    empty_frame_index = -1
    for i, frame in enumerate(frames[:-2]):
        is_frame_empty = all([x is None for x in frame])
        if is_frame_empty:
            empty_frame_index = i
            break

        bonus = 0
        total = sum([x for x in frame if x is not None])
        if total == PIN_COUNT:
            next_throws = [*frames[i + 1]]
            is_strike = frame[0] == 10
            if is_strike:
                next_throws.extend(frames[i + 2])
            next_throws = [x for x in next_throws if x is not None]
            if len(next_throws) != 0:
                bonus = sum(next_throws[:2]) if is_strike else next_throws[0]

        scores[i] = total + bonus

    if empty_frame_index == 0:
        return scores
    elif empty_frame_index > 0:
        frame_scores = cum_sum(scores[:empty_frame_index])
        scores = [*frame_scores, *scores[empty_frame_index:]]
        return scores
    else:
        return cum_sum(scores)


frames = init_frames()
pins_left = PIN_COUNT
current_frame = 0
current_throw = 0
last_frame_bonus = False
while True:
    render(frames)

    user_input = get_user_input(pins_left)
    if user_input == EXIT_CODE:
        print()
        print("spill avsluttet og lagret")
        break

    roll(
        user_input,
    )
    throw = user_input
    frames[current_frame][current_throw] = throw
    pins_left -= throw

    pins_left, current_throw, current_frame = go_to_next_throw(
        pins_left, current_throw, current_frame, last_frame_bonus
    )

    if current_frame >= FRAME_COUNT:
        render(frames)
        print("Game end")
        break


def test_game():
    game = Game()
    test_frames = [x for x in flatten_list(frames) if x is not None]
    for frame in test_frames:
        game.roll(frame)
    game_score = game.score()
