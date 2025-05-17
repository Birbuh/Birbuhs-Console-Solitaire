import curses
import logging
import time

from desk import Desk
from buttons import Button
from card import Card

logger = logging.getLogger()


def start_game(stdscr: curses.window):
    """Loading screen and stuff"""
    # Setup
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getch non-blocking

    # Clearing the window
    stdscr.clear()

    # Drawing the button
    start_button = Button(10, 10, "Start the game!", stdscr)
    start_button.draw()

    # Instructions
    stdscr.addstr(5, 10, "Click the button to start the game")
    stdscr.refresh()

    while True:
        try:
            key = stdscr.getch()
            if key == curses.KEY_MOUSE:
                try:
                    _, mouse_x, mouse_y, _, _ = curses.getmouse()
                    if start_button.is_clicked(mouse_x, mouse_y):
                        break
                except curses.error:
                    # Sometimes getmouse can fail
                    pass
            elif key == ord("q"):  # Allow quitting with 'q'
                raise KeyboardInterrupt
        except curses.error:
            # No input available
            pass

        time.sleep(0.1)  # Prevent CPU hogging

    stdscr.clear()
    stdscr.refresh()


def game(stdscr: curses.window):
    """Main game function"""
    # Make sure that nodelay mode is kept from start_game
    stdscr.nodelay(True)
    curses.start_color()

    # Create and draw restart button
    restart_button = Button(10, 10, "Restart the game", stdscr)
    restart_button.draw()

    desk = Desk(stdscr)
    desk.initialize()
    desk.init_draw()

    # Game instructions
    stdscr.addstr(2, 10, "Solitaire Game")
    stdscr.addstr(3, 10, "(double) Press 'q' to quit")

    # Start time.time()
    start_time = time.time()
    # Game loop
    running = True
    while running: # EVENT LOOP
        # Show time
        elapsed_mins = (time.time() - start_time) / 60
        stdscr.addstr(
            4,
            10,
            f"your time: {int(elapsed_mins)} minutes {int((elapsed_mins % 1) * 60)} seconds",
        )

        try:
            key = stdscr.getch()  # Checking for input
            if key == ord("q"):  # q for quit
                running = False
            elif key == curses.KEY_MOUSE:  # mouse click
                try:
                    _, mouse_x, mouse_y, _, _ = curses.getmouse()  # get mouse pos
                    desk.change_mouse_pos(mouse_x, mouse_y)
                    if restart_button.is_clicked(mouse_x, mouse_y):
                        # Restart the game
                        stdscr.clear()
                        return game(stdscr)
                    active_card: Card | None = desk.active_card_search()
                    if active_card:
                        desk.try_moving_active_card()
                    else:
                        desk.try_activate_some_card()
                    desk.check_stockpile()
                except Exception as e:
                    logger.error(e, exc_info=True)
        except Exception as e:
            logger.error(e, exc_info=True)

        stdscr.refresh()
        time.sleep(0.05)  # Prevent CPU hogging
