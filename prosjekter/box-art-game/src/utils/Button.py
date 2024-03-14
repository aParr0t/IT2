import pygame


class Button:
    def __init__(self, display, width, height, text, color, x=0, y=0):
        self.display = display
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        font = pygame.font.SysFont("Arial", 25)
        self.text = font.render(text, True, (0, 0, 0))

    def draw(self, **kwargs):
        self.x = kwargs.get("x", self.x)
        self.y = kwargs.get("y", self.y)
        pygame.draw.rect(
            self.display, self.color, (self.x, self.y, self.width, self.height)
        )
        self.display.blit(
            self.text,
            (
                self.x + self.width / 2 - self.text.get_width() / 2,
                self.y + self.height / 2 - self.text.get_height() / 2,
            ),
        )

    def is_clicked(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (
            self.x < mouse[0] < self.x + self.width
            and self.y < mouse[1] < self.y + self.height
        ):
            if click[0] == 1:
                return True
        return False
