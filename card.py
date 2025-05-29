import curses
import logging
from enum import Enum


logger = logging.getLogger()


class CardPileEnum(Enum):
    FOUNDATIONS = 0
    TABLEAU = 1
    STOCK = 2


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

    Attributes:
        self.color: Color (or symbol) of the card
        self.num: Number of the card
        self.window:
        self.width: Width of the card (8)
        self.height: Width of the card (6 (or 3 if unturned in Tableau))
        self.turned: Variable storing the info about the turned status (True or False)
        self.is_active: Variable storing the info about the active status (True or False)
        self.pile: Variable storing the info about in which pile the card is
        self.is_drawn: ???
        self.x: x coord of the card
        self.y: y coord of the card
    """

    def __init__(self, color, num, window: curses.window):
        self.color: Enum.name = color
        self.num: Enum.name = num
        self.window = window
        self.width: int = 8
        self.height: int = 6
        self.turned: bool = False
        self.is_active: bool = False
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_MAGENTA)
        self.pile: CardPileEnum | None = None
        self.drawn: bool = False
        self.x = None
        self.y = None

    def draw(
        self,
        x: int = None,
        y: int = None,
        pile: CardPileEnum | None = None,
        turned: bool = False,
    ):
        """Draws the card"""
        if not self.pile:
            self.pile = pile
        self.turned = turned
        if x and y:
            self.x = x
            self.y = y
        if self.turned or self.pile == CardPileEnum.STOCK:
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
        except Exception:
            logger.error("Error drawing card border", exc_info=True)

        # Draw card content
        if self.turned:
            card_symbol = self.get_symbol()
            bottom_symbol_shift = 2
            if len(card_symbol) > 2: 
                bottom_symbol_shift = 3

            if self.color_check() == "black":
                if not self.is_active:
                    self.window.addstr(self.y + 1, self.x + 1, card_symbol)
                    self.window.addstr(
                        self.y + self.height - 1, self.x + self.width - bottom_symbol_shift, card_symbol
                    )
                else:
                    self.window.addstr(
                        self.y + 1, self.x + 1, card_symbol, curses.color_pair(3)
                    )
                    self.window.addstr(
                        self.y + self.height - 1,
                        self.x + self.width - bottom_symbol_shift, # - self.move_num,
                        card_symbol,
                        curses.color_pair(3),
                    )
            else:
                if not self.is_active:
                    self.window.addstr(
                        self.y + 1, self.x + 1, card_symbol, curses.color_pair(1)
                    )
                    self.window.addstr(
                        self.y + self.height - 1,
                        self.x + self.width - bottom_symbol_shift, # - self.move_num,
                        card_symbol,
                        curses.color_pair(1),
                    )
                else:
                    self.window.addstr(
                        self.y + 1, self.x + 1, card_symbol, curses.color_pair(4)
                    )
                    self.window.addstr(
                        self.y + self.height - 1,
                        self.x + self.width - bottom_symbol_shift,
                        card_symbol,
                        curses.color_pair(4),
                    )

        else:
            try:
                self.window.addstr(self.y + 1, self.x + 1, "~~~~")
            except curses.error:
                pass
            if not height == int(self.height / 2):
                try:
                    self.window.addstr(
                        self.y + self.height - 1, self.x + self.width - 2, "~~"
                    )
                except curses.error:
                    pass
        self.window.refresh()
        self.drawn = True

    def is_a_king(self) -> bool:
        return self.num.value == 13

    def undraw(self):
        for i in range(self.height + 1):
            self.window.move(self.y + i, self.x)
            self.window.addstr(" " * int(self.width + 1))
        self.window.refresh()
        self.drawn = False

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
        elif self.num == CardNumberEnum.CARD_NUM_10:
            num_symbol = "10"
            # self.move_num = 1
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
        """Turns the card up.

        (or down if it's turned and in stock pile)"""
        if (
            self.turned and self.pile == CardPileEnum.STOCK
        ):  # Card can't be turned down except for stockpile.
            self.turned = False
        elif not self.turned:
            self.turned = True
        # Ignore all other

    def redraw(self):
        self.undraw()
        self.draw(self.x, self.y, self.pile, self.turned)

    def return_pile(self):
        return self.pile.name

    def activate(self):
        """Makes the card active and marking it red"""
        try:
            self.is_active = True
            # Fill the card with colored background - safely
            for y in range(self.y + 1, self.y + self.height):
                for x in range(self.x + 1, self.x + self.width):
                    try:
                        self.window.addch(y, x, " ", curses.color_pair(2))
                    except curses.error:
                        pass
            self.draw(self.x, self.y, self.pile, self.turned)

            self.window.refresh()
        except Exception as e:
            logger.error(e, exc_info=True)

    def deactivate(self):
        """Restoring the card to it's original state."""
        try:
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
            self.redraw()
        except Exception as e:
            logger.error(e, exc_info=True)

    def is_clicked(self, x, y) -> bool:
        """Checking if the card is clicked

        :param x: The x coord of click
        :param y: The y coord of click
        """
        try:
            return (self.x <= x < (self.x + self.width)) and (
                self.y <= y < (self.y + self.height)
            )
        except Exception:
            logger.error(str(self), exc_info=True)

    def color_check(self) -> str:
        """Checking and returning the **COLOR** of the card (not the symbol)"""
        if self.color.value % 2 == 1:
            return "black"
        else:
            return "red"

    def change_piles(self, new_pile):
        """Changing the pile

        :param new_pile: New pile to replace the old one with.
        """
        self.pile = new_pile

    def get_turned_status(self):
        return self.turned

    def __str__(self):
        return f"Card: {self.color}, {self.num}, {self.pile}"
