import curses
# import asyncio
import logging
import time 

from game import start_game


##################################################################
# logging setup
logging.basicConfig(filename="solitare.log", 
                    encoding='utf-8', 
                    filemode='a', 
                    format="{asctime} - {levelname}: {message}", 
                    style="{", 
                    datefmt="%Y-%m-%d %H:%M",
                    level=logging.DEBUG
                    )
##################################################################


def main():
    """Function running the program."""
    stdscr = curses.initscr() # Initializing ncurses; window is now under ncurses supervision.
    curses.noecho() # Making no echo from keypresses
    curses.nocbreak() # React to keys instantly (without Enter)
    stdscr.keypad(True) # Enabling special keys

    try:
        start_game(stdscr)
        time.sleep(10 + 1/3) # only for some time to prevent the program from ending immediately
    finally:
        # Restoring the terminal to the original state
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    main()