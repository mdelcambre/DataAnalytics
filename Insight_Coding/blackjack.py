#!/usr/bin/env python

""" Blackjack Game for the coding challenge submitted as round 2 of the Data
Engineering Fellows program.

Prompt:

Insight Data Engineering Fellows Program - Coding Challenge

We'd like you to implement a text-based Blackjack program in one of the
following programming languages: Java, Clojure, Scala, C, C++, Python, or Ruby.
There should be one player and one dealer. The dealer should hit until his hand
value is 17 or greater. You should implement the basic actions of hitting and
standing. Implementing the more advanced actions such as splitting is optional.
The player should start with 100 chips and must bet at least 1 chip each hand.
"""


import random
from time import sleep

__author__ = "Mark Delcambre"
__copyright__ = "Copyright 2014, Mark Delcambre"
__license__ = "GPL"
__version__ = "0.1"

__maintainer__ = "Mark Delcambre"
__email__ = "mark@delcambre.com"
__status__ = "Prototype"


class deck_of_cards:
    """Implements the deck of cards for blackjack.
    Assembles a deck and shuffles it. After you can shuffle, deal multiple cards
    and compute the minimum total value of the deck (to detect when you need to
    reshuffle the deck)"""

    cards = [
        ("Ace",1),
        ("Two",2),
        ("Three",3),
        ("Four",4),
        ("Five",5),
        ("Six",6),
        ("Seven",7),
        ("Eight",8),
        ("Nine",9),
        ("Ten",10),
        ("Jack",10),
        ("Queen",10),
        ("King",10),
    ]
    suits = [
        "Spades",
        "Clubs",
        "Diamonds",
        "Hearts",
    ]

    clean_deck = []
    "Assembles the class base deck from the arrays above."
    for i in cards:
        for j in suits:
            clean_deck.append(i+(j,))


    def __init__(self):
        """Copy the deck of cards from the clean class variable, shuffle them,
        and set the number of cards dealt to zero"""
        self.deck = deck_of_cards.clean_deck
        random.shuffle(self.deck)
        self.dealt = 0

    def deal(self,number):
        """Deals out a given number of Cards and increments
        the offset in the pre-shuffled deck"""
        card = []
        for i in range(0,number):
            card.append(self.deck[self.dealt+i])
        self.dealt += number
        return card

    def shuffle(self):
        """Shuffle the deck and set the number of dealt to zero
        The class doesn't keep track of return cards so a deck cannot be
        shuffled with cards still in play"""
        random.shuffle(self.deck)
        self.dealt = 0

    def cards(self):
        return 52-self.dealt


class dealer:
    """Implements the base player class as the dealer, keeps track of hand.
    Functions have support for splitting for the player child class to extend"""

    def __init__(self,deck):
        'Initialize the dealer: Deal one card to the hand'
        self.deck = deck

    def cheat(self,hand):
        'A function used for testing, allows for setting the hand'
        self.cards = hand

    def hand(self):
        'Returns the current hand'
        return self.cards

    def value(self):
        'Calculate the value of the hand, automatically handle aces'
        total=[0,0]
        for i in range(0,len(self.cards)):
            total[i] = sum(j[1] for j in self.cards[i])
            """If any card is an ace, we check the total value of the hand, if
            the hand has a value of less than 12, then we can add the addition
            value to the hand. It is impossible for two aces to have a value of
            11"""
            for card in self.cards[i]:
                if card[0] == "Ace":
                    if total[i] < 12:
                        total[i] += 10 #Ace has already been counted for 1 point
        return total

    def hit(self,hand):
        """Implements hitting, deals a card from the stored deck and places into
        the given hand index."""
        self.cards[hand].extend(self.deck.deal(1))
        return self.cards

    def new_deal(self):
        'Replaces the current hand with a newly dealt hand of 1 card'
        self.cards = [self.deck.deal(1),] #stored in array for player splitting


class player(dealer):
    'Extends the dealer class to implement betting commands and track chips'

    def __init__(self,deck,chips):
        """Initiates the player child class of dealer andsets chips to the
        value passed in."""
        self.deck = deck
        self.chips = chips
        self.cards = [[],]

    def bet(self,bet):
        'Bets chips, returns the current value of chips or -1 if not enough'
        if bet > self.chips:
            return -1
        self.chips -= bet
        return self.chips

    def win(self,winnings):
        'Adds to the chips value after a bet'
        self.chips += winnings

    def bank(self):
        'Returns the number of chips the player currently has'
        return self.chips

    def new_deal(self):
        'Replaces the current hand with a newly dealt hand of 2 card'
        self.cards = [self.deck.deal(2),] #stored in array for splitting later

    def split(self,bet):
        """Checks for proper conditions and then splits the hand, dealing one
        to each of the two new hands"""
        if bet > self.chips: # check if sufficent funds
            return -1
        if self.cards[0][0][0] != self.cards[0][1][0]: #are they the same card?
            return -2
        self.chips -= bet
        self.cards = [
                [self.cards[0][0],self.deck.deal(1)[0]],
                [self.cards[0][1],self.deck.deal(1)[0]],
        ]
        return 0

def main():

    start_chips = 100
    min_bet = 1

    clear_line()
    print "Starting game of blackjack"
    global user
    global deck
    global comp
    deck   = deck_of_cards()
    user   = player(deck,start_chips)
    comp   = dealer(deck)
    first  = True

    while True:
        if user.bank() < 1:
            print "You do not have enough chips to keep playing."
            again = raw_input("Would you like to play again? (Y/N):")
            if again.lower().strip()[0] is 'y':
                user = player(deck,start_chips)
                comp = dealer(deck)
            elif again.lower().strip()[0] is 'n':
                break
            else:
                print "Input not regonized"
                continue
        elif first is False:
            print "You currently have %d chips" % (user.bank())
            more = raw_input("Would you like to play another round? (Y/N):")
            if more.lower().strip()[0] is 'y':
                pass
            elif more.lower().strip()[0] is 'n':
                break
            else:
                print "Input not regonized."
                continue
        new_deal()
        first = False

    clear_line()
    print "Thank you for playing."


def new_deal():
    'Start of a new deal in a game'
    global deck
    global user
    global comp

    clear_line()

    # Check to make sure the deck has enough value to bust three hands
    if deck.cards() < 21: #worst case 20 cards is needed to establish a winner
        print "Deck has too few cards, reshuffling"
        clear_line()
        deck.shuffle()


    while True:

        bet = raw_input("You have %d chips. "\
                        "Please input your bet: "%(user.bank()))

        # Validate that input is a positive intiger and does not exceed the bank
        if bet.isdigit() is False or int(bet) < 0:
            print "Not Valid Input"
            continue    # Not valid try for input again
        elif int(bet) == 0:
            print "You must bet at least 1 chip"
            continue

        if user.bet(int(bet)) < 0:
            print "You do not have enough chips to make that bet"
            continue    # Too big of a bet, try again
        print "You have %d chips remaining" % (user.bank())
        break
    bet = int(bet)

    user.new_deal() # Now that we have established the bet, deal the cards
    comp.new_deal() # After player gets cards, dealer now gets its
    clear_line()    # print a pretty line

    print_screen()
    player_actions(bet)
    sleep(1)
    dealer_actions(bet)



def player_actions(bet):
    global user
    global comp
    global deck

    split_hand = 0 #Used as the index for which hand is currently being played.
    while True: # This is the player action loops

        if user.value()[split_hand] is 21: # check if player has 21 boints
            if split_hand < len(user.hand())-1: # detect if first of split hands
                print "Your first hand has 21 points. Switching to second hand"
                split_hand  = 1
                continue
            else: # Either only one hand or second of split hands
                print "You have 21 points."
                return 0
        elif user.value()[split_hand] > 21:
            if split_hand < len(user.hand())-1:
                print "Your first hand has busted. Switching to second hand"
                split_hand  = 1
                continue
            else:
                print "You have busted."
                return 0

        # Check if split is valid, need the face to match and have enough chips
        if user.hand()[0][0][0] is user.hand()[0][1][0] and \
           user.bank() >= bet and \
           len(user.hand()) is 1:
            # Conditions for split met.
            action = raw_input("Would you like to Stand, Hit, or Split?")
            if action.lower().strip() == 'stand':
                clear_line()
                print "You have chosen to stand."
                clear_line()
                return 0
            elif action.lower().strip() == 'hit':
                clear_line()
                print "You have hit."
                clear_line()
                user.hit(split_hand)
                print_screen()
            elif action.lower().strip() == 'split':
                if user.split(bet) < 0:
                    print "You can't split right now."
                    continue
                clear_line()
                print "Splitting"
                clear_line()
                print_screen()
                continue
            else:
                print "I'm sorry, I didn't understand you."
                continue

        # Ask for the user action, detect if we are dealing with a split hand
        if len(user.hand()) is 2 and split_hand is 0:
            action = raw_input("Would you like to [S]tand or [H]it on your "\
                           "First Hand? ")
        elif len(user.hand()) is 2 and split_hand is 1:
            action = raw_input("Would you like to [S]tand or [H]it on your "\
                           "Split Hand? ")
        else:
            action = raw_input("Would you like to [S]tand or [H]it? ")


        # Handle Standing: If first split hand, switch hands.
        if action.lower().strip()[0] is 's':
            if split_hand < len(user.hand())-1:
                print "You have chosen to stand your first hand. "\
                      "Switching to second hand."
                split_hand  = 1
                continue
            else:
                print "You have chosen to stand, dealers play now."
                return 0

        # Handle Hitting on current hand
        elif action.lower().strip()[0] is 'h':
            clear_line()
            print "You have hit."
            clear_line()
            user.hit(split_hand)
            print_screen()

        # Input didn't hit any of our actions, repeat the loop.
        else:
            print "I'm sorry, I didn't understand you."
            continue


def dealer_actions(bet):
    global user
    global comp

    # Store the players score, but busts are stored as 0
    user_score = map(lambda x: 0 if x >21 else x, user.value())

    #comp.hit(0)

    while comp.value() < 18 and sum(user_score) >0:
        clear_line()
        print "Dealer Hits"
        clear_line()
        comp.hit()
        print_screen()
        sleep(0.7)

    clear_line()
    print "Dealer Stays"
    clear_line()
    print_screen()
    sleep(1)

    comp_score = 0 if comp.value()[0] > 21 else comp.value()[0]

    clear_line()

    for i in range(0,len(user.hand())):

        if len(user.hand()) == 2:
            hand = ' first ' if i == 1 else ' split '
        else:
            hand = ' '

        if user_score[i] > comp_score:
            print ("Your%shand beat the dealer." % (hand)),
            if user_score[i] == 21 and len(user.hand()[i]) == 2:
                user.win(int(bet*3.5))
                print "BLACKJACK You win %d chips" %(int(bet*3.5))
            else:
                user.win(2*bet)
                print "You win %d chips" % (int(bet*2))
        elif user_score[i] == 21 and\
                len(user.hand()[i]) == 2 and\
                len(comp.hand()[0]) > 2:
            user.win(int(bet*3.5))
            print "Your%shand beat the dealer. BLACKJACK. You win %d chips"\
                    % (hand,int(bet*3.5))
        else:
             print "Your%shand lost to the dealer" % (hand)


def print_screen():
    global user
    global comp

    print "The dealer hand: %s\n" % (fancy_print(comp.hand()[0]))
    if len(user.hand()) is 2:
        print "Your first hand is: %s" % (fancy_print(user.hand()[0]))
        print "Your split hand is: %s\n" % (fancy_print(user.hand()[1]))
    else:
        print "Your hand is: %s\n" % (fancy_print(user.hand()[0]))




def clear_line():
    'Prints a break bar to help see what is going on'
    print "--------------------------------------------------------------------"
    print ""


def fancy_print(hand):
    string = ""
    for card in hand:
        string += "%s of %s, " % (card[0],card[2])
    return string[:-2]



main()

 



