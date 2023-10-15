import pygame

from src import shared


class Button:
    """
    Clickable button
    """

    def __init__(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        colors: dict[str, tuple[int, int, int]],
        text: str,
        corner_radius: int = None,
    ) -> None:
        self.colors = colors

        self.rect = pygame.Rect(pos, size)

        self.text = text
        font = pygame.font.Font(None, size[1])
        self.text_surf = font.render(text, False, colors["text"])
        self.text_pos = self.text_surf.get_rect(center=self.rect.center).topleft

        self.corner_radius = corner_radius

        self.state = "static"
        self.clicked = False

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self.clicked = False
        self.state = "static"

        if self.rect.collidepoint(mouse_pos):
            self.state = "hover"

        for event in shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == "hover":
                self.clicked = True

    def draw(self, screen: pygame.Surface) -> None:
        if self.corner_radius is None:
            pygame.draw.rect(screen, self.colors[self.state], self.rect)
        else:
            pygame.draw.rect(
                screen,
                self.colors[self.state],
                self.rect,
                border_radius=self.corner_radius,
            )

        screen.blit(self.text_surf, self.text_pos)
