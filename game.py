import curses
import logging
import time

from desk import Desk
from buttons import Button


logger = logging.getLogger()

class Game:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr

    def start_game(self):
        """Loading screen and stuff"""
        # Setup
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(True)  # Make getch non-blocking

        # Clearing the window
        self.stdscr.clear()

        # Drawing the button
        start_button = Button(10, 10, "Start the game!", self.stdscr)
        start_button.draw()

        # Instructions
        self.stdscr.addstr(5, 10, "Click the button to start the game")
        self.stdscr.refresh()

        while True:
            try:
                key = self.stdscr.getch()
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

        self.stdscr.refresh()

    def game(self):
        """Main game function"""
        self.stdscr.clear()
        # Make sure that nodelay mode is kept from start_game
        self.stdscr.nodelay(True)
        curses.start_color()

        # Create and draw restart button
        restart_button = Button(10, 10, "Restart the game", self.stdscr)
        restart_button.draw()

        desk = Desk(self.stdscr)
        desk.initialize()
        desk.init_draw()

        # Game instructions
        self.stdscr.addstr(2, 10, "Solitaire Game")
        self.stdscr.addstr(3, 10, "(double) Press 'q' to quit")

        # Start time.time()
        start_time = time.time()
        # Game loop
        running = True

        while running:  # EVENT LOOP
            # Show time
            elapsed_mins = (time.time() - start_time) / 60
            self.stdscr.addstr(
                4,
                10,
                f"your time: {int(elapsed_mins)} minutes {int((elapsed_mins % 1) * 60)} seconds",
            )

            try:
                key = self.stdscr.getch()  # Checking for input
                if key == ord("q"):  # q for quit
                    running = False
                elif key == curses.KEY_MOUSE:  # mouse click
                    try:
                        _, mouse_x, mouse_y, _, _ = curses.getmouse()  # get mouse pos
                        if restart_button.is_clicked(mouse_x, mouse_y):
                            # Restart the game
                            self.stdscr.clear()
                            return self.game()
                        desk.on_click(mouse_x, mouse_y)
                        self.stdscr.refresh()
                    except Exception as e:
                        logger.error(e, exc_info=True)
            except Exception as e:
                logger.error(e, exc_info=True)

            self.stdscr.refresh()
            time.sleep(0.05)  # Prevent CPU hogging