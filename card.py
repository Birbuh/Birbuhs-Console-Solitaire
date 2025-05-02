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

    def draw(self, x, y, is_stockpile):
        self.x = x
        self.y = y
        if self.turned:
            width = self.width
            height = self.height
        elif is_stockpile:
            width = self.width
            height = self.height
        else:
            width = self.width
            height = int(self.height / 2)

        for i in range(width):
            self.window.addch(self.y, self.x + i, curses.ACS_HLINE)
            self.window.addch(self.y + height, self.x + i, curses.ACS_HLINE)
        for i in range(height):
            self.window.addch(self.y + i, self.x, curses.ACS_VLINE)
            self.window.addch(self.y + i, self.x + width, curses.ACS_VLINE)

        # Drawing the corners:
        self.window.addch(self.y, self.x, curses.ACS_ULCORNER)
        self.window.addch(self.y, self.x + width, curses.ACS_URCORNER)
        self.window.addch(self.y + height, self.x, curses.ACS_LLCORNER)
        self.window.addch(self.y + height, self.x + width, curses.ACS_LRCORNER)

        if self.turned:
            card_symbol = self.get_symbol()
            self.window.addstr(self.y + 1, self.x + 1, card_symbol)
            self.window.addstr(
                self.y + self.height - 1, self.x + self.width - 2, card_symbol
            )
        else:
            self.window.addstr(self.y + 1, self.x + 1, "~~")

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
        if self.turned:
            pass
        elif not self.turned:
            self.turned = True

    def make_active(self, color_pair):
        try:
            logger.debug("IS IT WORKING?!?!!?!?!?!?")
            self.is_active = True
            for y in range(self.y + 1, self.y + self.height - 1):
                for x in range(self.x + 1, self.x + self.width - 1):
                    self.window.addch(y, x, " ", curses.color_pair(color_pair))
                    logger.debug("IS IT WORKING?!?!!?!?!?!?")
        except Exception as e:
            logger.error(e)

    def is_clicked(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height

    def may_move(self, other_card):
        if self.num == other_card.num:
            other_card.x = self.x
            other_card.y = self.y + 3
