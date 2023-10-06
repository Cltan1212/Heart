# __future__ module is a built-in module in Python that is used to inherit new features that will be available in the new Python versions.
from __future__ import annotations
# From the task 1 which is cards import the class that inside the class which is Card, Rank and Suit.
from cards import Card, Rank, Suit
# From class player which is used to check how many cards that is valid to play import Player
from player import Player
# Random library is imported, which helps load the random module, as it provides a number of random number generation-related functions.
import random


# Create a class HumanPlayer that inherits the base player and asks the user to input a name when initialising itself
class HumanPlayer(Player):
    Card.pretty_print = True

    # __init__ is a reserved method
    # Define a method which use to initialise class by setting the passed argument as instance variable
    # Super() means that it return the object that represents the parent class
    def __init__(self):
        self.name = input('Please enter player name: ')  # Give player to insert their name
        super().__init__(self.name)

    # __str__ is a magic method that returns a string representation when we print the object
    # Define a method which use to return the string type name
    def __str__(self) -> str:
        return self.name

    # __repr__ is a magic method that return the string representation (here is string) when we called an object
    # Overwritten to return a readable representation of object when printing a list of card objects.
    def __repr__(self) -> str:
        return self.__str__()

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:

        """
        Determine a card to play on a given trick.
        Arguments:
        - trick: a list of Card
        - broken_hearts: boolean that indicate the status of broken hearts
        Return the lowest ranking card from the player's hand that constitutes a valid play
        """

        print("Your current hand:")
        self.print_hand()  # Called print_hand method to show player's hand

        # will keep prompting user until proper integer input is read for card index, then it breaks from the loop
        while True:
            card_index = input(f'Select a card to play (0-{len(self.hand) - 1}):')

            # The try and except block are used to handle the exceptions
            # The assert statement is used to check whether the conditions are compatible with the required of the method
            try:
                assert len(card_index) > 0, 'Please try again.'  # error if user input empty

                # checks through the characters of the string, if its integer 0-9.
                for char in card_index:
                    assert char.isdecimal(), 'Please enter valid integer to represent card number'  # error if invalid character

                # checks if entered integer is within range
                card_index = int(card_index)
                assert 0 <= card_index <= (len(self.hand) - 1), 'Please enter a number in range'  # error if not in range

                # check if card is valid
                assert self.check_valid_play(self.hand[card_index], trick, broken_hearts)[0], self.check_valid_play(self.hand[card_index], trick, broken_hearts)[1]  # error if not valid

                # Stop the while loop by using break
                break

            # error message will be printed and loop reiterates
            except Exception as e:
                print(e)

        return self.hand.pop(card_index)

    # Create a method which use to pass the 3 of the hand's card to appropriate corresponding player
    def pass_cards(self, passing_to):

        """
        Determine three cards to pass on a given round.
        Argument:
        - passing_to : the player will be passing to
        Return a list of three cards from the player's hands to pass off and
        remove them from self.hand before returning.
        """

        cards = []  # Card list for player to pass
        print("Your current hand:")
        self.print_hand()

        # Check player input numbers
        # will keep prompting user until proper integer input is read for target score, then it breaks from the loop
        while True:
            rand_card_num = []

            # Random number from player hand index (extra stuff)
            for num in random.sample(range(len(self.hand)), 3):
                rand_card_num.append(str(num))

            # Input from user and validate the numbers
            card_index_str = input(f'Select three cards to pass off to {passing_to} (0-{len(self.hand) - 1}) (eg. {",".join(rand_card_num)}): ')
            cardlst = card_index_str.split(',')

            # The try and except block are used to handle the exception
            # The assert statement raises an error when the statement is false, with appropriate error message attached
            try:
                assert len(card_index_str) > 0, 'Please try again.'   # error if user input empty

                # check if the user input three characters
                assert len(cardlst) == 3, 'Three integers separated by commas needed.'  # error if the length is not 3

                # checks through the characters of the string, if its integer 0-9 and checks no repetition
                for num in cardlst:
                    assert len(num) > 0, 'Please enter 3 numbers to indicate card number'
                    for char in num:
                        assert char.isdecimal(), 'Please enter valid integer to represent card number'
                    assert num == '0' or self.hand.index(self.hand[0]) < int(num) < self.hand.index(self.hand[-1]) + 1, 'Please enter number in range'
                    assert cardlst.count(num) == 1, 'No repetition of card number.'

                # Stop the while loop by using break
                break

            except Exception as e:
                print(e)

        # Append card from cardlst into cards and remove them from player hand
        num_popped = 0
        for num in cardlst:
            cards.append(self.hand.pop(int(num) - num_popped))  # The length will decrease after pop so need to count the number of pops.
            num_popped += 1
        return cards

    # Print out the current hand card to user to have a look
    def print_hand(self):

        """
        Print current hand to user.
        """

        index_str = ''      # for printing index line below the card art.
        card_art_lst = []   # list to contain lists of individual cards from player's hand

        # sorts player's hand for printing
        self.hand = sorted(self.hand)

        for card in self.hand:                  # all cards in player's hand to be added to card_art_lst in art string form.
            card_art_lst.append(str(card).split('\n'))         # card art split into pieces, together added into the card_art_lst

        for art_piece_index in range(len(card_art_lst[0])):     # range(len(card_art_lst[0])) measures number of parts (rows / top to bottom) in single card art string, card #0 is taken as the benchmark. So it iterates through every row
            for card in card_art_lst:                           # iterates through every card.
                print(card[art_piece_index],end='')             # prints specified row of that card, specified row indicated by art_piece_index
            print(end='\n')                                     # there after completion of the single row, will move to new line.

        card_str_len = len(card_art_lst[0][0])                  # tracks the number of columns used of a single card's string (width/ one side to another)/ First string of the first card (len(card_art_lst[0][0])) is used as benchmark.

        for card_index in range(len(self.hand)):
            index = str(card_index)                             # index will represent card number
            while len(index) != card_str_len:                   # if length not same as the width of card, will add whitespace to right
                index = index + ' '
                if len(index) != card_str_len:                  # reaffirms if length not same as the width of card, will add whitespace to left, to make it even.
                    index = ' ' + index
            index_str += index                                  # index_str concatenated with index (string).
        print(index_str)                                        # prints the final index line


if __name__ == "__main__":
    # Test your function here
    player = HumanPlayer()
    player.hand = [Card(Rank.Ace, Suit.Diamonds), Card(Rank.Ten, Suit.Hearts), Card(Rank.Seven, Suit.Spades),
                   Card(Rank.Queen, Suit.Hearts), Card(Rank.Four, Suit.Diamonds), Card(Rank.Queen, Suit.Spades),
                   Card(Rank.Six, Suit.Spades), Card(Rank.Five, Suit.Spades), Card(Rank.King, Suit.Clubs),
                   Card(Rank.Two, Suit.Hearts), Card(Rank.King, Suit.Hearts), Card(Rank.Three, Suit.Hearts),
                   Card(Rank.Jack, Suit.Hearts), Card(Rank.Jack, Suit.Spades), Card(Rank.Ace, Suit.Spades),
                   Card(Rank.Seven, Suit.Hearts), Card(Rank.Seven, Suit.Diamonds)]

    player.play_card([Card(Rank.Two, Suit.Clubs)], False)


