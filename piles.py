import curses
import logging

from card import Card, CardColorEnum, CardPileEnum


logger = logging.getLogger()


class Pile:
    """
    Parent pile class.

    Attributes:
        self.card_list: list of cards inside the pile
        self.x: x coord of the pile
        self.y: y coord of the pile
        self.width: width of the pile (same as the card's, 8)
        self.height: height of the pile (same as the **turned** card's, 6)
        self.window: The window in which everything is drawn.
    """

    def __init__(self):
        self.card_list: list[Card] = []
        self.x = None
        self.y = None
        self.width = 8
        self.height = 6
        self.window: curses.window = None
        self.turned_card_list: list[Card] | None = None

    def is_empty(self) -> bool:
        """Checking if the pile is empty."""
        if self.card_list:
            return False
        else:
            return True

    def is_last_card(self, card: Card):
        """Checking if the card is the last card from the pile.

        :param card: The card to check
        """
        try:
            return card == self.card_list[-1]
        except IndexError:
            return False

    def is_clicked(self, x: int, y: int) -> bool:
        """Checking for a click in the pile.

        :param x: The x coord of click
        :param y: The y coord of click

        """
        return (self.x <= x < (self.x + self.width)) and (
            self.y <= y < (self.y + self.height)
        )

    def draw_empty(self):
        """Drawing the empty pile (without cards)"""
        if not any(self.card_list):
            for i in range(self.width):
                self.window.addch(self.y, self.x + i, curses.ACS_HLINE)
                self.window.addch(self.y + self.height, self.x + i, curses.ACS_HLINE)
            for i in range(self.height):
                self.window.addch(self.y + i, self.x, curses.ACS_VLINE)
                self.window.addch(self.y + i, self.x + self.width, curses.ACS_VLINE)
            self.window.addch(self.y, self.x, curses.ACS_ULCORNER)
            self.window.addch(self.y, self.x + self.width, curses.ACS_URCORNER)
            self.window.addch(self.y + self.height, self.x, curses.ACS_LLCORNER)
            self.window.addch(
                self.y + self.height, self.x + self.width, curses.ACS_LRCORNER
            )

    def is_a_stock_pile(self) -> bool:
        """Checking if this pile is a StockPile."""
        if self.turned_card_list:
            return any(self.turned_card_list)
        try:
            self.can_move_from()
            return False
        except NotImplementedError:
            return True

    def is_in_card_list(self, card):
        return card in self.card_list

    def pile_or_card_clicked(self, x, y):
        """Check if last card in a pile is clicked (or, if it's not found, check the pile itself).

        :param x: The x coord of click
        :param y: The y coord of click
        """
        try:
            return self.card_list[-1].is_clicked(x, y)
        except IndexError:
            return self.is_clicked(x, y)

    # Interface methods: If not implemented in the inherited class,
    # it would raise the error.
    def can_move_to(self):
        raise NotImplementedError()

    def can_move_from(self):
        raise NotImplementedError()

    # Moving the card methods
    def move_to(self, count: int = -1):
        """Method to **TAKE THE CARD(S) OFF**
        Caution: many cards can be taken off.

        :param count: How many cards will get removed
        """

        if self.can_move_to():
            if self.turned_card_list:
                next_card = self.turned_card_list[-1]
                self.turned_card_list.remove(next_card)
                try:
                    self.turned_card_list[-1].turn()
                except IndexError:
                    pass
            else:
                if count == -1:
                    try:
                        next_card = self.card_list[-1]
                        self.card_list.remove(next_card)
                        self.card_list[-1].turn()
                    except IndexError:
                        pass
                else:
                    try:
                        next_card = self.card_list[count]
                        self.card_list.remove(next_card)
                        self.card_list[-1 + count].turn()
                    except Exception:
                        logger.error(
                            "Transfer of multiple cards went wrong.", exc_info=True
                        )

    def move_from_other_pile(self, card: Card | None):
        """Method to **PUT THE CARD ON THIS PILE**
        Caution: Only one card can be put at once.

        :param addy: The space to add to the original pile y.
        :param pile_enum: Card has to know, in which pile it is.
        :param card: The card to move to this pile.
        """
        if self.can_move_from():
            self.card_list.append(card)


class FoundationPile(Pile):
    """Foundation pile class

    Attributes:
        self.color: The color (symbol) of the pile
        self.card_list: list of cards inside the pile
        self.x: x coord of the pile
        self.y: y coord of the pile
        self.width: width of the pile (same as the card's, 8)
        self.height: height of the pile (same as the **turned** card's, 6)
        self.window: The window in which everything is drawn.
    """

    def __init__(self, window: curses.window, color):
        super().__init__()
        self.x = 112
        self.y = 1
        self.window = window
        self.color = color
        if self.color == CardColorEnum.HEARTS:
            self.x -= 30
        elif self.color == CardColorEnum.DIAMONDS:
            self.x -= 20
        elif self.color == CardColorEnum.CLUBS:
            self.x -= 10
        # else:     # spades will have the default x.
        # pass

    def draw(self):
        """Draws the Foundation piles."""
        if self.is_empty():
            for i in range(self.width):
                self.window.addch(self.y, self.x + i, curses.ACS_HLINE)
                self.window.addch(self.y + self.height, self.x + i, curses.ACS_HLINE)
            for i in range(self.height):
                self.window.addch(self.y + i, self.x, curses.ACS_VLINE)
                self.window.addch(self.y + i, self.x + self.width, curses.ACS_VLINE)
            self.window.addch(self.y, self.x, curses.ACS_ULCORNER)
            self.window.addch(self.y, self.x + self.width, curses.ACS_URCORNER)
            self.window.addch(self.y + self.height, self.x, curses.ACS_LLCORNER)
            self.window.addch(
                self.y + self.height, self.x + self.width, curses.ACS_LRCORNER
            )
            if self.color == CardColorEnum.HEARTS:
                symbol = "♥"
            elif self.color == CardColorEnum.DIAMONDS:
                symbol = "♦"
            elif self.color == CardColorEnum.CLUBS:
                symbol = "♣"
            else:  # SPADES
                symbol = "♠"

            self.window.addstr(
                int(self.y + self.height - 1), int(self.x + self.width / 2 - 1), symbol
            )
        else:
            self.card_list[-1].draw(self.x, self.y, CardPileEnum.FOUNDATIONS, True)

    def can_move(self, card: Card) -> bool:
        """Moves (if it's possible) a card to the Foundation pile.

        :param card: The card to check if it can move into the pile the method is called on.
        """
        if self.color == card.color:
            num_val = card.num.value
            if num_val == 1:
                if self.is_empty():
                    return True
            else:
                try:
                    if num_val == self.card_list[-1].num.value + 1:
                        return True
                except IndexError:
                    pass
        return False

    # Method override
    def can_move_from(self) -> bool:
        return True


class TableauPile(Pile):
    """
    Simple class for one of the 7 main piles.

    Attributes:
        self.card_list: list of cards inside the pile
        self.x: x coord of the pile
        self.y: y coord of the pile
        self.width: width of the pile (same as the card's, 8)
        self.height: height of the pile (same as the **turned** card's, 6)
        self.window: The window in which everything is drawn.
    """

    def __init__(self, card_list: list[Card], x: int, window: curses.window):
        super().__init__()
        self.card_list = card_list
        self.window = window
        self.x = x
        self.y = 9

    def init_draw(self):
        for i, card in enumerate(self.card_list):
            if i == len(self.card_list) - 1:  # Last card should be face up
                card.draw(self.x, self.y + i * 2, CardPileEnum.TABLEAU, True)
            else:
                card.draw(self.x, self.y + i * 2, CardPileEnum.TABLEAU, False)

    def draw(self):
        for i, card in enumerate(self.card_list):
            card.draw(
                self.x, self.y + i * 2, CardPileEnum.TABLEAU, card.get_turned_status()
            )
        for card in self.card_list:
            if card.turned:
                card.redraw()

    def return_next_cards(self, card: Card) -> list[Card]:
        if card in self.card_list:
            card_index = self.card_list.index(card)
            return self.card_list[card_index:]

    def can_move_card(self, card: Card | None, cards: list[Card] | None = None) -> bool:
        try:
            last_card = self.card_list[-1]
            if card.num.value == last_card.num.value - 1 and (
                card.color_check() != last_card.color_check()
            ):
                return True
        except IndexError:
            if card.num.value == 13:  # King
                return True
        return False

    def iterate_and_activate(self, mouse_x, mouse_y) -> Card:
        for card in self.card_list:
            if card.is_clicked(mouse_x, mouse_y) and card.turned:
                card.activate()
                return card

    def last_card_relative_y(self) -> int:
        return self.card_list[-1].y - 9

    def reactivate_last_card(self):
        """Used for debug"""
        try:
            card = self.card_list[-1]
            card.activate()
            card.deactivate()
        except IndexError:
            pass

    # Method override
    def can_move_to(self) -> bool:
        return True

    def can_move_from(self) -> bool:
        return True


class StockPile(Pile):
    """Pile in which you have the rest of the cards

    Attributes:
        self.turned_card_list: basically the waste pile card_list
        self.card_list: list of cards inside the pile
        self.x: x coord of the pile
        self.y: y coord of the pile
        self.width: width of the pile (same as the card's, 8)
        self.height: height of the pile (same as the **turned** card's, 6)
        self.window: The window in which everything is drawn.
    """

    def __init__(self, card_list: list[Card], window: curses.window):
        super().__init__()
        self.card_list = card_list
        self.window = window
        self.x = 40
        self.y = 1
        self.turned_card_list: list[Card] = []

    def init_draw(self):
        for card in self.card_list:
            card.draw(self.x, self.y, CardPileEnum.STOCK, False)
        for i in range(self.width):
            self.window.addch(self.y, self.x + 10 + i, curses.ACS_HLINE)
            self.window.addch(self.y + self.height, self.x + 10 + i, curses.ACS_HLINE)
        for i in range(self.height):
            self.window.addch(self.y + i, self.x + 10, curses.ACS_VLINE)
            self.window.addch(self.y + i, self.x + 10 + self.width, curses.ACS_VLINE)
        self.window.addch(self.y, self.x + 10, curses.ACS_ULCORNER)
        self.window.addch(self.y, self.x + 10 + self.width, curses.ACS_URCORNER)
        self.window.addch(self.y + self.height, self.x + 10, curses.ACS_LLCORNER)
        self.window.addch(
            self.y + self.height, self.x + 10 + self.width, curses.ACS_LRCORNER
        )

    def draw(self):
        """Drawing the stockpile."""
        if self.card_list:
            self.card_list[-1].draw(self.x, self.y, CardPileEnum.STOCK, False)
        else:
            self.draw_empty()

        if self.turned_card_list:
            self.turned_card_list[-1].draw(
                self.x + 10, self.y, CardPileEnum.STOCK, True
            )
        else:
            # Draw empty turned pile
            for i in range(self.width):
                self.window.addch(self.y, self.x + 10 + i, curses.ACS_HLINE)
                self.window.addch(
                    self.y + self.height, self.x + 10 + i, curses.ACS_HLINE
                )
            for i in range(self.height):
                self.window.addch(self.y + i, self.x + 10, curses.ACS_VLINE)
                self.window.addch(
                    self.y + i, self.x + 10 + self.width, curses.ACS_VLINE
                )
            self.window.addch(self.y, self.x + 10, curses.ACS_ULCORNER)
            self.window.addch(self.y, self.x + 10 + self.width, curses.ACS_URCORNER)
            self.window.addch(self.y + self.height, self.x + 10, curses.ACS_LLCORNER)
            self.window.addch(
                self.y + self.height, self.x + 10 + self.width, curses.ACS_LRCORNER
            )

    def check_card(self) -> bool:
        """
        Turning the first (technically last) card of the stockpile.
        If card_list is empty, all turned cards will go back to the stock pile.
        """
        if self.card_list:  # Turn over the top card
            card = self.card_list[-1]
            logger.debug("stock_cart modified in chceck_card (remove)")
            self.card_list.remove(card)
            self.turned_card_list.append(card)
            card.turn()
            return True
        else:  # Reset the pile - move all turned cards back to stock pile
            if self.turned_card_list:
                cards_to_move = list(reversed(self.turned_card_list))
                self.turned_card_list = []
                for card in cards_to_move:
                    card.turn()  # Turn the card back down
                    logger.debug("stock_cart modified in chceck_card (append)")
                    self.card_list.append(card)
                return True
        return False

    def uncheck_card(self) -> bool:
        if self.turned_card_list:
            card = self.turned_card_list[-1]
            self.turned_card_list.remove(card)
            self.card_list.append(card)
            card.turn()
            return True
        return False

    def is_turned_list_empty(self) -> bool:
        return not self.turned_card_list

    def try_activate(self, mouse_x, mouse_y) -> Card:
        """Returns the card if it's clicked and can be activated"""
        if self.turned_card_list:
            card = self.turned_card_list[-1]
            if card.is_clicked(mouse_x, mouse_y):
                card.activate()
                return card
        return None

    def can_move_to(self) -> bool:
        return True
