import curses
import logging
import time

from desk import Desk
from buttons import Button


logger = logging.getLogger()


def start_game(window: curses.window):
    """Loading screen and stuff"""
    # Setup
    curses.curs_set(0)  # Hide cursor
    window.nodelay(True)  # Make getch non-blocking

    # Clearing the window
    window.clear()

    # Drawing the button
    start_button = Button(10, 10, "Start the game!", window)
    start_button.draw()
    # Instructions
    window.addstr(5, 10, "Click the button to start the game")
    window.refresh()

    while True:
        try:
            key = window.getch()
            if key == curses.KEY_MOUSE:
                try:
                    _, mouse_x, mouse_y, _, _ = curses.getmouse()
                    if start_button.is_clicked(mouse_x, mouse_y):
                        game(window)
                except curses.error:
                    # Sometimes getmouse can fail
                    pass
            elif key == ord("q"):  # Allow quitting with 'q'
                raise KeyboardInterrupt()
        except curses.error:
            # No input available
            pass

        time.sleep(0.1)  # Prevent CPU hogging

        window.refresh()


def game(window: curses.window):
    """Main game function (event loop)"""
    window.clear()
    # Make sure that nodelay mode is kept from start_game
    window.nodelay(True)
    curses.start_color()
    # Create and draw restart button
    restart_button = Button(10, 10, "Restart the game", window)
    restart_button.draw()

    desk = Desk(window)
    desk.initialize()
    desk.init_draw()

    # Game instructions
    window.addstr(2, 7, "Solitaire Game")
    window.addstr(3, 7, "(double) Press 'q' to quit")

    # Start time.time()
    start_time = time.time()
    # Game loop
    running = True

    while running:  # EVENT LOOP
        # Show time
        elapsed_mins = (time.time() - start_time) / 60
        window.addstr(
            4,
            7,
            f"your time: {int(elapsed_mins)} minutes {int((elapsed_mins % 1) * 60)} seconds",
        )
        try:
            key = window.getch()  # Checking for input
            if key == ord("q"):  # q for quit
                running = False
            elif key == curses.KEY_MOUSE:  # mouse click
                try:
                    _, mouse_x, mouse_y, _, _ = curses.getmouse()  # get mouse pos
                    if restart_button.is_clicked(mouse_x, mouse_y):
                        # Restart the game
                        return game(window)
                    if desk.on_click(mouse_x, mouse_y):
                        window.clear()
                        desk.draw()
                        restart_button.draw()

                except Exception as e:
                    logger.error(e, exc_info=True)
        except Exception as e:
            logger.error(e, exc_info=True)
        window.refresh()
        time.sleep(0.05)  # Prevent CPU hogging
