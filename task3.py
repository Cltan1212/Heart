# __future__ module is a built-in module in Python that is used to inherit new features that will be available in the new Python versions.
from __future__ import annotations
# From task 1 which is cards import the class which are Card, Rank and Suit. 
from cards import Card, Rank, Suit
# From task 2 which is basic_ai import the class which is BasicAIPlayer.
from basic_ai import BasicAIPlayer


# Task 3: Round
# Create a class called Round that takes a list of players (assume that players' hands have been dealt and cards have been passed before the Round is called) and executes a round of the game
class Round:
    """Round class represents and manipulates each round in Hearts game"""

    # Define a method which use to initialise the class by setting the passed arguments as instance variables
    def __init__(self, players: list[Player]) -> None:
        self.players = players                 # List players in the game
        self.broken_hearts = False             # Broken_hearts is initialise to false, it will change to true when hearts is broken
        self.leader = self.initiate()
        for _ in range(len(players[0].hand)):  # Round continue after player plays all card
            self.execution()

    # Define a method which use to initialise who is the leader(who take the Two of Clubs card)
    def initiate(self) -> int:
        """
        Initialize the leader to play the first round.
        Return an integer which is the index of the player that will lead the round.
        """
        
        # Initialise the player into None and the value of leader will update after execute the for loop
        leader = None

        # By using for loop to find who is the leader in which the player takes Two of Clubs 
        for player_index in range(len(self.players)):
            if Card(Rank.Two, Suit.Clubs) in self.players[player_index].hand:
                leader = player_index           # index of player that will lead the round

        # Return the index of the player (integer type) that lead in players
        return leader

    # Define a method called execution with parameter self which represent an instance(object) of the given class
    def execution(self) -> None:
        """
        Execute each round for each player to play their card.
        After each round ends, score for the current round will be calculated.
        """

        # Initialise the player_step_lst and trick as a empty list 
        player_step_lst = []    # Will be used to store the order of the player
        trick = []              # Will be used to store the cards played in a single trick  

        # Each round begin with leader and the player after 
        # Example: when leader is player 2, the order of the player would be player 2 (leader), player 3, player 4, player 1
        for player in self.players[self.leader:]:
            trick, player_step_lst = self.plays(player, trick, player_step_lst)
        for player in self.players[:self.leader]:
            trick, player_step_lst = self.plays(player, trick, player_step_lst)

        # Finds the max (applicable) card in the trick -> to find the next round leader (who takes the trick)
        max_card = trick[0]
        for card in trick:
            if (card.suit == max_card.suit) and (max_card < card):
                max_card = card                                 # Updates the max_card with the condition when the suit is the same and if higher Rank.

        # Find the player's index who plays the max card -> leader (who takes the trick)
        leader = player_step_lst[trick.index(max_card)]         # player_step_lst works in conjunction to trick, can determine the player with same index as max card
        self.leader = self.players.index(leader)                # Index of leader instead of player object
        pre_calc = self.players[self.leader].round_score        # Round score of leader will be manipulated for taking the trick, but a copy (pre-calculated) will be stored.
                                                    
        # Updates leader's round score
        # If the card is Queen of Spades, the player who takes the trick will add 13 points. For hearts suit cards, it will only add 1.
        for card in trick:
            if card == Card(Rank.Queen, Suit.Spades):
                self.players[self.leader].round_score += 13

            elif card.suit == Suit.Hearts:
                self.players[self.leader].round_score += 1
        
        post_calc = self.players[self.leader].round_score       # Score that leader received so far (including previous rounds score)
        print(f"{self.players[self.leader]} takes the trick. Points received: {post_calc - pre_calc}") # f means f-string which can be formatted in much the same way that you would with str.format()

    # Define a method called plays with parameter player, trick and player_step_lst which use to play the cards and print out the card that player play
    def plays(self, player, trick, player_step_lst):

        """
        Player plays card and prints out the moves.
        Arguments:
        - player: who plays the cards
        - trick: a list of cards played in the trick so far, in order of play
        - player_step_lst: the sequence players play in a round (list of players)
        Returns trick and player_step_lst for checking next round leader.
        """

        played_card = player.play_card(trick, self.broken_hearts)
        trick.append(played_card)               # Played card placed into trick
        print(f"{player} plays {played_card}")
        
        if (played_card.suit == Suit.Hearts) and (self.broken_hearts is False): # updates broken hearts
            self.broken_hearts = True        
            print("Hearts have been broken!")
        
        player_step_lst.append(player)          # Updates the player_step_lst with the player (who played the card) for later use.
        return trick, player_step_lst


if __name__ == "__main__":
    players = [BasicAIPlayer("Player 1"), BasicAIPlayer("Player 2"), BasicAIPlayer("Player 3"),
               BasicAIPlayer("Player 4")]
    players[0].hand = [Card(Rank.Four, Suit.Diamonds), Card(Rank.King, Suit.Clubs), Card(Rank.Nine, Suit.Clubs),
                       Card(Rank.Ace, Suit.Hearts)]
    players[1].hand = [Card(Rank.Two, Suit.Clubs), Card(Rank.Four, Suit.Spades), Card(Rank.Nine, Suit.Spades),
                       Card(Rank.Six, Suit.Diamonds)]
    players[2].hand = [Card(Rank.Seven, Suit.Diamonds), Card(Rank.Ace, Suit.Spades), Card(Rank.Jack, Suit.Diamonds),
                       Card(Rank.Queen, Suit.Spades)]
    players[3].hand = [Card(Rank.Queen, Suit.Hearts), Card(Rank.Jack, Suit.Clubs), Card(Rank.Queen, Suit.Diamonds),
                       Card(Rank.King, Suit.Hearts)]

    Round(players)

