# Birbuh's Console Solitaire

BCS is a light-weight solitaire written fully in python (ncurses library).

To play, just clone the repo or download the zip.
Then go to the folder it's in and launch `python main.py`. 

The one and only requirement is Python interpreter and Linux OS. It doesn't work for Windows rn, sorry.


* CAUTION: If You click too fast, the screen might flash. I'm sorry about this, but I don't have much time before I can post it to my competition, so I'll propably update that after the results will come.


# HOW TO:

## Installing and running

To play Birbuh's Console Solitaire, You need to, as mentioned earlier, clone the repo or download it from zip file.
Also, You need to be on Linux and have Python installed.
No, this program currently doesn't support Windows.
Next, **IN THE CONSOLE** go to the folder you unpacked/cloned it and run `python main.py`

## Playing

You should have the classic solitaire layout in the center. On the left, You should see a timer, a prompt to exit (press Q to do it), and the "click me if You lost" button.

First comes the button.
This button restarts the game and redirects You to the "You lost, didn't ya?" screen. Choose "Play again?" button to play again or "Quit :c" button to quit.

The next is the timer.
You cannot interact with it; the time will be shown at the end of the game, regardless of whether you lose or win.

And, finally, let's go to the game itself.
Left-click a card (with mouse) to activate it.
Once it's activated, You can click other card. If it can move, it will move. 
***BUT***
The cards have to meet the requirements to do it. More in the next part, called *Playing Solitaire (rules etc.)*

So, let's say a bit about the behaviour of the piles:

1. The Tableau.
  This is the easiest: left click on the first one, left click on the second one.
  The cards can move in and out.

2. Foundation Piles.
   This is a little bit more complicated. The cards can move in, can't move out. Make one of the cards active and then left-click the right pile.

3. The Stock Pile.
   This is the last one. Cards can only move out. To show next card, left-click the covered side. If you want to go back, right-click the same side of the pile.

* CAUTION: If the covered side of the Stock Pile is empty and you left-click on it, the cards will reset. However, if the uncovered (turned) side will be empty and You right-click the covered side, nothing will happen 😱
  
## Playing Solitaire (rules etc.):
(this tutorial is fully copied from https://bicyclecards.com/how-to-play/solitaire)

Many Solitaire games can be played on areas smaller than a card table. Others require a larger playing area, and these games are often played on the floor or on a bedspread. Alternatively, in order to play with large layouts on a card table, miniature playing cards are available. These are usually half the size of standard playing cards.

The Pack
Virtually all Solitaire games are played with one or more standard 52-card packs. Standard Solitaire uses one 52-card pack.

Object of the Game
The first objective is to release and play into position certain cards to build up each foundation, in sequence and in suit, from the ace through the king. The ultimate objective is to build the whole pack onto the foundations, and if that can be done, the Solitaire game is won.

Rank of Cards
The rank of cards in Solitaire games is: K (high), Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2, A (low).

The Deal
There are four different types of piles in Solitaire:

The Tableau: Seven piles that make up the main table.

The Foundations: Four piles on which a whole suit or sequence must be built up. In most Solitaire games, the four aces are the bottom card or base of the foundations. The foundation piles are hearts, diamonds, spades, and clubs.

The Stock (or “Hand”) Pile: If the entire pack is not laid out in a tableau at the beginning of a game, the remaining cards form the stock pile from which additional cards are brought into play according to the rules.

The Talon (or “Waste”) Pile: Cards from the stock pile that have no place in the tableau or on foundations are laid face up in the waste pile.

To form the tableau, seven piles need to be created. Starting from left to right, place the first card face up to make the first pile, deal one card face down for the next six piles. Starting again from left to right, place one card face up on the second pile and deal one card face down on piles three through seven. Starting again from left to right, place one card face up on the third pile and deal one card face down on piles four through seven. Continue this pattern until pile seven has one card facing up on top of a pile of six cards facing down.

The remaining cards form the stock (or “hand”) pile and are placed above the tableau.

When starting out, the foundations and waste pile do not have any cards.

The Play
The initial array may be changed by "building" - transferring cards among the face-up cards in the tableau. Certain cards of the tableau can be played at once, while others may not be played until certain blocking cards are removed. For example, of the seven cards facing up in the tableau, if one is a nine and another is a ten, you may transfer the nine to on top of the ten to begin building that pile in sequence. Since you have moved the nine from one of the seven piles, you have now unblocked a face down card; this card can be turned over and now is in play.

As you transfer cards in the tableau and begin building sequences, if you uncover an ace, the ace should be placed in one of the foundation piles. The foundations get built by suit and in sequence from ace to king.

Continue to transfer cards on top of each other in the tableau in sequence. If you can’t move any more face up cards, you can utilize the stock pile by flipping over the first card. This card can be played in the foundations or tableau. If you cannot play the card in the tableau or the foundations piles, move the card to the waste pile and turn over another card in the stock pile.

If a vacancy in the tableau is created by the removal of cards elsewhere it is called a “space”, and it is of major importance in manipulating the tableau. If a space is created, it can only be filled in with a king. Filling a space with a king could potentially unblock one of the face down cards in another pile in the tableau.

Continue to transfer cards in the tableau and bring cards into play from the stock pile until all the cards are built in suit sequences in the foundation piles to win!

* Caution: in the code, there's NO SUCH THING AS WASTE PILE. It's a `turned_card_list` variable in the StockPile class.

# FAQ:

1. When the card is activated?
 - The card is activated when it has kind of light purple internals.

2. Why I can't put my Ace to one of the Foundations Piles?
 - Make sure that You were putting it to the right one - it has to match the symbols! If the problem continues, follow step 4.

3. What if my problem isn't covered here?
 - Message me on Discord (username: birbuh; id: 1058415231820382278) or just report in on GitHub (https://github.com/Birbuh/Birbuhs-Console-Solitaire/issues). 



# Additional information:

- By Franciszek Foltyński for Gigathon Competition 2nd Stage 2025.

- Won't be doing anything till the Gigathon IInd Stage results will come.# Birbuh's Console Solitaire
