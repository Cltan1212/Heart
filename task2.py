# __future__ module is a built-in module in Python that is used to inherit new features that will be available in the new Python versions.
from __future__ import annotations
# From the task 1 which is cards import the class that inside the class which is Card, Rank and Suit. 
from cards import Card, Rank, Suit


# Task 2.1: Basic AI Player
# Create a class called BasicAIPlayer with parameter which is Player that import in the beginning
# The BasicAIPlayer class is use to track the attributes such as a player's hand of cards and deciding what card to play on a given trick
class BasicAIPlayer:

    # __init__ is a reserved method
    # Define a method which use to initialise class by setting the passed argument as instance variable
    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.total_score = 0
        self.round_score = 0

    # __str__ is a magic method that return a string representation when we print the object
    # Define a method which use to return the string type name 
    def __str__(self) -> str:
        return self.name

    # __repr__ is a magic method that return the string representation (here is string) when we called an object
    # Define a method which use to see the same string of your card
    def __repr__(self) -> str:
        return self.__str__()

    # Task 2.3 Playing Cards 
    # Define a method which called play_card with the parameter (trick and broken_hearts)
    # This method is used to determine a card to play on a given trick 
    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:

        """
        Determine a card to play on a given trick.
        Arguments:
        - trick: a list of Card
        - broken_hearts: boolean that indicate the status of broken hearts
        Returns the lowest ranking card from the player's hand that constitutes a valid play
        """

        # Declare the lowest card index as lowest_card_index and initialise the lowest_card_index as none
        lowest_card_index = None 

        # Use for loop to find the mininum number of card in player hand
        for card_index in range(len(self.hand)):
            if self.check_valid_play(self.hand[card_index], trick, broken_hearts)[0] == True:    # Check if the card that in the hand is valid 
                if lowest_card_index == None:                                                    # First value will be assigned if appropriate and ovewrites the value 'None'
                    lowest_card_index = card_index
                elif self.hand[card_index] < self.hand[lowest_card_index]:                       # After the first loop, if the number of the card is lower than the loop before, it will reset the number which is lower than the previous number
                    lowest_card_index = card_index
        # The pop() method here is to return the removed card and remove the card in the player hand
        return self.hand.pop(lowest_card_index)

    # Task 2.3 Passing card
    # Define a method which called pass_card() with a parameter self (a reference to the current instance of the class)
    # Pass_cards() to return their chosen 3 cards to pass off at the start of each round
    def pass_cards(self) -> list:
        """
        Determine three cards to pass on a given round.
        Argument: None
        Returns a list of three cards from the player's hands to pass off and
        remove them from self.hand before returning. 
        """
        
        # Declare the list of 3 cards in list form as cardlst and initialise it as a blank list
        cardlst = []

        # We use for loop instead of while loop (given the exact number of iteration, already known.)
        for _ in range(3):                          # The reason why use 3 here is because the quesiton have already fixed the number of passing card is 3, so we initialise it as 3
            cardlst.append(max(self.hand))          # Append the greatest card that in player hand
            self.hand.remove(max(self.hand))        # Remove the card that append in the previous step

        return cardlst                              # Return the value of card that store in the cardlst

    # Define a method called check_valid_play with the parameter (card, trick and broken hearts)
    # This method is used to check whether the card can output or not 
    def check_valid_play(self, card: Card, trick, broken_hearts: bool) -> tuple:

        """
        Validate the card that player choose to play.
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
            for elm in self.hand:                           # Use for loop to find load each card in player hand
                if elm.suit == Suit.Hearts:                 # Updated num_of_hearts by incrementing 1 if the card suit is hearts
                    num_of_hearts += 1

            # Check if the card is not Two of Clubs and num_of_2_spades > 0(means that card Two of Clubs still in player hand, it will output the sentence which is present next line)
            if (card != (Card(Rank.Two, Suit.Clubs))) and (Card(Rank.Two, Suit.Clubs) in self.hand):
                return False, 'Player has Two of Clubs and has not been played'
            
            # Check the if the broken_hearts is False, the trick cannot output the hearts cards 
            elif (broken_hearts is False) and (card.suit == Suit.Hearts) and (num_of_hearts < len(self.hand)):
                return False, 'Player attempted playing Hearts while leading the trick although having other options'
       
        # If player not leading trick
        else:  
            num_of_suit_card = 0                                        # Number of card with same suit as leading card
            
            # Use a for loop to check whether the suit is the same or not, they must follow the suit if applicable
            for elm in self.hand:
                if elm.suit.name == trick[0].suit.name:                 # Updates number of card in the same suit in player's 
                    num_of_suit_card += 1

            # If the first trick is Two of Clubs, go into this block        
            if trick[0] == Card(Rank.Two, Suit.Clubs):
                if card.suit == Suit.Hearts:                            # If the card suit is hearts
                    return False, 'First trick of the round, Hearts cannot be played!'

                elif card == Card(Rank.Queen, Suit.Spades):             # If the card is Queen of Spades
                    return False, 'First trick of the round, Queen of Spades cannot be played!'

            # If player's card suit is not same as the trick suit but player still have the card in which the suit is same as the trick suit        
            if (card.suit != trick[0].suit) and (num_of_suit_card > 0):
                return False, 'Player still has cards from the suit of the current trick!'

        # Methods of elimination leads to True at the end        
        return True, None  


if __name__ == "__main__":
    # Test your function here
    player = BasicAIPlayer("Test Player 1")
    player.hand = [Card(Rank.Four, Suit.Clubs), Card(Rank.Ace, Suit.Hearts), Card(Rank.King, Suit.Spades),
                   Card(Rank.Ten, Suit.Spades), Card(Rank.Ace, Suit.Clubs)]

    print(player.pass_cards())
