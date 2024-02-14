import pygame


class Button:
    def __init__(self, display, x, y, width, height, text, color):
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(
            self.display, self.color, (self.x, self.y, self.width, self.height)
        )
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(self.text, True, (0, 0, 0))
        self.display.blit(
            text,
            (
                self.x + self.width / 2 - text.get_width() / 2,
                self.y + self.height / 2 - text.get_height() / 2,
            ),
        )

    def isClicked(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (
            self.x < mouse[0] < self.x + self.width
            and self.y < mouse[1] < self.y + self.height
        ):
            if click[0] == 1:
                return True
        return False
