import pygame

from src import shared


class Game:
    BG_COLOR = (50, 50, 50)

    def __init__(self) -> None:
        self.win_init()

    def win_init(self):
        pygame.init()
        shared.screen = pygame.display.set_mode((shared.WIN_SIZE))

    def update(self):
        shared.events = pygame.event.get()
        for event in shared.events:
            if event.type == pygame.QUIT:
                raise SystemExit

        pygame.display.update()

    def draw(self):
        shared.screen.fill(Game.BG_COLOR)

    def run(self):
        while True:
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
