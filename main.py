import pygame

import src.shared as shared


class Game:
    BG_COLOR = (50, 50, 50)

    def __init__(self) -> None:
        self.win_init()
        from src.states import StateManager

        self.state_manager = StateManager()

    def win_init(self):
        pygame.init()
        shared.screen = pygame.display.set_mode((shared.WIN_SIZE))
        shared.SRECT = shared.screen.get_rect()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Ice Age Puzzle")

    def update(self):
        shared.dt = self.clock.tick() / 1000.0
        shared.events = pygame.event.get()
        shared.keys = pygame.key.get_pressed()

        for event in shared.events:
            if event.type == pygame.QUIT:
                raise SystemExit

        self.state_manager.update()

        pygame.display.update()

    def draw(self):
        shared.screen.fill(Game.BG_COLOR)
        self.state_manager.draw()

    def run(self):
        while True:
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
