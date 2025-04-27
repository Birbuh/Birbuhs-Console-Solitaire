import curses
import logging



logger = logging.getLogger()

class Button:
    """Parent class for all buttons."""
    def __init__(self, x, y, width, height, stdscr: curses.window):
        box = curses.newwin(height, width, y, x)
        box.border(1)
        box.box()
        box.refresh()
