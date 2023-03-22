#!/usr/bin/env python
# coding: utf-8

# # Lab 4

# You are tasked with evaluating card counting strategies for black jack. In order to do so, you will use object oriented programming to create a playable casino style black jack game where a computer dealer plays against $n$ computer players and possibily one human player. If you don't know the rules of blackjack or card counting, please google it. 
# 
# A few requirements:
# * The game should utilize multiple 52-card decks. Typically the game is played with 6 decks.
# * Players should have chips.
# * Dealer's actions are predefined by rules of the game (typically hit on 16). 
# * The players should be aware of all shown cards so that they can count cards.
# * Each player could have a different strategy.
# * The system should allow you to play large numbers of games, study the outcomes, and compare average winnings per hand rate for different strategies.

# In[20]:


import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}


# 1. Begin by creating a classes to represent cards and decks. The deck should support more than one 52-card set. The deck should allow you to shuffle and draw cards. Include a "plastic" card, placed randomly in the deck. Later, when the plastic card is dealt, shuffle the cards before the next deal.

# In[31]:


class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
class Deck:
    def __init__(self):
        self.deck = [] #making an empty list of a deck
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) #adding cards to the deck

    def __str__(self):
        deck_of_cards = ''
        for card in self.deck:
            deck_of_cards += '\n '+card.__str__()
        return 'The deck has: '+ deck_of_cards
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal_1(self):
        return self.deck.pop(0)


# In[32]:


deck1 = Decks()
print(deck1)


# 2. Now design your game on a UML diagram. You may want to create classes to represent, players, a hand, and/or the game. As you work through the lab, update your UML diagram. At the end of the lab, submit your diagram (as pdf file) along with your notebook. 

# 3. Begin with implementing the skeleton (ie define data members and methods/functions, but do not code the logic) of the classes in your UML diagram.

# 4. Complete the implementation by coding the logic of all functions. For now, just implement the dealer player and human player.

# In[22]:


class Player:
    def __init__(self,name,chips):
        self.name = name
        self.chips = chips
        self.bet = 0
        
    def __str__(self):
        print_info = 'Player {} has {} chips\n'.format(self.name,self.chips)
        return print_info
    
    def add_chips(self,chips):
        self.chips += chips
        
    def rem_chips(self,chips):
        if chips > self.chips:
            print("Not enough chips")
            print("Current balance = {}".format(self.chips))
        else:
            self.chips -= chips
            print("Current balance = {}".format(self.chips))

##############################################################################

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def __str__(self):
        in_hand = 'Cards on hand is: \n'
        for x in range(len(self.cards)):
            in_hand += str(self.cards[x]) + "\n"
        return "This hand has a value of {}.\n\n".format(self.value) + in_hand
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
        
        if card.rank == "Ace":
            self.aces += 1
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


# ### Game Functions

# In[37]:


def take_bets(player):
    while True:
        try:
            current_bet = int(input("How many Chips would you like to bet : "))
        except:
            print("Enter a Valid Number of Chips.")  
        else:
            if current_bet > player.chips:
                print("Unsufficient Amount. Please try again.")
            else:
                player.bet += current_bet
                player.chips -= current_bet
                break
                
def create_player():
    global player
    while True:
        player_name = input("\nEnter your name: ")
        if player_name != '':
            break
        else:
            print("Enter a valid name\n")

    while True:
        try:
            start_am = int(input("Enter starting chip amount: "))
        except:
            print("Please enter a valid amount.\n")
        else:
            break
    player = Player(player_name,start_am)

def chip_adjust(winner):
    if winner == "player":
        player.chips += int(player.bet*1.5)
        player.bet = 0
    elif winner -- "tie":
        player.chips += player.bet
        player.bet = 0
    else:
        player.bet = 0

def hit_stand(player_hand,deck):
    global playing
    while True:
        st =input("Do you want to hit or stand, type h or s: ")
        if st == '':
            print("Not a valid option, try again.\n")
        elif st[0].lower() == 'h':
            player_hand.add_card(deck.deal_1())
        elif temp[0].lower() == 's':
            playing = False
            break
        else:
            print("Try again.\n")
    if temp[0].lower() == 'h':
        return "h"
    else:
        return "s"

#winning functions
def player_busted():
    global winner

    print("\nPlayer Busted.")
    print("Dealer Wins!\n")
    winner = "dealer"

def dealer_busted():
    global winner

    print("\nDealer Busted.")
    print("Player Wins!\n")
    winner = "player"

def player_dealer_tie():
    global winner
    print("IT'S A TIE!!\n")
    winner = "tie"

def player_wins():
    global winner
    print("Player Wins!\n")
    winner = "player"

def dealer_wins():
    global winner
    print("Dealer Wins!")
    winner = "dealer"

#Functions to show a partial hand and for both hands
def show_cards(player_hand,dealer_hand):
    print("\nPlayer cards: ")
    for card in player_hand.cards:
        print(" "+str(card))
    print("\nDealer cards: ")
    print(" "+str(dealer_hand.cards[0]))
    print("~~There is a hidden card~~")
    
def show_all(player_hand,dealer_hand):
    print("\nPlayer cards: ")
    for card in player_hand.cards:
        print(" "+str(card))
    print("\Dealer cards: ")
    for card in dealer_hand.cards:
        print(" "+str(card))


# ### Running Game function

# In[38]:


def game_run(player):
    print("Welcome to Lab 4 Blackjack! Get as close to 21 withut going over!")
    while True:

        #create deck and shuffle
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        dealer_hand = Hand()

        print("\n_________________________________________________________\n")

        #making a player and taking a bet
        print(player)
        take_bets(player)

        #dealing cards to player and dealer
        for p in range(2):
            player_hand.add_cards(deck.deal_1())
        for d in range(2):
            dealer_hand.add_cards(deck.deal_1())

        #player turn
        show_cards(player_hand,dealer_hand)
        player_play = True
        while playing == True:
            if player_hand.value == 21:
                break
            elif player_hand.value > 21:
                player_busted()
                break
            ask = hit_stand(player_hand,deck)
            if ask == 's':
                break
            show_cards(player_hand,dealer_hand)
        show_all(player_hand,dealer_hand)

        #dealer turn
        dealer_play = True
        while dealer_play:
            if player_hand.value <= 21:
                while dealer_hand.value < 17:
                    print("\nThe dealer hits!")
                    dealer_hand.add_card(deck.deal_1())
                    show_all(player_hand,dealer_hand)
                dealer_play = False
                if dealer_hand.value > 21:
                    dealer_busted()
                    break
                elif player_hand.value == dealer_hand.value:
                    player_dealer_tie()
                    break
                elif player_hand.value > dealer_hand.value:
                    player_wins()
                    break
                else:
                    dealer_wins()
                    break
            else:
                break
        adjust_winnings(winner)
        print("\n" + str(player))


# 5.  Test. Demonstrate game play. For example, create a game of several dealer players and show that the game is functional through several rounds.

# In[39]:


playing = True
player_1 = create_player()
game_run(player_1)


# 6. Implement a new player with the following strategy:
# 
#     * Assign each card a value: 
#         * Cards 2 to 6 are +1 
#         * Cards 7 to 9 are 0 
#         * Cards 10 through Ace are -1
#     * Compute the sum of the values for all cards seen so far.
#     * Hit if sum is very negative, stay if sum is very positive. Select a threshold for hit/stay, e.g. 0 or -2.  

# 7. Create a test scenario where one player, using the above strategy, is playing with a dealer and 3 other players that follow the dealer's strategy. Each player starts with same number of chips. Play 50 rounds (or until the strategy player is out of money). Compute the strategy player's winnings. You may remove unnecessary printouts from your code (perhaps implement a verbose/quiet mode) to reduce the output.

# In[ ]:





# 8. Create a loop that runs 100 games of 50 rounds, as setup in previous question, and store the strategy player's chips at the end of the game (aka "winnings") in a list. Histogram the winnings. What is the average winnings per round? What is the standard deviation. What is the probabilty of net winning or lossing after 50 rounds?
# 

# In[ ]:





# 9. Repeat previous questions scanning the value of the threshold. Try at least 5 different threshold values. Can you find an optimal value?

# 10. Create a new strategy based on web searches or your own ideas. Demonstrate that the new strategy will result in increased or decreased winnings. 

# In[ ]:




