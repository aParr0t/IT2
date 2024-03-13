import pygame

from ..GlobalState import GlobalState


class Screen:
    def __init__(self, state: GlobalState) -> None:
        self.state = state

    def reset(self):
        pass

    def tick(self, dt: float = 0.0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
                self.state.save_level()
            self._handle_events(event)

        self.update(dt)
        self.render()

    def _handle_events(self, event: pygame.event.Event):
        pass

    def render(self):
        pass

    def update(self, dt: float = 0.0):
        pass
