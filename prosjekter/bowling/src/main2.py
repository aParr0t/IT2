class BowlingGame:
    def __init__(self, frames=10, pins=10):
        self.frame_count = frames
        self.pin_count = pins
        self._init_throws()
        self.current_throw = 0

    def _init_throws(self):
        self.throws = [0] * (self.frame_count * 2 + 1)

    def roll(self, pins):
        if pins < 0 or pins > self.pin_count:
            raise ValueError("Invalid number of pins")

        self.throws[self.current_throw] = pins

        if self._is_strike(self._current_frame()) and not self._is_last_frame():
            self.current_throw += 1
        is_middle_throw = self.current_throw == len(self.throws) - 2
        if self._is_last_frame and not self._has_bonus_throw() and is_middle_throw:
            self.current_throw += 1
        self.current_throw += 1

    def reset(self):
        self._init_throws()

    def pins_left(self):
        return self.pin_count - sum(self._frame(self._current_frame()))

    def _frame_length(self, frame_idx):
        return 2 if frame_idx != self.frame_count - 1 else 3

    def _frame(self, frame_idx):
        throw_idx = frame_idx * 2
        return self.throws[throw_idx : throw_idx + self._frame_length(frame_idx)]

    def _get_bonus_points(self, throw_idx: int, count: int):
        points = 0
        count = count
        throw_idx = throw_idx + 1

        while count > 0 and throw_idx < len(self.throws):
            throw = self.throws[throw_idx]
            points += throw
            count -= 1

            frame_idx = self._frame_idx(throw_idx)
            is_last_frame = frame_idx == self.frame_count - 1
            is_first_throw = throw_idx % 2 == 0
            is_strike = is_first_throw and throw == self.pin_count and not is_last_frame
            if is_strike:
                throw_idx += 2
            else:
                throw_idx += 1

            if self._is_strike(frame_idx) and throw == 0:
                count += 1
        return points

    def _bonus_points(self, throw_idx: int):
        points = 0
        if self._is_spare(self._frame_idx(throw_idx)):
            count = 1

        # elif :

        # if self.throws[throw_idx] !=

        # [10, 0, 10, 2, 2]

        # throw_idx = (frame_idx + 1) * 2
        # count = count
        # while count > 0 and throw_idx < len(self.throws):
        #     throw = self.throws[throw_idx]
        #     points += throw
        #     count -= 1

        #     is_last_frame = throw_idx // 2 == self.frame_count - 1
        #     is_first_throw = throw_idx % 2 == 0
        #     is_strike = is_first_throw and throw == self.pin_count and not is_last_frame
        #     if is_strike:
        #         throw_idx += 2
        #     else:
        #         throw_idx += 1
        return points

    def _is_spare(self, frame_idx):
        return sum(self._frame(frame_idx)) == self.pin_count

    def _is_strike(self, frame_idx):
        throw_idx = frame_idx * 2
        return self.throws[throw_idx] == self.pin_count

    def _is_last_frame(self):
        return self._current_frame() == self.frame_count - 1

    def _frame_idx(self, throw_idx):
        if throw_idx <= 0 or throw_idx >= len(self.throws):
            raise ValueError("Invalid throw index")

        normal_throw_count = (self.frame_count - 1) * 2
        if throw_idx < normal_throw_count:
            return throw_idx // 2
        else:
            return self.frame_count - 1

    def _current_frame(self):
        return self._frame_idx(self.current_throw)

    def _frame_score(self, frame_idx):
        bonus_points = 0
        if self._is_strike(frame_idx):
            if frame_idx == self.frame_count - 1:
                bonus_points = sum(self.throws[-2:])
            else:
                bonus_points = self._bonus_points(frame_idx, 2)
        elif self._is_spare(frame_idx):
            bonus_points = self._bonus_points(frame_idx, 1)
        return sum(self._frame(frame_idx)) + bonus_points

    def _has_bonus_throw(self):
        if self.throws[-3] == self.pin_count:
            return True
        if self.throws[-3] + self.throws[-2] == self.pin_count:
            return True
        return False

    def running_scores(self):
        scores = []
        running_score = 0
        for frame_idx in range(self._current_frame()):
            running_score += self._frame_score(frame_idx)
            scores.append(running_score)
        return scores

    def score(self):
        return self.running_scores()[-1]


class Game:
    def __init__(self, players=1):
        self.players = players
        self.games = [BowlingGame() for _ in range(players)]

    def start(self):
        while True:
            # get player input
            # handle player input
            self._handle_input()
            pass

    def _handle_input(self):
        # player_input = input(f"Kast (0-{pins_left}, ENTER for random, {EXIT_CODE} for avslutte): ")
        pass


if __name__ == "__main__":
    game = Game()
    game.start()
