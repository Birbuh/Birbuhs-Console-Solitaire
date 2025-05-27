import curses
import random
import itertools
import logging

from piles import TableauPile, FoundationPile, StockPile
from card import Card, CardColorEnum, CardNumberEnum, CardPileEnum


logger = logging.getLogger()

class Desk:
    """Class that's drawing the whole Tableau on the window.
    
    Attributes:
        self.foundation_piles: Foundation piles list
        self.tableau_piles: Tableau piles list
        self.stock_pile: Stock pile object
        self.active_card: Card object that is active (not more than one)
        self.window: The window in which everything is drawn.
        self.mouse_x: mouse x coor on click
        self.mouse_y: mouse y coor on click

    """

    foundation_piles: list[FoundationPile] = []
    tableau_piles: list[TableauPile] = []
    active_card: Card | None = None

    def __init__(self, window: curses.window):
        self.window = window

    def initialize(self):
        """Initializing all of the desk's content."""

        # Initialize all cards
        cards = [
            Card(color, num, self.window)
            for color, num in itertools.product(CardColorEnum, CardNumberEnum)
        ]
        random.shuffle(cards)  # Shuffling the cards

        # Making these cards group for Tableau and Stock piles.
        tableau_cards = cards[:28]
        stock_cards = cards[28:]

        # Initialize all classes
        # 7 TableauPile instances
        self.initialize_tableau(tableau_cards)

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
        self.stock_pile = StockPile(stock_cards, self.window)

    def initialize_tableau(self, cards: list[Card]):
        """Initializing Tableau
        
        :param cards: The card list from which the Tableau is initialized
        """
        for i in range(7, 0, -1):
            lasted_cards = cards[:i]
            cards = cards[i:]
            current_pile = TableauPile(lasted_cards, 28 + 12 * i, self.window) 
            self.tableau_piles.append(current_pile)

    def init_draw(self):
        """Drawing the desk's content (for the first time only)"""
        # Drawing the Foundation piles
        for pile in self.foundation_piles:
            pile.draw()

        # Drawing the Tableau piles
        for pile in self.tableau_piles: 
            pile.init_draw()  

        # Drawing the Stock pile
        self.stock_pile.init_draw()

    def draw(self):
        for pile in self.foundation_piles:
            pile.draw()

        for pile in self.tableau_piles:
            pile.draw()

        self.stock_pile.draw()

    def on_click(self, mouse_x, mouse_y) -> bool:
        """Contains (and does) all of the things that are needed on click.
        
        :param mouse_x: The new x coor of the mouse
        :param mouse_y: The new y coor of the mouse
        """

        # Changing mouse position
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        if self.try_moving_active_card():
            return True
        if self.try_deactivate_active_card():
            return False
        if self.try_activate_some_card():
            return False
        return self.check_stockpile()
    
    def try_activate_some_card(self) -> bool:
        """Tries activating a card and returning bool (True is activated, False if not)."""
        if self.active_card:
            return False
        for pile in self.tableau_piles:
            ac = pile.iterate_and_activate(self.mouse_x, self.mouse_y)
            if ac:
                self.active_card = ac
                self.active_card_pile = pile
                return True
        ac = self.stock_pile.try_activate(self.mouse_x, self.mouse_y)
        if ac:
            self.active_card = ac
            self.active_card_pile = self.stock_pile
            return True
        return False

    def try_moving_active_card(self) -> bool:
        """Tries to move the active card and returning bool (True is moved, False if not)."""
        if not self.active_card:
            return False
        
        for pile in self.foundation_piles:  # Checking for click in foundation piles
            if pile.is_clicked(self.mouse_x, self.mouse_y):
                if pile.can_move(self.active_card):  # Move the card if it's possible
                    self.active_card_pile.move_to()
                    pile.move_from_other_pile(self.active_card)
                    self.active_card.change_piles(CardPileEnum.FOUNDATIONS)
                    self.try_deactivate_active_card()
                    return True
                
        for pile in self.tableau_piles:  # Checking for click in Tableau piles...
            if pile.pile_or_card_clicked(
                self.mouse_x, self.mouse_y
            ):  # ...on the last card
                if pile.can_move_card(
                    self.active_card
                ):  # Try to move the active card(s) on the clicked one.
                    if self.active_card_pile.is_last_card(self.active_card) or self.active_card.return_pile() == 'STOCK':
                        self.active_card_pile.move_to()
                        pile.move_from_other_pile(self.active_card)
                        self.active_card.change_piles(CardPileEnum.TABLEAU)
                    else:
                        cards = self.active_card_pile.return_next_cards(self.active_card)
                        for count, card in enumerate(cards):    
                            count = len(cards) - (count + 1)
                            if count == 0:  # First card (the one that was clicked)
                                self.active_card_pile.move_to()
                                pile.move_from_other_pile(card)
                            else:
                                self.active_card_pile.move_to()
                                pile.move_from_other_pile(card)
                        self.active_card_pile.reactivate_last_card()
                    self.try_deactivate_active_card()
                    # if pile.is_empty():         # drawing the empty pile if it's empty.
                    #     pile.draw_empty()
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
            return self.stock_pile.check_card()
        return False