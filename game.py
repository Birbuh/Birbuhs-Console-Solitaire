import curses
import logging

import settings
from buttons import Button


logger = logging.getLogger()

def start_game(stdscr: curses.window) -> bool:
    """Modifies the settings.py and prepares for launching game()"""
    button = Button(10, 10, 5, 15, stdscr)
    logger.debug("abc")
    if button:
        settings.default_lang = "pl"

# def game(stdscr: curses.window):
