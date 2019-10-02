#!/usr/bin/python3

import functools
import random
import unittest
import re
import pdb

redColorEsc, defaultColorEsc = ("\033[1;31m", "\033[0m")

@functools.total_ordering
class Rank:
    reprToValue = dict(zip(("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"), range(2, 15)))
    valueToRepr = {v: k for k, v in reprToValue.items()}

    def __init__(self, rank):
        if type(rank) == int:
            if not (2 <= rank or rank < 15):
                raise ValueError("Invalid rank value: {}".format(rank))
            self.value = rank
        elif type(rank) == str:
            self.value = Rank.reprToValue[rank]
        else:
            raise ValueError("Invalid Rank value type: {}".format(type(rank)))
    
    def __ge__(self, rank):
        return self.value >= rank.value
 
    def __lt__(self, rank):
        return not (self >= rank)
    
    def __eq__(self, rank):
        return self.value == rank.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return Rank.valueToRepr[self.value]

    def __str__(self):
        return repr(self)

Ranks = Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King, Ace = [Rank(v) for v in range(2, 15)]

@functools.total_ordering
class Suit:
    reprToValue = dict(zip(("♣", "♦", "♠", "♥"), range(4)))
    valueToRepr = {v: k for k, v in reprToValue.items()}

    def __init__(self, suit):
        if type(suit) == int:
            if not (0 <= suit or suit < 4):
                raise ValueError("Invalid suit value: {}".format(suit))
            self.value = suit
        elif type(suit) == str:
            self.value = Suit.reprToValue[suit]
        else:
            raise ValueError("Invalid suit value: {}".format(suit))
    
    def __ge__(self, card):
        return self.value >= card.value

    def __lt__(self, suit):
        return not (self >= suit)
    
    def __eq__(self, suit):
        return self.value == suit.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return Suit.valueToRepr[self.value]
    
    def __str__(self):
        rpr = repr(self)
        return redColorEsc + rpr + defaultColorEsc if self.value % 2 else rpr

Suits = Clubs, Diamonds, Spades, Hearts = [Suit(v) for v in range(4)]

@functools.total_ordering
class Card:
    def __init__(self, *args):
        if len(args) == 2 and all(map(lambda p: type(p[0]) == p[1], zip(args, (Rank, Suit)))):
            self.rank, self.suit = args
        elif len(args) == 1 and (type(args[0]) == str):
            repr = args[0]
            if len(repr) == 2:
                self.rank, self.suit = Rank(repr[0]), Suit(repr[1])
            elif len(repr) == 3:
                self.rank, self.suit = Rank(repr[:2]), Suit(repr[2])
            else:
                raise ValueError("Invalid card: {}".format(repr))
        else:
            raise ValueError("Invalid card: {}".format(repr))
        self.faceUp = False

    def turnFaceUp(self):
        self.faceUp = True
    
    def turnFaceDown(self):
        self.faceUp = False

    def __ge__(self, card):
        return (self.rank, self.suit) >= (card.rank, card.suit)

    def __lt__(self, card):
        return not (self >= card)
    
    def __eq__(self, card):
        return (self.rank, self.suit) == (card.rank, card.suit)

    def __hash__(self):
        return hash(self.rank, self.suit)

    def __repr__(self):
        return "{}{}".format(repr(self.rank), repr(self.suit))
    
    def __str__(self):
        return "{}{}".format(str(self.rank), str(self.suit)) if self.faceUp else "##"

class Hand:
    def __init__(self, reprOrCards, faceUp = False):
        if type(reprOrCards) == str:
            self.cards = [Card(r) for r in reprOrCards.split("-")]
        elif type(reprOrCards) == list and all((lambda c: type(c) == Card, reprOrCards)):
            self.cards = reprOrCards
        else:
            raise ValueError("Invalid hand: {}".format(repr))
        if not faceUp:
            self.turnFaceDown()
        else:
            self.turnFaceUp()

    def turnFaceUp(self):
        for c in self.cards:
            c.turnFaceUp()
    
    def turnFaceDown(self):
        for c in self.cards:
            c.turnFaceDown()

    def __repr__(self):
        return "-".join((repr(c) for c in self.cards))

    def __str__(self):
        return " ".join((str(c) for c in self.cards))

@functools.total_ordering
class Ranking:
    HighCard, Pair, DoublePair, ThreeOfAKing, Flush, Straight, FullHouse, FourOfAKing, StraightFlush = range(9)

    def __init__(self, hand):
        self.hand = hand
        ranks = [h.rank for h in hand.cards]
        self.counts = [ranks.count(r) for r in Ranks]
        histogram = sorted(filter(lambda c: c > 0, self.counts))
        if histogram == [1, 1, 1, 1, 1]:
            firstIndex = self.counts.index(1)
            lastIndex = 13 - self.counts[::-1].index(1)
            atLeastStraight = (lastIndex - firstIndex) == 5
            atLeastFlush = len(set((c.suit for c in hand.cards))) == 1
            self.category = {(False, False): self.HighCard,
                             (True, False): self.Straight,
                             (False, True): self.Flush,
                             (True, True): self.StraightFlush}[(atLeastStraight, atLeastFlush)]            
        elif histogram == [1, 1, 1, 2]:
            self.category = self.Pair
        elif histogram == [1, 2, 2]:
            self.category = self.DoublePair
        elif histogram == [1, 1, 3]:
            self.category = self.ThreeOfAKing
        elif histogram == [2, 3]:
            self.category = self.FullHouse
        elif histogram == [1, 4]:
            self.category = self.FourOfAKing
        else:
            raise ValueError("Invalid hand: {}".format(hand))
    
    def __lt__(self, ranking):
        if self.category != ranking.category:
            return self.category < ranking.category
        else:
            return self.counts > ranking.counts

    def __ge__(self, ranking):
        return not (self < ranking)
    
    def __repr__(self):
        repr = "HighCard", "Pair", "DoublePair", "ThreeOfAKing", "Flush", "Straight", "FullHouse", "FourOfAKing", "StraightFlush"
        return "Ranking({}, {}, {})".format(self.hand, repr[self.category], "".join(map(str, self.counts)))

class Deck:
    def __init__(self, ranks = Ranks, suits = Suits):
        self.cards = [Card(r, s) for r in ranks for s in suits]

    def draw(self, numberOfCards = 1, faceUp=False):
        if numberOfCards > len(self.cards):
            raise RuntimeError("Cannot draw {} cards from a deck of {} cards".format(numberOfCards, len(self.cards)))
        drawnCards = [self.cards.pop() for i in range(numberOfCards)]
        for c in drawnCards:
            if faceUp:
                c.turnFaceUp()
            else:
                c.turnFaceDown()
        return drawnCards

    def shuffle(self):
        random.shuffle(self.cards)
        return self

    def deal(self, numberOfCardsPerHand, numberOfHands):
        hands = [[] for i in range(numberOfHands)]
        for i in range(numberOfCardsPerHand):
            for j in range(numberOfHands):
                hands[j].extend(self.draw())
        return hands

    def __repr__(self):
        return repr(self.cards)

    def __str__(self):
        return str(self.cards)    

class TestCard(unittest.TestCase):
    def testRank(self):
        self.assertEqual(repr(Jack), "J")
        self.assertGreaterEqual(Jack, Ten)
        self.assertEqual(King, King)
    def testSuit(self):
        self.assertEqual(repr(Hearts), "♥")
        self.assertGreaterEqual(Hearts, Clubs)
        self.assertEqual(Diamonds, Diamonds)
    def testCard(self):
        self.assertEqual(repr(Card(Jack, Hearts)), "J♥")
        self.assertEqual(repr(Card("10♥")), "10♥")
        self.assertGreaterEqual(Card(Jack, Clubs), Card(Ten, Clubs))
        self.assertGreaterEqual(Card(Jack, Diamonds), Card(Ten, Clubs))
        self.assertEqual(Card(Ten, Clubs), Card(Ten, Clubs))

class TestHand(unittest.TestCase):
    def testHand(self):
        self.assertEqual(repr(Hand("A♥-K♠-2♦-5♣-Q♥")), "A♥-K♠-2♦-5♣-Q♥")

class TestRanking(unittest.TestCase):
    def testRanking(self):
        self.assertEqual(Ranking(Hand("A♥-K♠-2♦-5♣-Q♥", True)).category, Ranking.HighCard)
        self.assertEqual(Ranking(Hand("A♥-A♠-2♦-5♣-Q♥", True)).category, Ranking.Pair)
        self.assertEqual(Ranking(Hand("A♥-A♠-2♦-2♣-Q♥", True)).category, Ranking.DoublePair)
        self.assertEqual(Ranking(Hand("A♥-A♠-A♦-5♣-Q♥", True)).category, Ranking.ThreeOfAKing)
        self.assertEqual(Ranking(Hand("A♥-K♠-Q♦-J♣-10♥", True)).category, Ranking.Straight)
        self.assertEqual(Ranking(Hand("A♥-A♠-A♦-J♣-J♥", True)).category, Ranking.FullHouse)
        self.assertEqual(Ranking(Hand("A♥-A♠-A♦-A♣-10♥", True)).category, Ranking.FourOfAKing)
        self.assertEqual(Ranking(Hand("A♥-K♥-Q♥-J♥-10♥", True)).category, Ranking.StraightFlush)
        self.assertLess(Ranking(Hand("Q♥-J♠-10♦-9♣-7♥", True)), Ranking(Hand("Q♦-J♠-10♦-9♣-8♥", True)))
        self.assertLess(Ranking(Hand("J♥-J♠-10♦-9♣-7♥", True)), Ranking(Hand("Q♦-Q♠-10♦-9♣-8♥", True)))
        self.assertLess(Ranking(Hand("J♥-J♠-10♦-9♣-7♥", True)), Ranking(Hand("J♦-J♣-10♦-9♣-8♥", True)))
        self.assertLess(Ranking(Hand("J♥-J♠-J♦-9♣-7♥", True)), Ranking(Hand("J♥-J♠-J♦-10♣-7♥", True)))
        self.assertLess(Ranking(Hand("7♦-7♠-7♣-J♣-J♥", True)), Ranking(Hand("8♥-8♦-8♠-7♠-7♣", True)))

class TestDeck(unittest.TestCase):
    def testDeck(self):
        self.assertEqual(repr(Deck()), "[2♣, 2♦, 2♠, 2♥, 3♣, 3♦, 3♠, 3♥, 4♣, 4♦, 4♠, 4♥, 5♣, 5♦, 5♠, 5♥, 6♣, 6♦, 6♠, 6♥, 7♣, 7♦, 7♠, 7♥, 8♣, 8♦, 8♠, 8♥, 9♣, 9♦, 9♠, 9♥, 10♣, 10♦, 10♠, 10♥, J♣, J♦, J♠, J♥, Q♣, Q♦, Q♠, Q♥, K♣, K♦, K♠, K♥, A♣, A♦, A♠, A♥]")
        self.assertNotEqual(repr(Deck().shuffle()), repr(Deck()))
        self.assertEqual(repr(Deck().draw()), repr([Card(Ace, Hearts)]))
        self.assertEqual(repr(Deck().draw(2)), repr([Card(Ace, Hearts), Card(Ace, Spades)]))
        self.assertEqual(repr(Deck().deal(5, 4)), "[[A♥, K♥, Q♥, J♥, 10♥], [A♠, K♠, Q♠, J♠, 10♠], [A♦, K♦, Q♦, J♦, 10♦], [A♣, K♣, Q♣, J♣, 10♣]]")

if __name__ == "__main__":
    unittest.main()