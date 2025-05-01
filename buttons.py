import curses
import logging


logger = logging.getLogger()


class Button:
    """
    Represents a clickable instance (button)

    x = initial x coordinate of a button;
    y = initial y coordinate of a button;
    width = witdth of a button;
    height = height of a button;
    window = window in which the button will appear
    """

    def __init__(self, x: int, y: int, text: str, window: curses.window):
        self.x = x
        self.y = y
        self.width = len(text) + 5
        self.height = 3
        self.text = text
        self.window = window

    def draw(self):
        """Drawing the button"""
        # Drawing the borders:
        for i in range(self.width):
            self.window.addch(self.y, self.x + i, curses.ACS_HLINE)
            self.window.addch(self.y + self.height, self.x + i, curses.ACS_HLINE)
        for i in range(self.height):
            self.window.addch(self.y + i, self.x, curses.ACS_VLINE)
            self.window.addch(self.y + i, self.x + self.width, curses.ACS_VLINE)

        # Drawing the corners:
        self.window.addch(self.y, self.x, curses.ACS_ULCORNER)
        self.window.addch(self.y, self.x + self.width, curses.ACS_URCORNER)
        self.window.addch(self.y + self.height, self.x, curses.ACS_LLCORNER)
        self.window.addch(
            self.y + self.height, self.x + self.width, curses.ACS_LRCORNER
        )

        # Drawing the text:
        self.window.addstr(self.y + 1, self.x + 2, self.text)
        self.window.refresh()

    def is_clicked(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height
