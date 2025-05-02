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
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)

    # Create and draw restart button
    restart_button = Button(10, 10, "Restart the game", stdscr)
    restart_button.draw()

    # Create and shuffle cards
    cards = [
        Card(color, num, stdscr)
        for color, num in itertools.product(CardColorEnum, CardNumberEnum)
    ]
    random.shuffle(cards)
    logger.debug(cards)

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
                    for card in cards:
                        if card in (
                            foundation_clubs.card_list
                            or foundation_diamonds.card_list
                            or foundation_spades.card_list
                            or foundation_hearts.card_list
                        ):
                            continue
                        elif card.is_clicked(mouse_x, mouse_y):
                            logger.debug("EROEFEGVBDEGVIOEWGVEGVJEDGFUSDGIVW")
                            card.make_active(2)
                        if card.is_active:
                            for other_card in cards:
                                # Get mouse pos again
                                _, mouse_x, mouse_y, _, _ = curses.getmouse()
                                if other_card == card:
                                    continue

                                if other_card.is_clicked(mouse_x, mouse_y):
                                    other_card.may_move(card)
                except curses.error:
                    pass
        except curses.error:
            # No input available
            pass

        stdscr.refresh()
        time.sleep(0.1)  # Prevent CPU hogging
