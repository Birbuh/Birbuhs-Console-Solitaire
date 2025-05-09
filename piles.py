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


class TableauPile(Pile):
    """Simple class for one of the 7 main piles."""

    def __init__(self):
        super().__init__()

    def try_move_card(self, card: Card):
        last_card = self.card_list[-1]
        if card.num.value == last_card.num.value + 1 and (
            card.color_check() == "black" and last_card.color_check()
        ):
            self.card_list.append(card)
            card.undraw()
            card.draw(last_card.x, last_card.y + 4)
            card.pile = "Tableau"


class Tableau:
    """Class that's drawing the whole Tableau on the window."""

    def __init__(self, cards: list[Card]):
        self.cards = cards

    def draw(self):
        """It has to be called if you want to draw the Tableau"""
        self.piles = [TableauPile() for _ in range(7)]
        # Distribute cards to piles (pile 1 gets 1 card, pile 7 gets 7 cards)
        for pile_num in range(7, 0, -1):
            current_pile = self.piles[7 - pile_num]  # Convert 7→0, 6→1, etc.

            # Take first 'pile_num' cards from remaining deck
            for i, card in enumerate(self.cards[:pile_num]):
                if i == pile_num - 1:  # Only top card is face-up
                    card.draw(40 + (7 - pile_num) * 12, 20 + i * 2, "Tableau", True)
                    current_pile.card_list.append(card)  # Add to current pile
                else:
                    # Position cards diagonally (adjust coordinates as needed)
                    card.draw(40 + (7 - pile_num) * 12, 20 + i * 2, "Tableau", False)
                    current_pile.card_list.append(card)  # Add to current pile
            # Remove these cards from the main list
            self.cards = self.cards[pile_num:]

        return self.cards, self.piles


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
        if self.card_list:
            # Turn over the top card
            card = self.card_list[-1]
            try:
                next_card = self.card_list[-2]
            except IndexError:
                next_card = None
            try:
                turned_card = self.turned_card_list[-1]
            except IndexError:
                turned_card = None

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

        else: # Reset the pile - move all turned cards back to stock pile
            cards_to_move = list(self.turned_card_list)
            for card in cards_to_move:
                card.undraw()
                card.draw(self.x, self.y, "Stock", False)
                self.card_list.append(card)
                self.turned_card_list.remove(card)
