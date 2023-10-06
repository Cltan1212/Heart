# __future__ module is a built-in module in Python that is used to inherit new features that will be available in the new Python versions.
from __future__ import annotations
# From the task 1 which is cards import the class that inside the class which is Card, Rank and Suit.
from cards import Card, Rank, Suit


# Task 2.2 Check Valid Player
# Create a class called Player and this player is used to check the valid played card
class Player:
    """
    Player class to be the base object inherited by all player types.
    """

    # Define a method which use to initailise the class by setting the passed arguments as instance variables
    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.total_score = 0
        self.round_score = 0

    # Define a method which use to indicate that the operation is not implemented with respect to the other type
    def __str__(self) -> None:
        raise NotImplementedError

    def __repr__(self) -> None:
        return self.__str__()

    # Define a method called check_valid_play with the parameter (card, trick and broken hearts)
    # This method is used to check whether the card can output or not
    def check_valid_play(self, card: Card, trick, broken_hearts: bool) -> tuple:

        """
        Validate the card that player chooses to play.
        Arguments:
        - card: a card from the player's hand to validate play against
        - trick: a list of cards played in the trick so far, in order of play
        - broken hearts: boolean to represent if hearts have been broken yet
        Return a boolean type to represents a valid play and a string for the error message associated with the invalid play.
        """

        # If player is leading the trick
        if len(trick) == 0:
            num_of_hearts = 0  # To tabulate number of the hearts that in the player's hand

            # Count num of Hearts and Two of Clubs for later use.
            for elm in self.hand:               # Use for loop to find load each card in player hand
                if elm.suit == Suit.Hearts:     # Updated num_of_hearts by incrementing 1 if the card suit is hearts
                    num_of_hearts += 1

            # Check if the card is not Two of Clubs and num_of_2_spades > 0(means that card Two of Clubs still in player hand, it will output the sentence which is present next line)
            if (card != (Card(Rank.Two, Suit.Clubs))) and (Card(Rank.Two, Suit.Clubs) in self.hand):
                return False, 'Player has Two of Clubs and has not been played'

            # Check the if the broken_hearts is False, the trick cannot output the hearts cards
            elif (broken_hearts is False) and (card.suit == Suit.Hearts) and (num_of_hearts < len(self.hand)):
                return False, 'Player attempted playing Hearts while leading the trick although having other options'

        # If player not leading trick
        else:
            num_of_suit_card = 0  # Number of card with same suit as leading card

            # Use a for loop to check whether the suit is the same or not, they must follow the suit if applicable
            for elm in self.hand:
                if elm.suit.name == trick[0].suit.name:  # Updates number of card in the same suit in player's
                    num_of_suit_card += 1

            # If the first trick is Two of Clubs, go into this block
            if trick[0] == Card(Rank.Two, Suit.Clubs):
                if card.suit == Suit.Hearts:  # If the card suit is hearts
                    return False, 'First trick of the round, Hearts cannot be played!'

                elif card == Card(Rank.Queen, Suit.Spades):  # If the card is Queen of Spades
                    return False, 'First trick of the round, Queen of Spades cannot be played!'

            # If player's card suit is not same as the trick suit but player still have the card in which the suit is same as the trick suit
            if (card.suit != trick[0].suit) and (num_of_suit_card > 0):
                return False, 'Player still has cards from the suit of the current trick!'

        # Methods of elimination leads to True at the end
        return True, None

