import pygame as pyg

import constants as CONSTS
from laser import Laser
from gameobject import GameObject


class Ship(GameObject):

    STARTING_LIVES: int = 3
    SPEED: int = 3
    LASER_SPEED: int = -4

    SPRITE_PATH: str = "resources/images/Ship.gif"

    def __init__(self):

        super().__init__(Ship.SPRITE_PATH, team=2)

        self.sprite_ = pyg.transform.scale(self.sprite_, (40, 64))
        self.rect_.x = (CONSTS.SCREEN_WIDTH / 2) - (self.rect_.w / 2)
        self.rect_.y = (CONSTS.SCREEN_HEIGHT / 4) * 3

        self.lives_: int = Ship.STARTING_LIVES

        self.events_: list = []

    def update(self) -> None:
        for event in self.events_:
            if event.type == pyg.KEYDOWN:
                # Horizontal Movement
                if event.key == pyg.K_LEFT or event.key == pyg.K_a:
                    self.dx_ = -Ship.SPEED
                elif event.key == pyg.K_RIGHT or event.key == pyg.K_d:
                    self.dx_ = Ship.SPEED
                # Vertical Movement
                if event.key == pyg.K_UP or event.key == pyg.K_w:
                    self.dy_ = -Ship.SPEED
                elif event.key == pyg.K_DOWN or event.key == pyg.K_s:
                    self.dy_ = Ship.SPEED

                # Fire laser
                if event.key == pyg.K_SPACE:
                    Laser(
                        self.rect_.x + (self.rect_.w / 2),
                        self.rect_.y,
                        0,
                        Ship.LASER_SPEED,
                        self.team_,
                    )

            if event.type == pyg.KEYUP:
                # Horizontal Movement
                if (
                    (event.key == pyg.K_LEFT or event.key == pyg.K_a) and self.dx_ < 0
                ) or (
                    (event.key == pyg.K_RIGHT or event.key == pyg.K_d) and self.dx_ > 0
                ):
                    self.dx_ = 0

                # Vertical Movement
                if (
                    (event.key == pyg.K_UP or event.key == pyg.K_w) and self.dy_ < 0
                ) or (
                    (event.key == pyg.K_DOWN or event.key == pyg.K_s) and self.dy_ > 0
                ):
                    self.dy_ = 0

        # Call parent method
        super().update()

    def off_left(self) -> None:
        self.rect_.x = CONSTS.SCREEN_WIDTH

    def off_right(self) -> None:
        self.rect_.x = 0

    def off_top(self) -> None:
        self.rect_.y = CONSTS.SCREEN_HEIGHT

    def off_bottom(self) -> None:
        self.rect_.y = 0

    def die(self) -> None:
        if self.lives_ > 0:
            self.lives_ -= 1
        else:
            super().die()

    def lives(self) -> int:
        return self.lives_

    def set_lives(self, lives: int) -> None:
        self.lives_ = 3

    def reset(self) -> None:
        self.lives_ = 3
        self.rect_.x = (CONSTS.SCREEN_WIDTH / 2) - (self.rect_.w / 2)
        self.rect_.y = CONSTS.SCREEN_HEIGHT / 4 * 3
        self.dx_ = 0
        self.dy_ = 0

    def events(self, events: list) -> None:
        self.events_ = events
