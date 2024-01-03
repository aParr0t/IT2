from .GlobalState import GlobalState
from .Screen import ScreenManager


class App:
    def __init__(self):
        self.global_state = GlobalState("data.json")
        self.screen_manager = ScreenManager(self.global_state, clear_display=True)
        self.screen_manager.set_start_screen(self.screen_manager._start_screen_function)

    def run(self):
        print("Velkommen til sykkelsjappa!")
        self.screen_manager.start()
