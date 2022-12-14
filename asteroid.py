import random

import constants as CONSTS
from gameobject import GameObject


class Asteroid(GameObject):

    TOTAL_DESTROYED: int = 0

    MAX_SPEED: int = 3
    SPRITE_PATH: str = "resources/images/Asteroid.gif"
    WIDTH: int = 32

    ALIVE: int = 0

    def __init__(self):
        rand_x: int = random.randint(0, CONSTS.SCREEN_WIDTH)
        rand_y: int = random.randint(0, CONSTS.SCREEN_HEIGHT / 4)
        rand_dx: int = random.randint(-1, 1)
        rand_dy: int = random.randint(1, Asteroid.MAX_SPEED)

        Asteroid.ALIVE += 1
        super().__init__(
            Asteroid.SPRITE_PATH, x=rand_x, y=rand_y, dx=rand_dx, dy=rand_dy, team=1
        )

    def off_bottom(self) -> None:
        self.rect_.y = 0 - self.rect_.h

    def off_left(self) -> None:
        self.rect_.x = CONSTS.SCREEN_WIDTH

    def off_right(self) -> None:
        self.rect_.x = 0 - self.rect_.w

    def die(self) -> None:
        Asteroid.TOTAL_DESTROYED += 1
        Asteroid.ALIVE -= 1
        super().die()
