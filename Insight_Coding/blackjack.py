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
from textwrap import wrap

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
    'Handles the main game loop and sets up the game'

    start_chips = 100

    header("Welcome to Blackjack. Starting new game")

    # global the class instances instead of passing them to each function
    global user
    global deck
    global comp
    deck   = deck_of_cards()
    user   = player(deck,start_chips)
    comp   = dealer(deck)
    first  = True


    # Main Loop: Handles input for starting a new deal or game
    while True:
        if user.bank() < 1: # Make sure the player has atleast 1 chip to play
            print "You do not have enough chips to keep playing."
            again = raw_input("Would you like to play again? (Y/N): ")

            # Check player input, whitespace stripped and only check first char
            if again.lower().strip()[0] is 'y':
                user.__init__(deck,start_chips)
                comp.__init__(deck)
            elif again.lower().strip()[0] is 'n':
                break
            else:
                print "Input not regonized"
                continue
        # Check if the player wants to play a new deal,
        # Even if they have enough chips to keep playing
        elif first is False:
            print "You currently have %d chips" % (user.bank())
            more = raw_input("Would you like to play another round? (Y/N): ")

            # Once again, strip whitespace and check only the first character
            if more.lower().strip()[0] is 'y':
                pass
            elif more.lower().strip()[0] is 'n':
                break
            else:
                print "Input not regonized."
                continue

        # Start the new deal of the game.
        new_deal()

        first = False

    header("Thank you for Playing")
    return 0


def new_deal():
    'Start of a new deal in a game'
    global deck
    global user
    global comp

    # Check to make sure the deck has enough value to bust three hands
    if deck.cards() < 21: #worst case 20 cards is needed to establish a winner
        header("Deck has too few cards, reshuffling")
        deck.shuffle()

    # Loop for handling the player bet
    while True:

        bet = raw_input("You have %d chips. "\
                        "Please input your bet: "%(user.bank()))

        # Validate that input is a positive intiger and does not exceed the bank
        if bet.isdigit() is False or int(bet) < 0:
            print "Not Valid Input"
            continue    # Not valid try for input again
        elif int(bet) == 0:
            print "You must bet at least 1 chip"
            continue    # Cannot bet 0 chips, loop again.

        if user.bet(int(bet)) < 0:
            print "You do not have enough chips to make that bet"
            continue    # Too big of a bet, try again

        # If we have made it this far, we know the bet has been valid and exit
        print "You have %d chips remaining" % (user.bank())
        break 

    bet = int(bet)

    user.new_deal() # Now that we have established the bet, deal the cards
    comp.new_deal() # After player gets cards, dealer now gets its

    print_screen("Game has started, Choose your action")

    player_actions(bet)
    sleep(1)
    dealer_actions(bet)
    sleep(1)
    end_of_round(bet)


def player_actions(bet):
    """Handles all of the player actions on a hand. Implements splitting,
    standing, and hitting. Handles the first hand and then the split hand
    until either hands have 21 points, the player stands, or the player
    busts on all hands"""
    global user
    global comp
    global deck

    split_hand = 0 #Used as the index for which hand is currently being played.
    while True: # This is the player action loops


        # Handle verbage if we are dealing with split or normal hands
        if len(user.hand()) == 2:
            hand = ' first ' if split_hand == 0 else ' split '
        else:
            hand = ' '

        if user.value()[split_hand] is 21: # check if player has 21 boints
            if split_hand < len(user.hand())-1: # detect if first of split hands
                print "Your first hand has 21 points. Switching to split hand"
                split_hand  = 1
                continue
            else: # The last (maybe only) hand has 21, end player action
                print "You have 21 points on your%shand. "\
                      "Dealer plays now." % (hand)
                return 0

        elif user.value()[split_hand] > 21:

            # Check if current hand is first of two hands.
            if split_hand < len(user.hand())-1:
                print "Your first hand has busted. Switching to split hand"
                split_hand  = 1 # Switch to split hand on future loops
                continue

            else: #  The last (maybe only) hand has busted, end player action
                print "You have busted on your%shand. Dealer plays now" % (hand)
                return 0

        # Check if split is valid, need the face to match and have enough chips
        if user.hand()[0][0][0] is user.hand()[0][1][0] and \
           user.bank() >= bet and \
           len(user.hand()) is 1:
            # Conditions for split met.
            action = raw_input("Would you like to Stand, Hit, or Split? ")

            # Check player input. Split and Stand start with S so we check full
            # words after striping white space and converting to lower case
            if action.lower().strip() == 'stand':
                header("You have chosen to stand.")
                return 0 # Player has chosen to stand, end player action.
            elif action.lower().strip() == 'hit':
                user.hit(0)
                print_screen("You have hit.")
                continue
            elif action.lower().strip() == 'split':
                # We should have already validated the condition for split, but
                # check one last time.
                if user.split(bet) < 0:
                    print "You can't split right now."
                    continue
                print_screen("Splitting...")
                continue # Split now loop again on the first hand.
            else:
                print "I'm sorry, I didn't understand you."
                continue # Input not understood, loop back for new input



        # Ask for the user action, auto deal with split hands
        action = raw_input("Would you like to Stand or Hit on your%shand"\
                           "? (H/S): " % (hand))

        # Handle Standing: If first split hand, switch hands.
        if action.lower().strip()[0] is 's':
            if split_hand < len(user.hand())-1:
                print "You have chosen to stand your first hand. "\
                      "Switching to second hand."
                split_hand  = 1
                continue
            else:
                print "You have chosen to stand on your%shand. "\
                      "Dealer plays now." % (hand)
                return 0 # standed on last hand, return to new_deal

        # Handle Hitting on current hand
        elif action.lower().strip()[0] is 'h':
            user.hit(split_hand)
            print_screen("Hitting on your%shand." % (hand))

        # Input didn't hit any of our actions, repeat the loop.
        else:
            print "I'm sorry, I didn't understand you."
            continue


def dealer_actions(bet):
    """Handles the dealer actions. Dealer hits to 17 unless player has busted
    on all hands."""
    global user
    global comp

    # Store the players score, but busts are stored as 0
    user_score = map(lambda x: 0 if x >21 else x, user.value())

    # Deal the 2nd card to the dealer.
    comp.hit(0)
    print_screen("Dealer's play now")
    print "Dealer deciding..."
    sleep(1)
    # While the dealer has less than 18 points, hit
    while comp.value()[0] < 17 and sum(user_score) >0:
        comp.hit(0)
        print_screen("Dealer Hits")
        print "Dealer deciding..."
        sleep(0.7) # slight pause to see what is going on.

    print_screen("Dealer Stays.")
    print "End of Round: Computing scores"

def end_of_round(bet):
    'Handles the end of the round scoring and handles bets paying back'

    global user
    global comp

    clear_line()
    # Store the score, but busts are stored as 0
    user_score = map(lambda x: 0 if x >21 else x, user.value())
    comp_score = 0 if comp.value()[0] > 21 else comp.value()[0]

    # Handle each hand to see if it won
    for i in range(0,len(user.hand())):

        # Setup the hand variable for easier printing later.
        if len(user.hand()) == 2:
            hand = ' first ' if i == 0 else ' split '
        else:
            hand = ' '

        if user_score[i] > comp_score: # if score beats dealer, this hand one
            print ("Your%shand beat the dealer." % (hand)),
            # If we have 21 points and only two cards, blackjack. Pays 3:2
            if user_score[i] == 21 and len(user.hand()[i]) == 2:
                user.win(int(bet*3.5))
                print "BLACKJACK You win %d chips" %(int(bet*3.5))
            else: # otherwise pay straight
                user.win(2*bet)
                print "You win %d chips" % (int(bet*2))
        # Check if we scored a blackjack without the dealer having blackjack
        # but the dealer does have 21 points.
        elif user_score[i] == 21 and\
                len(user.hand()[i]) == 2 and\
                len(comp.hand()[0]) > 2:
            user.win(int(bet*3.5))
            print "Your%shand beat the dealer. BLACKJACK. You win %d chips"\
                    % (hand,int(bet*3.5))
        else: # if we tie, even with a tied blackjack, you lose.
             print "Your%shand lost to the dealer" % (hand)
    clear_line()


def print_screen(message):
    global user
    global comp

    header(message)
    print "The dealer hand (%s): %s\n" % \
                (str(comp.value()[0]).rjust(2),fancy_print(comp.hand()[0]))
    if len(user.hand()) is 2:
        print "Your first hand is (%s): %s" % \
                (str(user.value()[0]).rjust(2),fancy_print(user.hand()[0]))
        print "Your split hand is (%s): %s\n" % \
                (str(user.value()[1]).rjust(2),fancy_print(user.hand()[1]))
    else:
        print "Your hand is (%s):    %s\n" % \
                (str(user.value()[0]).rjust(2),fancy_print(user.hand()[0]))
    clear_line()

def header(message):
    'Prints a message between two bars'
    print ''
    print '--------------------------------------------------------------------'
    print message
    print '--------------------------------------------------------------------'
    print ''

def clear_line():
    'Prints a break bar to help see what is going on'
    print "--------------------------------------------------------------------"
    print ""


def fancy_print(hand):
    string = ""
    for card in hand:
        string += "%s of %s, " % (card[0],card[2])
    string = "\n                      ".join(wrap(string[:-2],43))
    return string


if __name__ == "__main__":
    main()



