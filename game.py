import random
import pygame as pyg

import constants as CONSTS
import ui
from highscore import Highscore
from asteroid import Asteroid
from gameobject import GameObject
from ship import Ship
from surface import Surface

# Create Screen
# Where all the drawing happens
surface: Surface = Surface(CONSTS.SCREEN_WIDTH, CONSTS.SCREEN_HEIGHT)

# Pygame clock to control framerate of the game
clock: pyg.time.Clock = pyg.time.Clock()

# Instanciating objects for the game
amount_per_level: int = 5
level: int = 0
asteroid_field: list = []

player: Ship = Ship()

highscore = Highscore()

# Set up for the game
stage: int = CONSTS.MAIN_MENU
running: bool = True

while running:

    # Get the events from pygame
    events = pyg.event.get()

    # Check for the window close event
    for event in events:
        if event.type == pyg.QUIT:
            running = False

    # Clear the screen
    surface.clear()

    # State checking of the game
    if stage == CONSTS.MAIN_MENU:
        # FOR RESETTING THE GAME
        del GameObject.ALL_OBJS[1:]
        Asteroid.ALIVE = 0
        Asteroid.TOTAL_DESTROYED = 0
        level = 0
        player.reset()

        # Select title color
        title_r: int = random.randint(0, 255)
        title_g: int = random.randint(0, 255)
        title_b: int = random.randint(0, 255)

        # Draw Title
        surface.draw(
            ui.render_title_offset(
                "Blasteroids",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4),
                title_r,
                title_g,
                title_b,
            )
        )

        surface.draw(
            ui.render_text_offset(
                "Press  Enter  to  Continue",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3) - 20,
                font_size=25,
            )
        )
        surface.draw(
            ui.render_text_offset(
                "Press Esc to Quit",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3),
                font_size=25,
            )
        )
        surface.draw(
            ui.render_text_offset(
                "Press H for Highscores",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3) + 20,
                font_size=25,
            )
        )
        surface.draw(
            ui.render_text_offset(
                "Press C for Controls",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3) + 40,
                font_size=25,
            )
        )

        # Poll events for press
        for event in events:
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_RETURN:
                    stage = CONSTS.IN_GAME
                elif event.key == pyg.K_ESCAPE:
                    running = False
                elif event.key == pyg.K_h:
                    stage = CONSTS.HIGH_SCORE
                elif event.key == pyg.K_c:
                    stage = CONSTS.CONTROLS

    elif stage == CONSTS.IN_GAME:

        # Update
        player.events(events)
        GameObject.update_all()

        # Check for collision
        GameObject.check_collision_all()

        # Draw
        surface.draw(ui.render_text(f"Level {level}", 10, 5, font_size=20))
        surface.draw(ui.render_text(f"Lives {player.lives()}", 10, 25, font_size=20))
        surface.draw(
            ui.render_text(f"Score {Asteroid.TOTAL_DESTROYED}", 10, 45, font_size=20)
        )
        surface.draw_all(GameObject.ALL_OBJS)

        # Game is over when out of lives
        if player.lives() <= 0:
            if highscore.new_highscore(Asteroid.TOTAL_DESTROYED):
                initials: str = ""

                while len(initials) < 3:
                    surface.clear()

                    surface.draw(
                        ui.render_text_offset(
                            "Enter initials",
                            (CONSTS.SCREEN_WIDTH / 2),
                            (CONSTS.SCREEN_HEIGHT / 4),
                            font_size=78,
                        )
                    )
                    surface.draw(
                        ui.render_text_offset(
                            initials,
                            (CONSTS.SCREEN_WIDTH / 2),
                            (CONSTS.SCREEN_HEIGHT / 2),
                            font_size=40,
                        )
                    )

                    for event in pyg.event.get():
                        if event.type == pyg.KEYDOWN:
                            if event.key == pyg.K_BACKSPACE:
                                initials = initials[:-1]
                            else:
                                initials += pyg.key.name(event.key)

                    pyg.display.update()

                highscore.add(initials, Asteroid.TOTAL_DESTROYED)

            highscore.save_scores()
            stage = CONSTS.GAME_OVER

        # Purge dead objs when count gets to high
        if GameObject.DEAD_COUNT > 50:
            GameObject.purge_dead()

        if Asteroid.ALIVE <= 0:
            asteroid_field.clear()
            level += 1
            for i in range(10 + (amount_per_level * level)):
                asteroid_field.append(Asteroid())

    elif stage == CONSTS.GAME_OVER:

        # Draw GameOver
        r: int = random.randint(0, 255)
        g: int = random.randint(0, 255)
        b: int = random.randint(0, 255)

        surface.draw(
            ui.render_title_offset(
                "Game Over",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4),
                r,
                g,
                b,
            )
        )

        surface.draw(
            ui.render_text_offset(
                "Press Esc to Quit",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3),
                font_size=25,
            )
        )
        surface.draw(
            ui.render_text_offset(
                "Press Enter to Restart",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3) + 20,
                font_size=25,
            )
        )
        surface.draw(
            ui.render_text_offset(
                "Press H for HighScores",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3) + 40,
                font_size=25,
            )
        )

        for event in events:
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    running = False
                elif event.key == pyg.K_h:
                    stage = CONSTS.HIGH_SCORE
                elif event.key == pyg.K_RETURN:
                    stage = CONSTS.MAIN_MENU

    elif stage == CONSTS.HIGH_SCORE:

        surface.draw(
            ui.render_title_offset(
                "High Scores", (CONSTS.SCREEN_WIDTH / 2), (CONSTS.SCREEN_HEIGHT / 5)
            )
        )

        y: int = (CONSTS.SCREEN_HEIGHT / 3)
        for score in Highscore.SCORES:
            score_as_string: str = f"{score[1]}     {score[0]}"
            surface.draw(
                ui.render_text_offset(
                    score_as_string, (CONSTS.SCREEN_WIDTH / 2), y, font_size=25
                )
            )

            y += 20

        for event in events:
            if event.type == pyg.KEYDOWN:
                stage = CONSTS.MAIN_MENU

    elif stage == CONSTS.CONTROLS:

        surface.draw(
            ui.render_title_offset(
                "Controls", (CONSTS.SCREEN_WIDTH / 2), (CONSTS.SCREEN_HEIGHT / 5)
            )
        )
        surface.draw(
            ui.render_text_offset(
                "WASD    or    Arrow    Keys    to    move",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3),
            )
        )
        surface.draw(
            ui.render_text_offset(
                "SPACE    to    fire    laser",
                (CONSTS.SCREEN_WIDTH / 2),
                (CONSTS.SCREEN_HEIGHT / 4 * 3) + 20,
            )
        )

        for event in events:
            if event.type == pyg.KEYDOWN:
                stage = CONSTS.MAIN_MENU

    clock.tick(CONSTS.FPS)
    # print(f"dt: {dt}")

    pyg.display.update()
