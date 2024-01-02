import random


class Frame:
    STRIKE_CODE = "X"
    SPARE_CODE = "/"

    def __init__(self, length=2):
        self.length = length
        self.throws = [None] * self.length

    def throw(self, pins: int):
        if pins < 0 or pins > 10:
            raise Exception("Invalid number of pins")

        if pins > self.pins_left():
            raise Exception("Too many pins")

        throw_idx = self.throws.index(None)
        self.throws[throw_idx] = pins

    def is_strike(self):
        if self.length == 2:
            return self.throws[0] == 10
        elif self.length == 3:
            return self.STRIKE_CODE in self.codes()

    def is_spare(self):
        if self.length == 2:
            throws_to_sum = self.actual_throws()
            return sum(throws_to_sum) == 10 and not self.is_strike()
        elif self.length == 3:
            return self.SPARE_CODE in self.codes()

    def is_finished(self):
        is_bonus = self.is_strike() or self.is_spare()
        if self.length == 3:
            if is_bonus and None not in self.throws:
                return True
            elif not is_bonus and len(self.actual_throws()) == 2:
                return True
            return False

        return None not in self.throws or self.is_strike()

    def score(self):
        throws_to_sum = self.actual_throws()
        return sum(throws_to_sum)

    def actual_throws(self):
        return [t for t in self.throws if t is not None]

    def codes(self):
        if self.length == 2 and self.is_strike():
            return ["", self.STRIKE_CODE]

        codes = [self.STRIKE_CODE]
        for i, t in enumerate(self.throws):
            previous_was_special = codes[i] in [
                self.STRIKE_CODE,
                self.SPARE_CODE,
            ]
            if t == 0:
                codes.append("0")
            elif t == 10 and previous_was_special:
                codes.append(self.STRIKE_CODE)
            elif i > 0 and t is not None and self.throws[i - 1] + t == 10:
                codes.append(self.SPARE_CODE)
            else:
                codes.append(str(t) if t is not None else "")
        return codes[1:]

    def pins_left(self):
        return 10 - self.score() % 10
        # [5, 5, None] = 10
        # [10, None, None] = 10
        # [10, 10, None] = 10
        # [10, 4, None] = 6
        # [4, None, None] = 6

    def __repr__(self):
        return f"Frame({self.throws})"


class BowlingGame:
    def __init__(self, player_name: str = ""):
        self.frame_count = 10
        self.frames = [Frame() for _ in range(self.frame_count - 1)]
        self.frames.append(Frame(length=3))
        self.current_frame = 0
        self.player_name = player_name

    def throw(self, pins: int):
        if self.is_finished():
            raise Exception("Game is finished")

        frame = self.frames[self.current_frame]
        frame.throw(pins)
        if frame.is_finished():
            self.current_frame = min(self.current_frame + 1, self.frame_count - 1)

    def score(self):
        scores = self.running_scores()
        if None in scores:
            idx = scores.index(None) - 1
        else:
            idx = len(scores) - 1
        return scores[idx] if idx >= 0 else None

    def codes(self):
        return [f.codes() for f in self.frames]

    def running_scores(self):
        scores = [None] * self.frame_count
        running_score = 0
        for i, frame in enumerate(self.frames):
            if i > self.current_frame:
                break
            if i > 0 and i == self.current_frame and frame.actual_throws() == []:  # cursed last minute fix to prevent the score of an unplayed frame from being shown
                break

            bonus_points = 0
            if i == self.frame_count - 1:
                pass
            elif frame.is_strike():
                next_frames = self.frames[i + 1 : i + 3]
                next_throws = []
                for f in next_frames:
                    next_throws.extend(f.actual_throws())
                bonus_points = sum(next_throws[:2])
            elif frame.is_spare():
                bonus_points = self.frames[i + 1].throws[0]
                if bonus_points is None:
                    bonus_points = 0

            score = frame.score()
            running_score += score + bonus_points
            scores[i] = running_score
        return scores

    def pins_left(self):
        frame = self.frames[self.current_frame]
        return frame.pins_left()

    def is_finished(self):
        return (
            self.current_frame == self.frame_count - 1 and self.frames[-1].is_finished()
        )

    def __repr__(self):
        return f"BowlingGame({self.frames})"


class App:
    EXIT_CODE = "x"
    RANDOM_CODE = ""

    def __init__(self, player_names=None):
        self.frame_count = 10
        self.games = []
        self.is_running = False
        self.current_game_idx = 0
        self.player_names = player_names or ["Player 1", "Player 2"]
        self.number_of_players = len(self.player_names)
        if player_names is not None:
            self.init_games()

    def render_row(
        self,
        game: BowlingGame,
        first_cell_width: int
    ):
        # throw
        throw_cells = []
        for i, code in enumerate(game.codes()):
            row = " ".join(code)
            if i == self.frame_count - 1:
                throw_cells.append(f"{row:<5}")
            else:
                throw_cells.append(f"{row:<3}")
        throw_cells_row = " | ".join(throw_cells)
        throw_row = (
            f"| {game.player_name:^{first_cell_width}} | {throw_cells_row} |       |"
        )

        # score
        scores = game.running_scores()
        scores = [s if s is not None else "" for s in scores]
        score_cells = [f"{t:^3}" for t in scores[:-1]]
        score_cells_row = " | ".join(score_cells)
        last_cell = f"{scores[-1]:^5}"
        total = f"{game.score():^5}"
        score_row = (
            f"| {" "*first_cell_width} | {score_cells_row} | {last_cell} | {total} |"
        )
        
        return (
            throw_row + '''\n''' + score_row
        )

    def current_game(self) -> BowlingGame:
        return self.games[self.current_game_idx]

    def render(self):
        first_cell_width = max(*[len(p) for p in self.player_names], len("Frame"))

        # frame
        frame_cells = [f"{i}" for i in range(1, self.frame_count)]
        frame_cells_row = "  |  ".join(frame_cells)
        frame_row = f"| {"Frame":^{first_cell_width}} |  {frame_cells_row}  |  10   | Total |"

        # divider
        table_width = len(frame_row)
        divider_row = "-" * table_width

        player_rows = []
        for game in self.games:
            player_rows.append(self.render_row(game, first_cell_width))
            player_rows.append(divider_row)

        table = [divider_row, frame_row, divider_row, *player_rows]
        for row in table:
            print(row)

    def parse_user_input(self, user_input: str):
        is_valid = True
        value = user_input

        pins_left = self.current_game().pins_left()
        if user_input == self.EXIT_CODE:
            value = self.EXIT_CODE
        elif user_input == self.RANDOM_CODE:
            value = random.randint(0, pins_left)
            print(value)
        else:
            try:
                throw = int(user_input)
                if 0 <= throw <= pins_left:
                    value = throw
                else:
                    is_valid = False
            except:
                is_valid = False

        return (value, is_valid)

    def get_user_input(self):
        is_input_valid = False
        while not is_input_valid:
            pins_left = self.current_game().pins_left()
            user_input = input(
                f"Kast (0-{pins_left}, ENTER for random, {self.EXIT_CODE} for avslutte): "
            )
            user_input, is_input_valid = self.parse_user_input(user_input)
            if not is_input_valid:
                print(f"Ugyldig input: '{user_input}'")

        return user_input

    def handle_user_input(self, user_input: str):
        if user_input == self.EXIT_CODE:
            self.is_running = False
        elif not self.games[-1].is_finished():
            # get frame index of current frame
            frame_idx = self.current_game().current_frame
            self.current_game().throw(user_input)
            new_frame_idx = self.current_game().current_frame
            if new_frame_idx > frame_idx or self.current_game().is_finished():
                self.current_game_idx = (self.current_game_idx + 1) % len(self.games) 

    def init_games(self):
        for i in range(self.number_of_players):
            name = self.player_names[i]
            self.games.append(BowlingGame(name))

    def are_all_games_finished(self):
        return all([g.is_finished() for g in self.games])

    def start(self):
        self.is_running = True
        while self.is_running:
            user_input = self.get_user_input()
            self.handle_user_input(user_input)
            self.render()
            if self.are_all_games_finished():
                print("Spillet er ferdig!")
                self.is_running = False

if __name__ == "__main__":
    app = App(player_names=["Ola", "Kariiiiiii"])
    app.start()
