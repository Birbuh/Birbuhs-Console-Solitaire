import curses

from card import Card, CardColorEnum


class Pile:
    """Parent pile class"""

    def __init__(self):
        self.card_list = []

    def is_empty(self) -> bool:
        if self.card_list:
            return False
        else:
            return True


class FoundationPile(Pile):
    """Foundation piles"""

    def __init__(self, window: curses.window, color):
        super().__init__()
        self.window = window
        self.width = 8
        self.height = 6
        self.x = 112
        self.y = 5
        if color == CardColorEnum.HEARTS:
            self.x -= 30
        elif color == CardColorEnum.DIAMONDS:
            self.x -= 20
        elif color == CardColorEnum.CLUBS:
            self.x -= 10

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

    def maybe_move(self, card: Card) -> bool:
        """Moves (if it's possible) a card to the Foundation pile."""
        try:
            _ = self.card_list[card.num.value]
            return False
        except IndexError:
            try:
                if self.card_list:
                    if self.is_empty():
                        self.card_list.append(card)
                        card.x = self.x
                        card.y = self.y
                        return True
                    _ = self.card_list[card.num.value - 1]
                self.card_list.append(card)
                card.x = self.x
                card.y = self.y
            except IndexError:
                return False

    def is_clicked(self, x, y) -> bool:
        """Checking for a click in the pile."""
        return self.x <= x < (self.x + self.width) and self.y <= y < (
            self.y + self.height
        )


class TableauPile(Pile):
    """Simple class for one of the 7 main piles."""

    def __init__(self):
        super().__init__()

    def add_card(self, card):
        """Adds a card to the pile."""
        self.card_list.append(card)


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
                    card.turned = True
                # Position cards diagonally (adjust coordinates as needed)
                card.draw(40 + (7 - pile_num) * 12, 20 + i * 2, False)
                current_pile.add_card(card)  # Add to current pile

            # Remove these cards from the main list
            self.cards = self.cards[pile_num:]

        return self.cards


class StockPile(Pile):
    """Pile in which you have the rest of the cards"""

    def __init__(self, card_list: list[Card]):
        self.card_list = card_list

    def draw(self):
        """Drawing..."""
        for card in self.card_list:
            card.draw(40, 5, True)
