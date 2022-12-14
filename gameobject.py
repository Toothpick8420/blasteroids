import pygame as pyg

import constants as CONSTS


class GameObject:

    ALL_OBJS: list = []
    DEAD_COUNT: int = 0

    def __init__(
        self,
        sprite: str,
        x: int = 0,
        y: int = 0,
        dx: int = 0,
        dy: int = 0,
        team: int = 0,
    ):

        self.sprite_: pyg.Surface = pyg.image.load(sprite)

        self.rect_: pyg.Rect = self.sprite_.get_rect()
        self.rect_.x = x
        self.rect_.y = y

        self.dx_: int = dx
        self.dy_: int = dy

        self.team_: int = team
        self.alive_: bool = True

        GameObject.ALL_OBJS.append(self)

    # Move the object and then call the approriate off_edge functions depending
    # On where it went off
    def update(self) -> None:

        self.rect_.x += self.dx_
        if self.get_right() < 0:
            self.off_left()
        elif self.get_left() > CONSTS.SCREEN_WIDTH:
            self.off_right()

        self.rect_.y += self.dy_
        if self.get_bottom() < 0:
            self.off_top()
        elif self.get_top() > CONSTS.SCREEN_HEIGHT:
            self.off_bottom()

    # Returns the spirte and rect as a tuple, used on surface.blit() for drawing
    def as_tuple(self) -> (pyg.Surface, pyg.Rect):
        return (self.sprite_, self.rect_)

    # off_edge functions for when the object goes off edge
    # Meant to be overloaded default behaviour is do nothing
    def off_left(self) -> None:
        self.off_screen()

    def off_right(self) -> None:
        self.off_screen()

    def off_bottom(self) -> None:
        self.off_screen()

    def off_top(self) -> None:
        self.off_screen()

    def off_screen(self) -> None:
        pass

    # Collision detection of 2 objects using AABB collision detection
    def collided(self, obj: "GameObject") -> None:
        if self.team() == obj.team():
            return False
        elif not (self.alive()) or not (obj.alive()):
            return False

        else:
            return (
                self.get_left() < obj.get_right()
                and self.get_right() > obj.get_left()
                and self.get_top() < obj.get_bottom()
                and self.get_bottom() > obj.get_top()
            )

    # Sets to unalive, this is what will be called when collision is detected
    def die(self) -> None:
        GameObject.DEAD_COUNT += 1
        self.alive_ = False

    # Get the edges in numerical values
    def get_left(self) -> int:
        return self.rect_.x

    def get_right(self) -> int:
        return self.rect_.x + self.rect_.w

    def get_top(self) -> int:
        return self.rect_.y

    def get_bottom(self) -> int:
        return self.rect_.y + self.rect_.h

    # Get the team of the object to be used for collision
    def team(self) -> int:
        return self.team_

    def alive(self) -> bool:
        return self.alive_

    # "Static" functions for using the array
    # Update all alive objects
    def update_all() -> None:
        for obj in GameObject.ALL_OBJS:
            if obj.alive():
                obj.update()

    # Check collision across all objects and call die if collided
    def check_collision_all() -> None:
        for i in range(len(GameObject.ALL_OBJS) - 1):
            for j in range((i + 1), len(GameObject.ALL_OBJS)):
                if GameObject.ALL_OBJS[i].collided(GameObject.ALL_OBJS[j]):
                    GameObject.ALL_OBJS[i].die()
                    GameObject.ALL_OBJS[j].die()

    def check_collision(obj: "GameObject", compare_with: list) -> None:
        for obj2 in compare_with:
            if id(obj) != id(obj2) and obj.collided(obj2):
                obj.die()
                obj2.die()

    def purge_dead() -> None:
        alive_objs: list = []
        for obj in GameObject.ALL_OBJS:
            if obj.alive():
                alive_objs.append(obj)

        GameObject.ALL_OBJS = alive_objs
        GameObject.DEAD_COUNT = 0
