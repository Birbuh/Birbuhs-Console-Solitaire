import curses
import logging
from enum import Enum


logger = logging.getLogger()


class CardColorEnum(Enum):
    HEARTS = 0
    SPADES = 1
    DIAMONDS = 2
    CLUBS = 3


class CardNumberEnum(Enum):
    """
    Storing all possibilities for card numbers

    WARNING: it's from 1 to 13, not from 0 to 12,
    because it would be easier to draw cards this way.
    """

    ACE = 1
    CARD_NUM_2 = 2
    CARD_NUM_3 = 3
    CARD_NUM_4 = 4
    CARD_NUM_5 = 5
    CARD_NUM_6 = 6
    CARD_NUM_7 = 7
    CARD_NUM_8 = 8
    CARD_NUM_9 = 9
    CARD_NUM_10 = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card:
    """
    Objects of this class will represent cards on the table.
    """

    def __init__(self, color, num, window: curses.window):
        self.color = color
        self.num = num
        self.window = window
        self.width = 8
        self.height = 6
        self.turned = False
        self.is_active = False
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        self.pile = None



    def draw(self, x:int=None, y:int=None, pile:str|None=None, turned:bool=False):
        self.pile = pile
        """Draws the card"""
        self.turned = turned
        if x and y:
            self.x = x
            self.y = y
        if self.turned or self.pile == "Stock":
            width = self.width
            height = self.height
        else:
            width = self.width
            height = int(self.height / 2)

        # Draw the card border safely with error handling
        try:
            # Draw horizontal lines
            for i in range(width):
                try:
                    self.window.addch(self.y, self.x + i, curses.ACS_HLINE)
                except curses.error:
                    pass
                try:
                    self.window.addch(self.y + height, self.x + i, curses.ACS_HLINE)
                except curses.error:
                    pass

            # Draw vertical lines
            for i in range(height):
                try:
                    self.window.addch(self.y + i, self.x, curses.ACS_VLINE)
                except curses.error:
                    pass
                try:
                    self.window.addch(self.y + i, self.x + width, curses.ACS_VLINE)
                except curses.error:
                    pass

            # Drawing the corners:
            try:
                self.window.addch(self.y, self.x, curses.ACS_ULCORNER)
            except curses.error:
                pass
            try:
                self.window.addch(self.y, self.x + width, curses.ACS_URCORNER)
            except curses.error:
                pass
            try:
                self.window.addch(self.y + height, self.x, curses.ACS_LLCORNER)
            except curses.error:
                pass
            try:
                self.window.addch(self.y + height, self.x + width, curses.ACS_LRCORNER)
            except curses.error:
                pass
        except Exception as e:
            logger.error(f"Error drawing card border: {e}")

        # Draw card content
        if self.turned:
            card_symbol = self.get_symbol()
            self.window.addstr(self.y + 1, self.x + 1, card_symbol)
            self.window.addstr(
                self.y + self.height - 1, self.x + self.width - 2, card_symbol
            )
        else:
            self.window.addstr(self.y + 1, self.x + 1, "~~~~~")
            if not height == int(self.height / 2):
                self.window.addstr(
                    self.y + self.height - 1, self.x + self.width - 2, "~~"
                )
        self.window.refresh()

    def undraw(self):
        for i in range(self.height + 1):
            self.window.move(self.y + i, self.x)
            self.window.addstr(" " * int(self.width+1))
        self.window.refresh()

    def get_symbol(self):
        """Returns a string representation of the card"""
        # Card number representation
        if self.num == CardNumberEnum.ACE:
            num_symbol = "A"
        elif self.num == CardNumberEnum.JACK:
            num_symbol = "J"
        elif self.num == CardNumberEnum.QUEEN:
            num_symbol = "Q"
        elif self.num == CardNumberEnum.KING:
            num_symbol = "K"
        else:
            num_symbol = str(self.num.value)

        # Card suit representation
        if self.color == CardColorEnum.HEARTS:
            suit_symbol = "♥"
        elif self.color == CardColorEnum.DIAMONDS:
            suit_symbol = "♦"
        elif self.color == CardColorEnum.CLUBS:
            suit_symbol = "♣"
        else:  # SPADES
            suit_symbol = "♠"
        return f"{num_symbol}{suit_symbol}"

    def turn(self):
        """Turns the card up."""
        if self.turned:
            pass
        elif not self.turned:
            self.turned = True

    def activate(self):
        """Makes the card active and marking it red"""
        try:
            logger.debug(f"Activating the card: {self.get_symbol()}")
            self.is_active = True
            # Fill the card with colored background - safely
            for y in range(self.y + 2, self.y + self.height - 1):
                for x in range(self.x + 2, self.x + self.width - 1):
                    try:
                        self.window.addch(y, x, " ", curses.color_pair(2))
                    except curses.error:
                        pass

            self.window.refresh()
        except Exception as e:
            logger.error(e, exc_info=True)

    def deactivate(self):
        """Restoring the card to it's original state."""
        try:
            logger.debug(f"Deactivating the card {self.get_symbol()}")
            self.is_active = False
            # Clearing the red background
            for y in range(self.y + 2, self.y + self.height - 1):
                for x in range(self.x + 2, self.x + self.width - 1):
                    try:
                        self.window.addch(y, x, " ")  # Default color (black on white)
                    except Exception as e:
                        logger.error(e, exc_info=True)
            # Redraw the card content to ensure it's visible
            if self.turned:
                card_symbol = self.get_symbol()
                self.window.addstr(self.y + 1, self.x + 1, card_symbol)
                self.window.addstr(
                    self.y + self.height - 1, self.x + self.width - 2, card_symbol
                )
        except Exception as e:
            logger.error(e, exc_info=True)

    def is_clicked(self, x, y) -> bool:
        """Checking if the card is clicked"""
        return (self.x <= x < (self.x + self.width)) and (
            self.y <= y < (self.y + self.height)
        )

    def color_check(self) -> str:
        if self.color.value & 2 == 1:
            return "black"
        else:
            return "red"