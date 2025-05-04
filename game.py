import curses
import logging
import time
import itertools
import random

from card import Card, CardColorEnum, CardNumberEnum
from buttons import Button
from piles import FoundationPile, Tableau, StockPile  # , TableauPile

logger = logging.getLogger()


def start_game(stdscr: curses.window):
    """Loading screen and stuff"""
    # Setup
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getch non-blocking

    # Clearing the window
    stdscr.clear()

    # Drawing the button
    start_button = Button(10, 10, "Start the game!", stdscr)
    start_button.draw()

    # Instructions
    stdscr.addstr(5, 10, "Click the button to start the game")
    stdscr.refresh()

    while True:
        try:
            key = stdscr.getch()
            if key == curses.KEY_MOUSE:
                try:
                    _, mouse_x, mouse_y, _, _ = curses.getmouse()
                    if start_button.is_clicked(mouse_x, mouse_y):
                        break
                except curses.error:
                    # Sometimes getmouse can fail
                    pass
            elif key == ord("q"):  # Allow quitting with 'q'
                raise KeyboardInterrupt
        except curses.error:
            # No input available
            pass

        time.sleep(0.1)  # Prevent CPU hogging

    stdscr.clear()
    stdscr.refresh()


def game(stdscr: curses.window):
    """Main game function"""
    # Make sure that nodelay mode is kept from start_game
    stdscr.nodelay(True)
    curses.start_color()

    # Create and draw restart button
    restart_button = Button(10, 10, "Restart the game", stdscr)
    restart_button.draw()

    # Create and shuffle cards
    cards = [
        Card(color, num, stdscr)
        for color, num in itertools.product(CardColorEnum, CardNumberEnum)
    ]
    random.shuffle(cards)

    # Display cards
    lasted_cards = Tableau(cards).draw()
        
    # Initialize the Foundation Piles
    foundation_hearts = FoundationPile(stdscr, CardColorEnum.HEARTS)
    foundation_diamonds = FoundationPile(stdscr, CardColorEnum.DIAMONDS)
    foundation_clubs = FoundationPile(stdscr, CardColorEnum.CLUBS)
    foundation_spades = FoundationPile(stdscr, CardColorEnum.SPADES)
    # Drawing them
    foundation_hearts.draw()
    foundation_diamonds.draw()
    foundation_clubs.draw()
    foundation_spades.draw()
    # Grouping them
    foundation_piles = [
        foundation_hearts,
        foundation_diamonds,
        foundation_clubs,
        foundation_spades,
    ]

    # Initializing and drawing Stock Pile
    stock_pile = StockPile(lasted_cards)
    stock_pile.draw()

    # Game instructions
    stdscr.addstr(2, 10, "Solitaire Game")
    stdscr.addstr(3, 10, "(double) Press 'q' to quit")

    # Start time.time() here for more accurate time on potatoes
    start_time = time.time()
    # Game loop
    running = True
    while running:
        elapsed_mins = (time.time() - start_time) / 60
        stdscr.addstr(
            4,
            10,
            f"your time: {int(elapsed_mins)} minutes {int((elapsed_mins % 1) * 60)} seconds",
        )

        try:
            active_card: Card | None = next(
                (card for card in cards if card.is_active), None
            )
            logger.debug(active_card)
            key = stdscr.getch()
            if key == ord("q"):
                running = False
            elif key == curses.KEY_MOUSE:
                try:
                    _, mouse_x, mouse_y, _, _ = curses.getmouse()
                    if restart_button.is_clicked(mouse_x, mouse_y):
                        # Restart the game
                        stdscr.clear()
                        return game(stdscr)
                    if active_card is None:
                        for card in cards:
                            if (
                                card
                                in (  # ignore the card if it's already in the Foundations
                                    foundation_clubs.card_list
                                    or foundation_diamonds.card_list
                                    or foundation_spades.card_list
                                    or foundation_hearts.card_list
                                )
                            ):
                                continue
                            if card.is_clicked(mouse_x, mouse_y):
                                # Allow any card to be clicked, but it must be turned up
                                if card.turned:
                                    logger.debug("Card clicked: %s", card.get_symbol())
                                    # Make this card active
                                    card.activate()
                                    stdscr.refresh()  # Refresh to show the active card
                    elif active_card is not None:
                        for other_card in cards:
                            # Ignoring double clicks etc.
                            if other_card == active_card:
                                continue
                            # Checking for click in Tableau piles
                            if other_card.is_clicked(mouse_x, mouse_y):
                                other_card.may_move(
                                    active_card
                                )  # Move the card if it's possible
                                # Reset the active card
                                active_card.deactivate()
                            # Checking for click in foundation piles
                            for pile in foundation_piles:
                                if pile.is_clicked(mouse_x, mouse_y):
                                    pile.maybe_move(
                                        active_card
                                    )  # Move the card if it's possible
                                    # Reset the active card
                                    active_card.deactivate()
                except Exception as e:
                    logger.error(e, exc_info=True)
        except Exception as e:
            logger.error(e, exc_info=True)

        stdscr.refresh()
        time.sleep(0.1)  # Prevent CPU hogging