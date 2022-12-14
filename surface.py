import pygame as pyg

from gameobject import GameObject


class Surface:
    def __init__(self, width: int, height: int):
        self.surface_: pyg.Surface = pyg.display.set_mode((width, height))

    # Simulates clearing the screen by filling it black
    def clear(self) -> None:
        self.surface_.fill((0, 0, 0))

    # Draw an object to the screen
    def draw(self, obj_as_drawable: (pyg.Surface, pyg.Rect)) -> None:
        self.surface_.blit(obj_as_drawable[0], obj_as_drawable[1])

    # Draw a list of objects to the screen
    def draw_all(self, to_draw: list) -> None:
        for obj in to_draw:
            if obj.alive():
                obj_: tuple(pyg.Surface, pyg.Rect) = obj.as_tuple()
                self.surface_.blit(obj_[0], obj_[1])
