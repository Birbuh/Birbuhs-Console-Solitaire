import curses
import sys
import logging

from game import start_game


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


def main(window: curses.window):
    """Function running the program."""
    # Setup
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    curses.curs_set(0)  # Hide cursor
    window.clear()

    # Start the game flow
    start_game(window)

    # Clean exit
    window.clear()
    window.addstr(10, 10, "Thanks for playing! Press any key to exit.")
    window.nodelay(False)  # Switch back to blocking mode for final input
    window.refresh()
    window.getch()


if __name__ == "__main__":  # The program's called here
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(0)  # exit if ctrl + c
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(
            1
        )  # exit if an error occurs in the part in which catching exceptions aren't implemented.
