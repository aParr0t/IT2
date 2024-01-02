import unittest

from src.main3 import BowlingGame, Frame


class TestFrame(unittest.TestCase):
    def test_is_strike(self):
        frame = Frame()
        frame.throw(10)
        self.assertTrue(frame.is_strike())

    def test_is_spare(self):
        frame = Frame()
        frame.throw(5)
        frame.throw(5)
        self.assertTrue(frame.is_spare())

    def test_score(self):
        frame = Frame()
        frame.throw(5)
        frame.throw(4)
        self.assertEqual(frame.score(), 9)

    def test_throw(self):
        frame = Frame()
        frame.throw(5)
        frame.throw(4)
        with self.assertRaises(Exception):
            frame.throw(1)

    def test_throw_negative(self):
        frame = Frame()
        with self.assertRaises(Exception):
            frame.throw(-1)

    def test_throw_too_big(self):
        frame = Frame()
        with self.assertRaises(Exception):
            frame.throw(11)

    def test_pin_sum_too_big(self):
        frame = Frame()
        frame.throw(5)
        with self.assertRaises(Exception):
            frame.throw(6)

    def test_last_frame_code(self):
        test_throws = [
            [[10, 10, 10], ["X", "X", "X"]],
            [[5, 5, 10], ["5", "/", "X"]],
            [[3, 6], ["3", "6", ""]],
            [[10, 0, 10], ["X", "0", "/"]],
        ]
        for throws, result in test_throws:
            frame = Frame(length=3)
            for pins in throws:
                frame.throw(pins)
            self.assertEqual(frame.codes(), result)

    def test_frame_code(self):
        test_throws = [
            [[10], ["", "X"]],
            [[5, 5], ["5", "/"]],
            [[3, 6], ["3", "6"]],
        ]
        for throws, result in test_throws:
            frame = Frame(length=2)
            for pins in throws:
                frame.throw(pins)
            self.assertEqual(frame.codes(), result)

    def test_is_finished(self):
        frame = Frame()
        frame.throw(5)
        frame.throw(4)
        self.assertTrue(frame.is_finished())

        frame = Frame()
        frame.throw(10)
        self.assertTrue(frame.is_finished())

        frame = Frame(length=3)
        frame.throw(10)
        frame.throw(10)
        frame.throw(10)
        self.assertTrue(frame.is_finished())

        frame = Frame(length=3)
        frame.throw(3)
        frame.throw(4)
        self.assertTrue(frame.is_finished())

        frame = Frame(length=3)
        frame.throw(3)
        frame.throw(7)
        self.assertFalse(frame.is_finished())

        frame = Frame(length=3)
        frame.throw(10)
        self.assertFalse(frame.is_finished())

        frame = Frame(length=3)
        frame.throw(5)
        frame.throw(5)
        frame.throw(10)
        self.assertTrue(frame.is_finished())


class TestBowlingGame(unittest.TestCase):
    def test_throw(self):
        game = BowlingGame()
        game.throw(5)
        game.throw(4)
        self.assertEqual(game.frames[0].score(), 9)

    def test_throw_strike(self):
        game = BowlingGame()
        game.throw(10)
        self.assertEqual(game.frames[0].score(), 10)

    def test_throw_spare(self):
        game = BowlingGame()
        game.throw(5)
        game.throw(5)
        self.assertEqual(game.frames[0].score(), 10)

    def test_score(self):
        game = BowlingGame()
        game.throw(5)
        game.throw(4)
        self.assertEqual(game.score(), 9)

    def test_score_strike(self):
        game = BowlingGame()
        game.throw(10)
        game.throw(5)
        game.throw(4)
        self.assertEqual(game.score(), 28)

    def test_score_spare(self):
        game = BowlingGame()
        game.throw(5)
        game.throw(5)
        game.throw(5)
        game.throw(4)
        self.assertEqual(game.score(), 24)

    def test_score_perfect(self):
        game = BowlingGame()
        for _ in range(12):
            game.throw(10)
        self.assertEqual(game.score(), 300)

    def test_throw_beyond_last_frame(self):
        game = BowlingGame()
        with self.assertRaises(Exception):
            for _ in range(13):
                game.throw(10)
