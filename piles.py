import curses

from card import Card, CardColorEnum


class Pile:
    def __init__(self):
        self.card_list = []

    def is_empty(self):
        if self.card_list:
            return False
        else:
            return True


class FoundationPile(Pile):
    def __init__(self, window: curses.window, color):
        super().__init__()
        self.window = window
        self.width = 8
        self.height = 6
        self.x = window.getmaxyx[1] - 10
        self.y = 5
        if color == CardColorEnum.HEARTS:
            self.x -= 30
        elif color == CardColorEnum.DIAMONDS:
            self.x -= 20
        elif color == CardColorEnum.CLUBS:
            self.x -= 10

    def draw(self):
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
            self.window.addch(self.y + self.height, self.x + self.width, curses.ACS_LRCORNER)

    def maybe_move(self, card: Card):
        try:
            _ = self.card_list[card.num]
            return False
        except IndexError:
            try:
                if self.card_list:
                    _ = self.card_list[card.num - 1]
                self.card_list.append(card)
                card.x = self.x
                card.y = self.y
            except IndexError:
                return False


class TableauPile(Pile):
    def __init__(self):
        super().__init__()

    def add_card(self, card):
        self.card_list.append(card)


class Tableau:
    def __init__(self, cards: list[Card]):
        self.piles = [TableauPile() for _ in range(7)]
        # Distribute cards to piles (pile 1 gets 1 card, pile 7 gets 7 cards)
        for pile_num in range(7, 0, -1):
            current_pile = self.piles[7 - pile_num]  # Convert 7→0, 6→1, etc.

            # Take first 'pile_num' cards from remaining deck
            for i, card in enumerate(cards[:pile_num]):
                if i == pile_num - 1:  # Only top card is face-up
                    card.turned = True
                # Position cards diagonally (adjust coordinates as needed)
                card.draw(40 + (7 - pile_num) * 12, 5 + i * 2)
                current_pile.add_card(card)  # Add to current pile

            # Remove these cards from the main list
            cards = cards[pile_num:]


class StockPile:
    def __init__(self, card_list):
        self.card_list = card_list
