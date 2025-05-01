import curses

# import asyncio
import logging

# import time
import sys

from game import start_game, game


##################################################################
# logging setup
logging.basicConfig(
    filename="solitare.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname}: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)
##################################################################

logger = logging.getLogger()


def main(stdscr: curses.window):
    """Function running the program."""
    # Setup
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    # Start the game flow
    start_game(stdscr)
    game(stdscr)

    # Clean exit
    stdscr.clear()
    stdscr.addstr(10, 10, "Thanks for playing! Press any key to exit.")
    stdscr.nodelay(False)  # Switch back to blocking mode for final input
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)
