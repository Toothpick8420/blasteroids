import pygame as pyg

pyg.font.init()

TITLE_FONT_SIZE: int = 96


def render_text(
    txt: str,
    x: int,
    y: int,
    font_size: int = 16,
    red: int = 255,
    blue: int = 255,
    green: int = 255,
) -> (pyg.Surface, pyg.Rect):

    font_renderer: pyg.font.Font = pyg.font.Font(
        "resources/font/ARCADECLASSIC.TTF", font_size
    )

    text: pyg.Surface = font_renderer.render(txt, True, (red, blue, green))
    text_rect: pyg.Rect = text.get_rect()
    text_rect.x = x
    text_rect.y = y

    return (text, text_rect)


def render_text_offset(
    text: str,
    x: int,
    y: int,
    font_size: int = 16,
    red: int = 255,
    blue: int = 255,
    green: int = 255,
) -> (pyg.Surface, pyg.Rect):
    rendered_text: (pyg.Surface, pyg.Rect) = render_text(
        text, x, y, font_size, red, blue, green
    )

    offset_rect: pyg.Rect = rendered_text[1]

    offset_rect.x = x - (offset_rect.w / 2)
    offset_rect.y = y - (offset_rect.h / 2)

    return (rendered_text[0], offset_rect)


def render_title_offset(
    header: str, x: int, y: int, red: int = 255, blue: int = 255, green: int = 255
) -> (pyg.Surface, pyg.Rect):

    font_renderer: pyg.font.Font = pyg.font.Font(
        "resources/font/ARCADECLASSIC.TTF", TITLE_FONT_SIZE
    )

    title: pyg.Surface = font_renderer.render(header, True, (red, blue, green))
    title_rect: pyg.Rect = title.get_rect()
    title_rect.x = x - (title_rect.w / 2)
    title_rect.y = y - (title_rect.h / 2)

    return (title, title_rect)
