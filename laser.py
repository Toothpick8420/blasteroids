import pygame as pyg

from gameobject import GameObject


class Laser(GameObject):

    LASER_SPRITE: str = "resources/images/Laser.gif"

    def __init__(self, x: int, y: int, dx: int, dy: int, team: int):

        super().__init__(Laser.LASER_SPRITE, x, y, dx, dy, team)

    def off_screen(self) -> None:
        super().die()
