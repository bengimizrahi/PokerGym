from poker_core import *
import itertools

def printTable(hands, communityCards):
    communityCardsStr = " ".join((str(c) for c in communityCards))
    print("""\033c
                       N: {}

                        {}
W: {}                                         E: {}

                       S: {}""".format(hands[1], communityCardsStr, hands[0], hands[2], hands[3]))


def playOmaha():
    deck = Deck(ranks=filter(lambda r: r >= Seven, Ranks))
    deck = deck.shuffle()
    hands = [Hand(cards, faceUp=True) for cards in deck.deal(4, 4)]
    hands[-1].turnFaceUp()
    deck.draw()
    communityCards = deck.draw(3, faceUp=True)
    
    printTable(hands, communityCards)
    input()

    communityCards.extend(deck.draw(1, faceUp=True))
    printTable(hands, communityCards)
    input()

    communityCards.extend(deck.draw(1, faceUp=True))
    printTable(hands, communityCards)
    input()

    for h in hands:
        h.turnFaceUp()
    printTable(hands, communityCards)
    
    
    result = []
    for pl, h in zip(("W", "N", "E", "S"), hands):
        allCombinations = []
        for p1, p2 in ((2, 3), (1, 4), (0, 5)):
            for twoCards in itertools.combinations(h.cards, p1):
                for threeCards in itertools.combinations(communityCards, p2):
                    allCombinations.append(Hand(list(twoCards + threeCards), faceUp=True))
        best = max((Ranking(hh) for hh in allCombinations))
        result.append((pl, h, best))
    
    sortedResult = sorted(result, key=lambda e: e[2], reverse=True)
    print()
    for sr in sortedResult:
        print(sr)
    input()

if __name__ == "__main__":
    while True:
        playOmaha()




