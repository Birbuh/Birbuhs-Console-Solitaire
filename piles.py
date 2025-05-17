import curses

from card import Card, CardColorEnum


class Pile:
    """Parent pile class"""

    def __init__(self):
        self.card_list: list[Card] = []
        self.x = None
        self.y = None
        self.width = 8
        self.height = 6

    def is_empty(self) -> bool:
        if self.card_list:
            return False
        else:
            return True

    def is_clicked(self, x, y) -> bool:
        """Checking for a click in the pile."""
        return self.x <= x < (self.x + self.width) and self.y <= y < (
            self.y + self.height
        )
    
    def is_in_card_list(self, card):
        return card in self.card_list

    def last_card_clicked(self, x, y):
        return self.card_list[-1].is_clicked(x, y)

    # Interface methods
    def can_move_to(self):
        raise NotImplementedError()

    def can_move_from(self):
        raise NotImplementedError()

    # Moving the card methods
    def move_to(self, pile_o, pile_str):
        if self.can_move_to():
            try:
                next_card = self.card_list[-1]
                self.card_list.remove(next_card)
                next_card.undraw()
                next_card.draw(pile_o.x, pile_o.y, pile_str, True)
            except IndexError:
                pass

    def move_from_other_pile(self, card: Card, addy, pile_str):
        if self.can_move_from():
            self.card_list.append(card)
            card.undraw()
            card.draw(self.x, self.y + addy, pile_str, True)


class FoundationPile(Pile):
    """Foundation piles"""

    def __init__(self, window: curses.window, color):
        super().__init__()
        self.window = window
        self.x = 112
        self.y = 5
        if color == CardColorEnum.HEARTS:
            self.x -= 30
        elif color == CardColorEnum.DIAMONDS:
            self.x -= 20
        elif color == CardColorEnum.CLUBS:
            self.x -= 10
        self.color = color

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
            suit_symbol = "♥"
        elif self.color == CardColorEnum.DIAMONDS:
            suit_symbol = "♦"
        elif self.color == CardColorEnum.CLUBS:
            suit_symbol = "♣"
        else:  # SPADES
            suit_symbol = "♠"

        self.window.addstr(
            int(self.y + self.height - 1), int(self.x + self.width / 2 - 1), suit_symbol
        )

    def maybe_move(self, card: Card) -> bool:
        """Moves (if it's possible) a card to the Foundation pile."""
        self.num = card.num.value
        if self.num == 0:
            return False
        if self.num == 1:
            if self.is_empty():
                self.card_list.append(card)
                card.undraw()
                card.draw(self.x, self.y, False, True)
                return True
        else:
            if self.num == self.card_list[self.num].num.value + 1:
                self.card_list.append(card)
                card.undraw()
                self.card_list[self.num - 1].undraw()
                card.draw(self.x, self.y, "Foundation", True)
                return True
            else:
                return False

    # Method override
    def can_move_from(self):
        return True


class TableauPile(Pile):
    """
    Simple class for one of the 7 main piles.
    card_list: list[Card]; that is a list filled with the cards that belong in the pile.
    x: int; coordinate of the pile on the x axis
    """

    def __init__(self, card_list: list[Card], x: int):
        super().__init__()
        self.card_list = card_list
        self.x = x
        self.y = 20

    def draw(self):
        for i, card in enumerate(self.card_list):
            if i == len(self.card_list) - 1:  # Last card should be face up
                card.draw(self.x, 20 + i * 2, "Tableau", True)
            else:
                card.draw(self.x, 20 + i * 2, "Tableau", False)

    def try_move_card(self, card: Card):
        last_card = self.card_list[-1]
        if card.num.value == last_card.num.value + 1 and (
            card.color_check() != last_card.color_check()
        ):
            self.card_list.append(card)
            card.undraw()
            card.draw(last_card.x, last_card.y + 4)
            card.pile = "Tableau"

    def iterate_and_activate(self, mouse_x, mouse_y) -> bool:
        for card in self.card_list:
            if card.is_clicked(mouse_x, mouse_y) and card.turned:
                card.activate()
                return True
        return False

    # Method override
    def can_move_to(self) -> bool:
        return True

    def can_move_from(self) -> bool:
        return True


class StockPile(Pile):
    """Pile in which you have the rest of the cards"""

    def __init__(self, card_list: list[Card]):
        super().__init__()
        self.card_list = card_list
        self.x = 40
        self.y = 5
        self.turned_card_list: list[Card] = []

    def draw(self):
        """Drawing..."""
        for card in self.card_list:
            card.draw(self.x, self.y, "Stock", False)

    def draw_empty(self, window: curses.window):
        for i in range(self.width):
            window.addch(self.y, self.x + i, curses.ACS_HLINE)
            window.addch(self.y + self.height, self.x + i, curses.ACS_HLINE)
        for i in range(self.height):
            window.addch(self.y + i, self.x, curses.ACS_VLINE)
            window.addch(self.y + i, self.x + self.width, curses.ACS_VLINE)
        window.addch(self.y, self.x, curses.ACS_ULCORNER)
        window.addch(self.y, self.x + self.width, curses.ACS_URCORNER)
        window.addch(self.y + self.height, self.x, curses.ACS_LLCORNER)
        window.addch(self.y + self.height, self.x + self.width, curses.ACS_LRCORNER)

    def check_card(self, window: curses.window):
        """
        Turning the first (technically last) card of the stockpile.
        If card_list is empty, draw_empty(), and in the next click all of the cards will go back to it's place.
        """
        if self.turned_card_list:
            turned_card = self.turned_card_list[-1]
        else:
            turned_card = None

        if self.card_list:  # Turn over the top card
            try:
                next_card = self.card_list[-2]
            except IndexError:
                next_card = None
            card = self.card_list[-1]

            self.card_list.remove(card)
            self.turned_card_list.append(card)
            card.turn()
            card.undraw()

            # Draw the next card in the stock pile or empty pile
            if next_card:
                next_card.draw(self.x, self.y, "Stock", False)
            else:
                self.draw_empty(window)

            # Undraw previous turned card if exists
            if turned_card:
                turned_card.undraw()

            # Draw the newly turned card
            card.draw(self.x + 10, self.y, "Stock", True)

        else:  # Reset the pile - move all turned cards back to stock pile
            cards_to_move = list(self.turned_card_list)
            for card in cards_to_move:
                card.undraw()
                card.draw(self.x, self.y, "Stock", False)
                self.card_list.append(card)
                self.turned_card_list.remove(card)

    def is_turned_list_empty(self):
        return any(self.turned_card_list)

    def iterate_and_activate(self, mouse_x, mouse_y) -> bool:
        card = self.turned_card_list[-1]
        if card.is_clicked(mouse_x, mouse_y):
            card.activate()
            return True
        else:
            return False

    def can_move_to(self):
        return True
