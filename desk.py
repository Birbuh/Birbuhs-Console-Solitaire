import curses
import random
import itertools
import logging

from piles import TableauPile, FoundationPile, StockPile
from card import Card, CardColorEnum, CardNumberEnum, CardPileEnum


logger = logging.getLogger()

class Desk:
    """Class that's drawing the whole Tableau on the window."""

    cards: list[Card] = []
    foundation_piles: list[FoundationPile] = []
    tableau_piles: list[TableauPile] = []
    active_card: Card | None = None

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

    def change_mouse_pos(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def on_click(self, newx, newy):
        self.change_mouse_pos(newx, newy)
        if self.try_moving_active_card():
            return
        if self.try_deactivate_active_card():
            return
        if self.try_activate_some_card():
            return
        self.check_stockpile()
    
    def try_activate_some_card(self) -> bool:
        if self.active_card:
            return False
        for pile in self.tableau_piles:
            ac = pile.iterate_and_activate(self.mouse_x, self.mouse_y)
            if ac:
                self.active_card = ac
                self.active_card_pile = pile
                return True
        if self.stock_pile.is_turned_list_empty():
            ac = self.stock_pile.try_activate(self.mouse_x, self.mouse_y)
            if ac:
                self.active_card = ac
                self.active_card_pile = self.stock_pile
                return True
        return False

    def try_moving_active_card(self) -> bool:
        if not self.active_card:
            return False
        
        for pile in self.foundation_piles:  # Checking for click in foundation piles
            if pile.is_clicked(self.mouse_x, self.mouse_y):
                if pile.can_move(self.active_card):  # Move the card if it's possible
                    self.active_card_pile.move_to()
                    pile.move_from_other_pile(self.active_card, 0, self.active_card_pile)
                    self.active_card.change_piles(CardPileEnum.FOUNDATIONS)
                    if self.active_card.pile == CardPileEnum.STOCK:
                        self.stock_pile.draw_last_card()
                    self.try_deactivate_active_card()
                    return True
                
        for pile in self.tableau_piles:  # Checking for click in Tableau piles...
            if pile.last_card_clicked(
                self.mouse_x, self.mouse_y
            ):  # ...on the last card
                if pile.can_move_card(
                    self.active_card
                ):  # Try to move the active card on the clicked one.
                    self.active_card_pile.move_to()
                    pile.move_from_other_pile(self.active_card, pile.last_card_relative_y() + 3, self.active_card_pile)
                    self.active_card.change_piles(CardPileEnum.TABLEAU)
                    if self.active_card.pile == CardPileEnum.STOCK:
                        self.stock_pile.draw_last_card()
                    self.try_deactivate_active_card()
                    return True
        return False
        # self.window.refresh()  # Refresh to show the active card

    def try_deactivate_active_card(self) -> bool:
        if self.active_card:
            self.active_card.deactivate()
            self.active_card = None
            return True
        return False

    def check_stockpile(self):
        if self.stock_pile.is_clicked(self.mouse_x, self.mouse_y):
            self.stock_pile.check_card(self.window)