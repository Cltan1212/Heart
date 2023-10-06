# __future__ module is a built-in module in Python that is used to inherit new features that will be available in the new Python versions.
from __future__ import annotations
# From the task 1 which is cards import the class that inside the class which is Card, Rank and Suit. 
from cards import Card, Rank, Suit
# From task 2 which is basic_ai import the class which is BasicAIPlayer.
from basic_ai import BasicAIPlayer
# From task 3 which is round import the class which is Round. 
from round import Round
# Random library is imported, which helps load the random module, as it provides a number of random number generation-related functions.
import random


# Main class for game of 'Hearts'
class Hearts:

    def __init__(self) -> None:
        """ 
        Constructor for Hearts
        """
        self.round_num = 1                                      # keeps track of round number, starting with 1
        # target_score keeps track of target score from user / num_of_players keeps track of number of players
        self.target_score, self.num_of_players = self.inputs()  # Input from user, invoked inputs method returns target score and number of player
        self.players = self.initiate()                          # Keeps track of players, to be added in the next lines of code.
        
        # Main program starts
        self.execute()

    # Create a method called initiate, which use to initialise the players and update the player (self player)
    def initiate(self):

        """
        Initialization of players, update self players.
        Return a list of player: BasicAI players.
        """
        players = []

        for player_num in range(self.num_of_players - len(players)):   # Loop for future proofing (for this task no player is initialized before loop )
            player_name = f"Player {player_num + 1}"                   # Player name     
            players.append(BasicAIPlayer(player_name))                 # Adds BasicAIPlayer with name to players list.

        return players

    # Define a method called execute and use to run the program of the hearts game
    def execute(self):
        """
        Main program for execute the hearts game.
        """
        end = False                                             # Initialize end game flag ( False to indicate game not ending )

        while end is False:
            deal = False                                        # Initialize dealing cards flag ( False to indicate dealt cards are not valid )
            while deal is False:                             
                deal = True                                     # Assume all deal are valid at first
                players_preset = self.dealer()                  # Invokes dealer method to deal cards, players_preset to be a list containing lists of cards, each player with their dedicated list of dealt cards.

                # Assign list of cards to each player’s hand
                for player_index in range(len(self.players)):
                    self.players[player_index].hand = players_preset[player_index]

                # Ensure every player has at least one card that isn't the Queen of Spades or from Hearts
                for player in self.players:
                    count = 0                                 # Counter for Hearts or Queen of Spades

                    # Update the counter when the card is either Hearts or Queen of Spade
                    for card in player.hand:
                        if card.suit == Suit.Hearts or card == Card(Rank.Queen, Suit.Spades):
                            count += 1
                            
                    # Flag changes to False to indicate card dealing is not valid, and loop reiterates
                    if count == len(player.hand):
                        deal = False

            # Prints round header
            print(f"========= Starting round {self.round_num} =========")

            # Prints players' hands
            for player in self.players:
                print(f"{player} was dealt {player.hand}")

            self.pass_card_general()    # Pass cards
            Round(self.players)         # Execute round
            end = self.end_game()       # Check end game status
            self.round_num += 1         # Round number updated for next iteration

    # Check whether the user input is valid or not valid, if not valid, print out the error and called the user to enter again
    def inputs(self) -> tuple:

        """
        Validation and capturing of user inputs.
        If the inputs are invalid, prompt the user to enter again with appropriate error message.
        Returns target score and number of players after validating.
        """

        # Will keep prompting user until proper integer input is read for target score, then it breaks from the loop
        while True:
            target_score = input(f'Enter a target score to end the game:') # used to set the target score to end game.

            # The try and except block are used to handle the execptions
            # The assert statement raises an error when the statement is false, with appropriate error message attatched
            try:
                assert len(target_score) > 0, 'Please try again.'               # Error if user input empty

                # Checks through the characters of the string, if its integer 0-9.
                for char in target_score:           
                    assert char.isdecimal(), 'Please enter a positive integer'  # Error if invalid character
                break

            # Error message will be printed and loop reiterates
            except Exception as e:
                print(e)

        # Will keep prompting user until proper integer input is read for number of players, then it breaks from the loop
        while True:
            num_of_players = input('Please enter the number of players (3-5):')        # Input for setting number of players
            try:
                assert len(num_of_players) > 0, 'Please try again.'                    # Error if user input empty

                # Checks through the characters of the string, if its integer 0-9.
                for char in num_of_players:
                    assert char.isdecimal(), 'Please enter a positive integer'         # error if invalid character
                
                # Checks if entered integer is within range
                assert 3 <= int(num_of_players) <= 5, 'Please enter a number in range' # error if not in range
                break

            # Error message will be printed and loop reiterates
            except Exception as e:
                print(e)

        # Return the integer value of target_score and num_of_players to fulfill the condition in the later task
        return int(target_score), int(num_of_players)

    # Create a method which use to create deck, shuffle and deal the cards
    def dealer(self) -> list:

        """
        Create deck, shuffle and deal the cards.
        Return a list of list of cards (nested list) after shuffle and deal the cards.
        """

        deck = []               # Initialise the deck to store a deck of 52 cards
        hands = []              # Initialise hands to contain players' hand (list of hands)
        for _ in self.players:  # Generates an empty list to represent each player's hand.
            hands.append([])

        # Generates all 52 cards for the list, then check the condition_1 and condition_2
        for suit in Suit:
            for rank in Rank:
                deck.append(Card(rank, suit))

        # Condition_1: the card Two of Diamonds will be remove if num_of_players is 3
        if self.num_of_players == 3:
            deck.remove(Card(Rank.Two, Suit.Diamonds))

        # Condition_2: the cards Two of Diamonds and Two of Spade will be remove if num_of_players is 5
        elif self.num_of_players == 5:
            deck.remove(Card(Rank.Two, Suit.Diamonds))
            deck.remove(Card(Rank.Two, Suit.Spades))

        # Randomly pops a card from deck and move it into the player's hand
        random_deck = random.sample(deck, len(deck))

        while len(random_deck) > 0:
            for player_index in range(len(self.players)):
                hands[player_index].append(random_deck.pop(0))

        return hands  # list containing every one of the player's hand
    
    # Create a method which use to pass the 3 of the hand's card to appropriate corresponding player
    def pass_card_general(self):

        """
        Handles passing of cards
        All players will be passing cards, determines passers and receivers, and corresponding cards.
        Each player chooses 3 cards to pass, which should be passed to corresponding determined receiver.
        """

        pass_ahead = self.round_num % len(self.players)                     # Number of players ahead to pass to
        pass_cards = []                                                     # List to contain lists of cards to be passed to specified player
        receivers = []                                                      # List containing receiver's player index, works in conjunction with pass_cards

        if self.round_num != self.num_of_players:                           # Execute if not round number

            for player_index in range(len(self.players)):                   # Players gets turn to pass cards.
                pass_ahead_index = pass_ahead                               # Reassign the pass_ahead_index after wrap around manipulation incurred

                if player_index + pass_ahead > len(self.players) - 1:       # If player to pass ahead is an overshot,
                    pass_ahead_index -= len(self.players)                   # Wrap around occurs

                pass_cards.append(self.players[player_index].pass_cards())  # player passes card and list of passed cards added into pass_cards
                receivers.append(pass_ahead_index + player_index)           # Receiver's index added to list; sequenced in line with pass_cards

        # All card transfer happens at the end.
        passer_index = 0

        # Update the sequence of passing the card to others
        for player_index in receivers:
            print(f"{self.players[passer_index]} passed {pass_cards[0]} to {self.players[player_index]}") # pass_cards[0] will be effective because pop happens in the next lines of code.
            passer_index += 1
            for pass_card in pass_cards.pop(0):                             # Iterate through the popped pass_cards list to obtain individual pass_card list.
                self.players[player_index].hand.append(pass_card)           # Player receives passed cards.

    # Create a method which use to determine the status of end of game
    def end_game(self):
        """
        Determine if the game has finished, printing the round result before returning.
        Returns True to end the game or False if not. If true winner is printed before return.
        """

        min_total = self.players[0].total_score             # Minimum total score (determines the winner)
        num_of_min_total = 0                                # Number of players who obtained minimum total score
        max_total = 0                                       # Maximum total score (determines if passed target score)
        max_round_score = 0                                 # Maximum round score (determines if a player shot the moon)

        # Round score manipulation
        for player in self.players:
            if player.round_score > max_round_score:
                max_round_score = player.round_score

        if max_round_score == 26:  # shot the moon
            for player in self.players:
                if player.round_score == 26:            # Means this player has shot the moon
                    player.round_score = 0              # Player gets 0 for the round
                    print(f"{player} has shot the moon! Everyone else receives 26 points")
                else:
                    player.round_score = 26             # Other players receives 26 points as penalty

        for player in self.players:
            player.total_score += player.round_score    # Updates to player's total score.
            player.round_score = 0

        for player in self.players:
            if player.total_score < min_total:          # Find minimum total score
                min_total = player.total_score
            if player.total_score > max_total:          # Finds maximum total score
                max_total = player.total_score

        for player in self.players:                     # Finds number of players with minimum total score
            if player.total_score == min_total:
                num_of_min_total += 1
        
        print(f"========= End of round {self.round_num} =========")
        for player in self.players:  # prints round stats
            print(f"{player}'s total score: {player.total_score}")

        if (num_of_min_total > 1) or (max_total < self.target_score):   # If more than 1 minimum scorer or scores less than target score, game continues
            return False
        else:
            for player in self.players:                                 # Otherwise, search for winner (with minimum score) and game ends.
                if player.total_score == min_total:
                    print(f"{player} is the winner!")
            
            return True


if __name__ == "__main__":
    Hearts()

