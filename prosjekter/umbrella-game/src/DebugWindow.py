import pygame
import pygame_gui
from pygame_gui.elements.ui_window import UIWindow

from .State import State


class DebugUIWindow(UIWindow):
    def __init__(self, position, ui_manager, state: State):
        super().__init__(
            pygame.Rect(position, (320, 240)),
            ui_manager,
            window_display_title="CustomUIWindow",
            # object_id="#pong_window",
        )
        self.state = state
        self.labels = []
        self.refresh()

    def process_event(self, event):
        """
        Handles events for the window.
        """
        handled = super().process_event(event)
        if event.type == pygame.KEYDOWN:
            key = event.unicode
            if key in self.state.shortcut_variables:
                var_name = self.state.shortcut_variables[key]
                value = getattr(self.state, var_name)
                if isinstance(value, bool):
                    setattr(self.state, var_name, not value)
            handled = True
        if handled:
            self.refresh()
        return handled

    def update(self, time_delta):
        super().update(time_delta)

    def clear(self):
        """
        Clears all elements in the window.
        """
        for l in self.labels:
            l.kill()

    def refresh(self):
        """
        Refreshes the window. This is called when the state changes.
        Updates the information in the labels.
        """
        self.clear()
        game_surface_size = self.get_container().get_size()
        for i, var_name in enumerate(self.state.visible_variables):
            value = getattr(self.state, var_name)

            label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, i * 20, game_surface_size[0], 20),
                text=f"{var_name}: {value}",
                manager=self.ui_manager,
                container=self,
            )
            self.labels.append(label)
