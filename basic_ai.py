# __future__ module is a built-in module in Python that is used to inherit new features that will be available in the new Python versions.
from __future__ import annotations
# From the task 1 which is cards import the class that inside the class which is Card, Rank and Suit. 
from cards import Card, Rank, Suit
# From class player which is used to check how many cards that is valid to play import Player 
from player import Player


# Task 2.1: Basic AI Player
# Create a class called BasicAIPlayer with parameter which is Player that import in the beginning
# The BasicAIPlayer class use to track the attributes such as a player's hand of cards and deciding what card to play on a given trick
class BasicAIPlayer(Player):

    # __init__ is a reserved method
    # Define a method which use to initialise class by setting the passed argument as instance variable
    # super() means that it return the object that represents the parent class
    def __init__(self, name: str):
        super().__init__(name)

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
        - broken_hearts: boolean that indicates the status of broken hearts
        Returns the lowest ranking card from the player's hand that constitutes a valid play
        """

        # Declare the lowest card index as lowest_card_index and initialise the lowest_card_index as none
        lowest_card_index = None

        # Use for loop to find the minimum number of card in player hand
        for card_index in range(len(self.hand)):
            if self.check_valid_play(self.hand[card_index], trick, broken_hearts)[0] == True:   # Check if the card that in the hand is valid
                if lowest_card_index == None:                                                   # First value will be assigned if appropriate and overwrite the value 'None'
                    lowest_card_index = card_index
                elif self.hand[card_index] < self.hand[lowest_card_index]:                      # After the first loop, if the number of the card is lower than the loop before, it will reset the number which is lower than the previous number
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
        for _ in range(3):                      # The reason why use 3 here because the question have already fixed the number of passing card is 3, so we initialise it as 3
            cardlst.append(max(self.hand))      # Append the greatest card that in player hand
            self.hand.remove(max(self.hand))    # Remove the card that append in the previous step

        return cardlst  # Return the value of card that store in the cardlst
