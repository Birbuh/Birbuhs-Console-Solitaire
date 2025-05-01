import curses
import logging
import time
import itertools
import random
from card import Card, CardColorEnum, CardNumberEnum
from buttons import Button
from piles import FoundationPile, Tableau, TableauPile, StockPile

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

    # Create and draw restart button
    restart_button = Button(10, 10, "Restart the game", stdscr)
    restart_button.draw()

    # Create and shuffle cards
    cards = [
        Card(color, num, stdscr)
        for color, num in itertools.product(CardColorEnum, CardNumberEnum)
    ]
    random.shuffle(cards)
    logger.debug(cards)

    # Display cards
    Tableau(cards)

    # Game instructions
    stdscr.addstr(2, 10, "Solitaire Game")
    stdscr.addstr(3, 10, "Press 'q' to quit")

    # Game loop
    running = True
    while running:
        try:
            key = stdscr.getch()
            if key == ord("q"):
                running = False
            elif key == curses.KEY_MOUSE:
                try:
                    _, mouse_x, mouse_y, _, _ = curses.getmouse()
                    if restart_button.is_clicked(mouse_x, mouse_y):
                        # Restart the game
                        stdscr.clear()
                        return game(stdscr)
                except curses.error:
                    pass
        except curses.error:
            # No input available
            pass

        stdscr.refresh()
        time.sleep(0.1)  # Prevent CPU hogging
