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
        """Copy the deck of cards from the class variable., shuffle them,
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
    'Implements the base player class as the dealer, keeps track of hands'
    
    def __init__(self,deck):
        self.cards = deck.deal(1)

    def cheat(self,hand):
        'A function used for testing, allows for setting the hand'
        self.cards = hand

    def hand(self):
        'Returns the current hand'
        return self.cards

    def value(self):
        'Calculate the value of the hand, automatically handle aces'
        value = sum(i[1] for i in self.cards)
        
       """If any card is an ace, we check the total value of the hand, if the 
       hand has a value of less than 12, then we can add the addition value to 
       the hand. It is impossible for two aces to have a value of 11"""
        for i in self.cards:
            if i[0] == "Ace":
                if value < 12 and ace != 0:
                    value += 10 # Ace has already been counted for 1 point
        return value

    def hit(self,deck):
        """Implements hitting, deals a card from the passed in deck and returns
        the new hand"""
        self.cards.extend(deck.deal(1))
        return self.cards

    def new_deal(self.deck):
        self.cards = deck.deal(1)

class player(dealer):
    'Extends the dealer class to implement betting commands and track chips'

    def __init__(self,deck):
        self.cards = deck.deal(2)
        self.chips = 100

    def bet(self,bet):
        if bet > self.chips:
            return -1
        self.chips -= bet
        return self.chips
    
    def chips(self):
        return self.chips

    def new_deal(self.deck):
        self.cards = deck.deal(2)


