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
        self.mouse_x: mouse x coord on click
        self.mouse_y: mouse y coord on click

    """

    def __init__(self, window: curses.window):
        self.window = window
        self.foundation_piles = []
        self.tableau_piles = []
        self.active_card = []

    def initialize(self):
        """Initializing all of the desk's content."""

        # Initialize all cards
        self.cards = [
            Card(color, num, self.window)
            for color, num in itertools.product(CardColorEnum, CardNumberEnum)
        ]
        random.shuffle(self.cards)  # Shuffling the cards

        # Making these cards group for Tableau and Stock piles.
        self.tableau_cards = self.cards[:28]
        self.stock_cards = self.cards[28:]
        logger.debug(
            f"Cards in Tableau: {len(self.tableau_cards)}, Cards in StockPile: {len(self.stock_cards)}"
        )

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
        self.stock_pile = StockPile(self.stock_cards, self.window)

    def initialize_tableau(self, cards: list[Card]):
        """Initializing Tableau

        :param cards: The card list from which the Tableau is initialized
        """
        for i in range(7, 0, -1):
            lasted_cards = cards[:i]
            logger.debug("tableau_cards changed")
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

    def on_click(self, mouse_x, mouse_y, event) -> bool:
        """Contains (and does) all of the things that are needed on click.

        :param mouse_x: The new x coord of the mouse
        :param mouse_y: The new y coord of the mouse
        """
        if (
            len(self.stock_cards)
            + len(self.tableau_cards)
            + len(self.stock_pile.turned_card_list)
            < 52
        ):
            logger.error(
                f"""Hm, I think some card went missing...
                   stock cards: {len(self.stock_cards)}; 
                   stock turned cards: {len(self.stock_pile.turned_card_list)} 
                   tableau cards: {len(self.tableau_cards)};"""
            )
        # Changing mouse position
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        if self.try_moving_active_card():
            return True
        if self.try_deactivate_active_card():
            return False
        if self.try_activate_some_card():
            return False
        return self.check_stockpile(event)

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
            if (
                self.active_card_pile.is_last_card(self.active_card)
                and self.active_card.return_pile() == "TABLEAU"
            ) or self.active_card.return_pile() == "STOCK":
                if pile.is_clicked(self.mouse_x, self.mouse_y):
                    if pile.can_move(
                        self.active_card
                    ):  # Move the card if it's possible
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
                    if (
                        self.active_card_pile.is_last_card(self.active_card)
                        or self.active_card.return_pile() == "STOCK"
                    ):
                        self.active_card_pile.move_to()
                        pile.move_from_other_pile(self.active_card)
                        self.active_card.change_piles(CardPileEnum.TABLEAU)
                    else:
                        cards = self.active_card_pile.return_next_cards(
                            self.active_card
                        )
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

    def check_stockpile(self, event):
        if self.stock_pile.is_clicked(self.mouse_x, self.mouse_y):
            if (event & curses.BUTTON1_CLICKED != 0) or (
                event & curses.BUTTON1_PRESSED
            ) != 0:
                return self.stock_pile.check_card()
            elif (event & curses.BUTTON3_CLICKED != 0) or (
                event & curses.BUTTON3_PRESSED
            ):
                return self.stock_pile.uncheck_card()
        return False

    def is_game_won(self):
        return (
            all(pile.is_empty() for pile in self.tableau_piles)
            and self.stock_pile.is_empty()
        )
