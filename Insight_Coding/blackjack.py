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

    def value(self):
        value = sum(i[1] for i in self.deck[self.dealt:])
        return value


class dealer:
    """Implements the base player class as the dealer, keeps track of hand.
    Functions have support for splitting for the player child class to extend"""
    
    def __init__(self,deck):
        'Initialize the dealer: Deal one card to the hand'
        self.deck = deck
        self.cards = [self.deck.deal(1),]

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
    
    def chips(self):
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
        return (self.cards,self.chips)


