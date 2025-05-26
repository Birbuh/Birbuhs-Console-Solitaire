# Birbuh's Console Solitaire

BCS is a light-weight solitaire written fully in python (ncurses library).

* Caution: it works ONLY for Linux by now.

# HOW TO PLAY:
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
 - The card is activated when it has red internals.

2. Why I can't put my Ace to one of the Foundations Piles?
 - Make sure that You were putting it to the right one - it has to match the symbols! If the problem continues, follow step 4.

3. What to do when the card isn't fully drawn?
 - That is an issue I had while developing the program; there's one simple solution to that problem: activate and deactivate the card. That should update the card and draw it once again.

4. What if my problem isn't covered here?
 - Message me on Discord (username: birbuh; id: 1058415231820382278) or just report in on GitHub (https://github.com/Birbuh/Birbuhs-Console-Solitaire/issues). 

