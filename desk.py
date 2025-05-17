import curses
import random
import itertools

from piles import TableauPile, FoundationPile, StockPile
from card import Card, CardColorEnum, CardNumberEnum, CardPileEnum


class Desk:
    """Class that's drawing the whole Tableau on the window."""

    cards: list[Card] = []
    foundation_piles: list[FoundationPile] = []
    tableau_piles: list[TableauPile] = []
    piles = []

    def __init__(self, window: curses.window):
        self.window = window

    def initialize(self) -> list[Card]:
        """Initializing all of the desk's content."""

        # Initialize all cards
        cards = [
            Card(color, num, self.window)
            for color, num in itertools.product(CardColorEnum, CardNumberEnum)
        ]
        random.shuffle(cards)  # Shuffling the cards

        # Making these cards group for Tableau and Stock piles.
        self.tableau_cards = cards[:28]
        self.stock_cards = cards[28:]

        # Initialize all classes
        # 7 TableauPile instances
        self.initialize_tableau(self.tableau_cards)

        # 4 FoundationPile instances
        self.foundation_hearts = FoundationPile(self.window, CardColorEnum.HEARTS)
        self.foundation_diamonds = FoundationPile(self.window, CardColorEnum.DIAMONDS)
        self.foundation_clubs = FoundationPile(self.window, CardColorEnum.CLUBS)
        self.foundation_spades = FoundationPile(self.window, CardColorEnum.SPADES)
        # Grouping them
        self.foundation_piles = [
            self.foundation_hearts,
            self.foundation_diamonds,
            self.foundation_clubs,
            self.foundation_spades,
        ]

        # 1 StockPile instance
        self.stock_pile = StockPile(self.stock_cards)


    def initialize_tableau(self, cards: list[Card]):
        for i in range(7, 0, -1):
            lasted_cards = cards[:i]
            cards = cards[i:]
            current_pile = TableauPile(lasted_cards, 28 + 12 * i)
            self.tableau_piles.append(current_pile)

    def init_draw(self):
        """Drawing the desk's content (for the first time only)"""
        # Drawing the Foundation piles
        self.foundation_hearts.draw()
        self.foundation_diamonds.draw()
        self.foundation_clubs.draw()
        self.foundation_spades.draw()

        for pile in self.tableau_piles:  # Iterating through the tableau piles
            pile.draw()  # Drawing them

        self.stock_pile.draw()

    def draw(self):
        """Drawing the desk's content (safe to use mid-game)"""
        pass 

    def active_card_search(self):
        # Searching for active card
        self.active_card = next(
        (card for card in self.cards if card.is_active), None
        )
        return bool(self.active_card)

    def change_mouse_pos(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def try_activate_some_card(self):
        for pile in self.tableau_piles:
            pile.iterate_and_activate(self.mouse_x, self.mouse_y)
        if self.stock_pile.is_turned_list_empty():
            self.stock_pile.iterate_and_activate(self.mouse_x, self.mouse_y)

    def try_moving_active_card(self):
        for (
            pile
        ) in self.foundation_piles:  # Checking for click in foundation piles
            if pile.is_clicked(self.mouse_x, self.mouse_y):
                pile.maybe_move(
                    self.active_card
                )  # Move the card if it's possible
                # Reset the active card

                self.active_card.change_piles(CardPileEnum.FOUNDATIONS)
        for (
            pile
        ) in self.tableau_piles:  # Checking for click in Tableau piles...
            if pile.last_card_clicked(
                self.mouse_x, self.mouse_y
            ):  # ...on the last card
                pile.try_move_card(
                    self.active_card
                )  # Try to move the active card on the clicked one.
                self.active_card.change_piles(CardPileEnum.TABLEAU)

        self.active_card.deactivate()
        self.window.refresh()  # Refresh to show the active card

    def check_stockpile(self):
        if self.stock_pile.is_clicked(self.mouse_x, self.mouse_y):
            self.stock_pile.check_card(self.window)