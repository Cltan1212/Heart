# __future__ module is a built-in module in Python that is used to inherit new features that will be available in the new Python versions.
from __future__ import annotations
# From the task 1 which is cards import the class that inside the class which is Card, Rank and Suit. 
from cards import Card, Rank, Suit
# From task 2 which is basic_ai import the class BasicAIPlayer. 
from basic_ai import BasicAIPlayer
# From class player which is used to check how many cards that is valid to play import Player 
from player import Player


# Create an AI player who use more advanced strategies of playing the hearts game
class BetterAIPlayer(Player):

    """
    AI player that implement more advanced strategy of play rather than the greedy approach.
    """

    # __init__ is a reserved method
    # Define a method which use to initialise class by setting the passed argument as instance variable
    # super() means that it return the object that represents the parent class
    def __init__(self, name):
        super().__init__(name)
        self.plan = None

    # __str__ is a magic method that return a string representation when we print the object
    # Define a method which use to return name as string.
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    # Define a method called play_card with the parameter trick and broken_hearts
    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:

        """
        Determine a card to play on a given trick.
        Arguments:
        - trick: a list of Card
        - broken_hearts: boolean that indicate the status of broken hearts
        Returns the lowest ranking card from the player's hand that constitutes a valid play
        """

        play_lst = []  # A list to contain valid cards for deciding a card to play

        # Append card into play_lst based on self.plan
        # Sneaky -> put the valid card (but not Queen of Spades) into play_lst
        if self.plan[0] == 'sneaky':
            for card in self.hand:
                if (card != Card(Rank.Queen, Suit.Spades)) and (self.check_valid_play(card, trick, broken_hearts)[0] is True):
                    play_lst.append(card)

        # Domination -> put the valid card but not same suit as the suit return from self.plan into play_lst
        elif self.plan[0] == 'domination':
            for card in self.hand:
                if (card.suit != self.plan[1]) and (self.check_valid_play(card, trick, broken_hearts)[0] is True):
                    play_lst.append(card)

        # We play the maximum card in play lst
        # But if there is no card inside play_lst, there are two plan to continue executed which is plan high and plan low
        if len(play_lst) == 0:
            for card in self.hand:
                if self.check_valid_play(card, trick, broken_hearts)[0] is True:
                    play_lst.append(card)

            play_card = max(play_lst)
        
        # If the play_card have cards, play_card would be the maximum number of the card in play_lst and remove it after player play the particular card
        else:
            play_card = max(play_lst)

        self.hand.remove(play_card)
        return play_card

    # Task 5 Passing card
    # Define a method which called pass_card() with a parameter self (a reference to the current instance of the class)
    # Pass_cards() to return their chosen 3 cards to pass off at the start of each round
    # There are 6 plans to remove the card which are 'sneaky', 'remove,domination', 'play low', 'play high' and 'shoot the moon'
    def pass_cards(self) -> list:
        """
        Determine three cards to pass on a given round.
        Argument: None
        Returns a list of three cards from the player's hands to pass off and
        remove them from self.hand before returning.
        """
        cardlst = []              # Used to store the card that player need to pass later
        self.plan = self.strat()  # Decide on strategy

        # Before passing the card we check our strategy and filtered some cards
        # sneaky -> play for delayed spades execution (as the last card) so we're not going to pass Queen of Spades
        if self.plan[0] == 'sneaky':
            for card in self.hand:                            # Append the card which is not Queen of Spades into the cardlst
                if card != Card(Rank.Queen, Suit.Spades): 
                    cardlst.append(card)

        # remove -> remove Queen of Spades
        elif self.plan[0] == 'remove':
            cardlst.append(Card(Rank.Queen, Suit.Spades))
            self.hand.remove(Card(Rank.Queen, Suit.Spades))
            for _ in range(2):
                cardlst.append(max(self.hand))
                self.hand.remove(max(self.hand))
            return cardlst

        # domination -> remove the card that suit is not same as domination suit
        elif self.plan[0] == 'domination':
            for card in self.hand:
                if card.suit != self.plan[1]:
                    cardlst.append(card)

        # play low -> remove nothing
        elif self.plan[0] == 'play low':
            for card in self.hand:
                cardlst.append(card)

        # Start passing three cards here
        # Strategy of playing the game: 'play high' or 'shoot the moon' -> pass the minimum number of three cards
        if self.plan[0] == 'shoot the moon':
            for _ in range(3):
                cardlst.append(min(self.hand))
                self.hand.remove(min(self.hand))
        else:
            newlst = []
            for _ in range(3):
                newlst.append(max(cardlst))     # Append 3 of the maximum number's cards into the newlst and remove it from user's hand cards
                self.hand.remove(max(cardlst))
                cardlst.remove(max(cardlst))
            cardlst = newlst

        # Other plans -> use the list that we filtered before and pass the maximum three cards
        return cardlst

    # Create a method called strat to calculate the number of cards in different suit and based on this, we see whether which plan do we need to execute
    def strat(self) -> tuple:
        """
        Calculate the cards in self hand and decide the best strategy to win the game
        Return a tuple (self plan):
        - sneaky, shoot the moon, remove, domination, play low : strategies
        - suit : use in play card (we don't want to use this suit first)
        """

        # Calculate the number of different suit of the cards
        num_clubs = 0
        num_diamonds = 0
        num_spades = 0
        num_hearts = 0

        # Use for loop to go through every card in player's hand and update the number of suit by adding 1
        for card in self.hand:
            if card.suit == Suit.Clubs:
                num_clubs += 1
            elif card.suit == Suit.Diamonds:
                num_diamonds += 1
            elif card.suit == Suit.Spades:
                num_spades += 1
            elif card.suit == Suit.Hearts:
                num_hearts += 1
        suit_list = [num_clubs, num_diamonds, num_spades, num_hearts]

        # Determine the strategy by checking Queen of Spades
        # Low hearts card -> sneaky
        if Card(Rank.Queen, Suit.Spades) in self.hand:
            if num_hearts <= 4:
                return 'sneaky', None

            # High rank cards (number of card which is more than 8) -> plan: shoot the moon
            num_high_ranks = 0
            for card in self.hand:
                if card > Card(Rank.Eight, Suit.Hearts):
                    num_high_ranks += 1

            if num_high_ranks > 4:
                return 'shoot the moon', None

            # If not in above situation -> remove it
            else:
                return 'remove', None

        # No Queen of Spades continue to determine other strategies here
        # Many cards in same suit -> domination
        if max(suit_list) >= (len(self.hand) - 5):
            suit = suit_list.index(max(suit_list)) + 1
            suit = Suit(suit)
            return 'domination', suit
        else: # regular basic_ai style if options ran out
            return 'play low', None


if __name__ == "__main__":
    # Test your function here
    player = BetterAIPlayer("Test Player 1")
    player.hand = [Card(Rank.Ace, Suit.Diamonds), Card(Rank.Ten, Suit.Hearts), Card(Rank.Seven, Suit.Spades),
                   Card(Rank.Queen, Suit.Hearts), Card(Rank.Four, Suit.Diamonds), Card(Rank.Queen, Suit.Spades),
                   Card(Rank.Six, Suit.Spades), Card(Rank.Five, Suit.Spades), Card(Rank.King, Suit.Clubs),
                   Card(Rank.Two, Suit.Hearts), Card(Rank.King, Suit.Hearts), Card(Rank.Three, Suit.Hearts),
                   Card(Rank.Jack, Suit.Hearts), Card(Rank.Jack, Suit.Spades), Card(Rank.Ace, Suit.Spades),
                   Card(Rank.Seven, Suit.Hearts), Card(Rank.Seven, Suit.Diamonds)]

    print(player.pass_cards())
    print(player.hand)


