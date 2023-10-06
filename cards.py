# __future__ module is a built-in module in Python that is used to inherit new features that will be available in the new Python versions
from __future__ import annotations  
# An enum is a set of symbolic names bound to unique constant values 
from enum import Enum


# Task 1.1 class Rank
# Create a class called Rank with parameter Enum
# The enum in class Rank is used to initialise different number of the range of ranks within a suit
class Rank(Enum):
    Two = 2         # Initialise the variable name and assign (or bound) to a value (others are similar)
    Three = 3       
    Four = 4        
    Five = 5        
    Six = 6         
    Seven = 7       
    Eight = 8       
    Nine = 9       
    Ten = 10        
    Jack = 11       
    Queen = 12      
    King = 13      
    Ace = 14        

    # __lt__() is a magic method which describe the lower than operator
    # This method takes two arguments: self(self object) and other(object class Rank) and return a boolean(true or false)
    def __lt__(self, other: Rank) -> bool:
        return self.value < other.value


# Task 1.2 class Suit
# Create a class called Suit with the parameter Enum
# The Enum in class Suit is used to initialise different suit within a class
class Suit(Enum):
    Clubs = 1       # Initialise the variable name and assign (or bound) to a value (others are similar)
    Diamonds = 2    
    Spades = 3     
    Hearts = 4     

    # __lt__() is a magic method which describe the lower than operator
    # This method takes two arguments: self(self object) and other(object class Suit) and return a boolean(true or false)
    def __lt__(self, other: Suit) -> bool:
        return self.value < other.value


# Task 1.3 class Card
# Define a class called Card to represent an object represents a combination of class "Rank" and class "Suit"
class Card:
    """
    Card class represents an object with the combination of both class "Rank" and class "Suit"
    """
    pretty_print = False

    # Define a method which use to initialise class by setting the passed arguments as instance variables
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    # __repr__ is a magic method that return the string representation (here is string) when we called an object
    # Define a method which use to represent a string when we called the object card
    def __repr__(self) -> str:
        return self.__str__()

    # __str__ is a magic method that return a string representation when we print the object
    # Define a method which use to represent the object when we print the object (or called the string of object)
    # Return the string type of the name of the card. i.e.: two of clubs/queen of spade
    def __str__(self) -> str:
        if self.pretty_print:
            if self.rank < Rank.Jack:       # Check the if the rank is more than Jack, then take the first char of the string
                rank = self.rank.value
            else:
                rank = self.rank.name[0]
            
            # Check the suit of the card and assign their particular symbol representation of the suit
            if self.suit == Suit.Clubs:     
                suit = '♣'
            elif self.suit == Suit.Diamonds:
                suit = '♦'
            elif self.suit == Suit.Spades:
                suit = '♠'
            else:
                suit = '♥'

            # Divided into two part, one is 10 (because it have two digit), another one is except 10(only have one digit)
            # Return the card_art of the card
            if self.rank is Rank.Ten:
                str = f'┌─────┐\n│{rank}   │\n│  {suit}  │\n│   {rank}│\n└─────┘'
            else:
                str = f'┌─────┐\n│{rank}    │\n│  {suit}  │\n│    {rank}│\n└─────┘'
            return str

        else:
            return f'{self.rank.name} of {self.suit.name}'

    # __eq__ is a magic method that used to define the equality logic for the comparing two object using equal operator
    # Define a method which takes two arguments self(object card) and other(object card) and return a boolean(true or false)
    # Return true if both self suit and rank is same as other suit and rank
    def __eq__(self, other: Card) -> bool:
        return (self.suit == other.suit) and (self.rank == other.rank) 

    # __lt__() is a magic method which describe the lower than operator
    # Define a method which use to compare suit first then rank to determine if a card is lower than others
    def __lt__(self, other: Card) -> bool:
        if self.suit != other.suit:                                 # If cards suit not the same, compare suit
            return self.suit < other.suit                           
        else:                                                       # Otherwise, compares rank
            return self.rank < other.rank                       


if __name__ == "__main__":
    # you can make some local tests here.
    card1 = Card(Rank.Two, Suit.Clubs)
    Card.pretty_print = True
    print(card1)
    # card2 = Card(Rank.Two, Suit.Clubs)
    # print(card1 > card2)
