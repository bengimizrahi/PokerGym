#define CATCH_CONFIG_MAIN

#include "poker.h"
#include "catch.hpp"
#include <iostream>

using namespace std;

SCENARIO("Card class works fine", "[Card-1]")
{
    stringstream s;
    s << Card(Card::Rank::Ace, Card::Suit::Clubs);
    REQUIRE(s.str() == "A♣");
    REQUIRE(Card(Card::Rank::King, Card::Suit::Clubs) < Card(Card::Rank::Ace, Card::Suit::Clubs));
    REQUIRE(Card(Card::Rank::King, Card::Suit::Clubs) < Card(Card::Rank::King, Card::Suit::Hearts));
    REQUIRE(Card(Card::Rank::King, Card::Suit::Hearts) == Card(Card::Rank::King, Card::Suit::Hearts));
}

SCENARIO("Ranking category calculation works fine", "[Ranking-1]")
{
    auto highCard = set<Card>{
        Card(Card::Rank::Ace, Card::Suit::Clubs),
        Card(Card::Rank::King, Card::Suit::Clubs),
        Card(Card::Rank::Nine, Card::Suit::Hearts),
        Card(Card::Rank::Seven, Card::Suit::Diamonds),
        Card(Card::Rank::Eight, Card::Suit::Clubs)};
    REQUIRE(Ranking(highCard).category() == Ranking::Category::HighCard);

    auto pair = set<Card>{
        Card(Card::Rank::Ace, Card::Suit::Clubs),
        Card(Card::Rank::Ace, Card::Suit::Diamonds),
        Card(Card::Rank::Nine, Card::Suit::Hearts),
        Card(Card::Rank::Seven, Card::Suit::Diamonds),
        Card(Card::Rank::King, Card::Suit::Clubs)};
    REQUIRE(Ranking(pair).category() == Ranking::Category::Pair);

    auto doublePair = set<Card>{
        Card(Card::Rank::Ace, Card::Suit::Clubs),
        Card(Card::Rank::Ace, Card::Suit::Diamonds),
        Card(Card::Rank::Nine, Card::Suit::Hearts),
        Card(Card::Rank::Nine, Card::Suit::Diamonds),
        Card(Card::Rank::Queen, Card::Suit::Clubs)};
    REQUIRE(Ranking(doublePair).category() == Ranking::Category::DoublePair);

    auto threeOfAKind = set<Card>{
        Card(Card::Rank::Nine, Card::Suit::Clubs),
        Card(Card::Rank::Ace, Card::Suit::Diamonds),
        Card(Card::Rank::Nine, Card::Suit::Hearts),
        Card(Card::Rank::Nine, Card::Suit::Diamonds),
        Card(Card::Rank::Queen, Card::Suit::Clubs)};
    REQUIRE(Ranking(threeOfAKind).category() == Ranking::Category::ThreeOfAKind);

    auto flush = set<Card>{
        Card(Card::Rank::Ace, Card::Suit::Spades),
        Card(Card::Rank::King, Card::Suit::Spades),
        Card(Card::Rank::Nine, Card::Suit::Spades),
        Card(Card::Rank::Seven, Card::Suit::Spades),
        Card(Card::Rank::Eight, Card::Suit::Spades)};
    REQUIRE(Ranking(flush).category() == Ranking::Category::Flush);

    auto straight = set<Card>{
        Card(Card::Rank::Ace, Card::Suit::Clubs),
        Card(Card::Rank::King, Card::Suit::Clubs),
        Card(Card::Rank::Queen, Card::Suit::Hearts),
        Card(Card::Rank::Jack, Card::Suit::Diamonds),
        Card(Card::Rank::Ten, Card::Suit::Clubs)};
    REQUIRE(Ranking(straight).category() == Ranking::Category::Straight);

    auto fullHouse = set<Card>{
        Card(Card::Rank::Queen, Card::Suit::Clubs),
        Card(Card::Rank::Queen, Card::Suit::Spades),
        Card(Card::Rank::Queen, Card::Suit::Hearts),
        Card(Card::Rank::Eight, Card::Suit::Diamonds),
        Card(Card::Rank::Eight, Card::Suit::Clubs)};
    REQUIRE(Ranking(fullHouse).category() == Ranking::Category::FullHouse);

    auto straightFlush = set<Card>{
        Card(Card::Rank::Ace, Card::Suit::Clubs),
        Card(Card::Rank::King, Card::Suit::Clubs),
        Card(Card::Rank::Queen, Card::Suit::Clubs),
        Card(Card::Rank::Jack, Card::Suit::Clubs),
        Card(Card::Rank::Ten, Card::Suit::Clubs)};
    REQUIRE(Ranking(straightFlush).category() == Ranking::Category::StraightFlush);

}

SCENARIO("Compare Rankings", "[Ranking-1]")
{
    GIVEN("QJ097 and KQJ07")
    {
        auto highCardQueen = set<Card>{
            Card(Card::Rank::Ten, Card::Suit::Clubs),
            Card(Card::Rank::Nine, Card::Suit::Hearts),
            Card(Card::Rank::Queen, Card::Suit::Clubs),
            Card(Card::Rank::Seven, Card::Suit::Diamonds),
            Card(Card::Rank::Jack, Card::Suit::Clubs)};
        auto highCardKing = set<Card>{
            Card(Card::Rank::Ten, Card::Suit::Clubs),
            Card(Card::Rank::King, Card::Suit::Hearts),
            Card(Card::Rank::Queen, Card::Suit::Clubs),
            Card(Card::Rank::Seven, Card::Suit::Diamonds),
            Card(Card::Rank::Jack, Card::Suit::Clubs)};
        
        THEN("QJ097 < KQJ07")
        {
            auto rankingOfHighCardQueen = Ranking(highCardQueen);
            auto rankingOfHighCardKing = Ranking(highCardKing);
            REQUIRE(rankingOfHighCardQueen.category() == Ranking::Category::HighCard);
            REQUIRE(rankingOfHighCardKing.category() == Ranking::Category::HighCard);
            REQUIRE(rankingOfHighCardQueen < rankingOfHighCardKing);
        }
    }

    GIVEN("KQJ07 and KQJ08")
    {
        auto highCardSeven = set<Card>{
            Card(Card::Rank::Ten, Card::Suit::Spades),
            Card(Card::Rank::King, Card::Suit::Spades),
            Card(Card::Rank::Queen, Card::Suit::Spades),
            Card(Card::Rank::Seven, Card::Suit::Spades),
            Card(Card::Rank::Jack, Card::Suit::Clubs)};
        auto highCardEight = set<Card>{
            Card(Card::Rank::Ten, Card::Suit::Clubs),
            Card(Card::Rank::King, Card::Suit::Clubs),
            Card(Card::Rank::Queen, Card::Suit::Clubs),
            Card(Card::Rank::Eight, Card::Suit::Diamonds),
            Card(Card::Rank::Jack, Card::Suit::Clubs)};
        
        THEN("KQJ07 and KQJ08")
        {
            auto rankingOfHighCardSeven = Ranking(highCardSeven);
            auto rankingOfHighCardEight = Ranking(highCardEight);
            REQUIRE(rankingOfHighCardSeven.category() == Ranking::Category::HighCard);
            REQUIRE(rankingOfHighCardEight.category() == Ranking::Category::HighCard);
            REQUIRE(rankingOfHighCardSeven < rankingOfHighCardEight);
        }
    }

}

SCENARIO("A game can be constructed", "[Game-1]")
{
    Card::Rank allRanks[] = {Card::Rank::Seven, Card::Rank::Eight, Card::Rank::Nine,
            Card::Rank::Ten, Card::Rank::Jack, Card::Rank::Queen, Card::Rank::King, Card::Rank::Ace};
    Card::Suit allSuits[] = {Card::Suit::Clubs, Card::Suit::Diamonds, Card::Suit::Hearts, Card::Suit::Spades};

    vector<Card> deck{};
    for (auto r : allRanks) {
        for (auto s : allSuits) {
            deck.push_back(Card(r, s));
        }
    }
    
    array<set<Card>, 4> hands;
    auto& south = hands[0], &west = hands[1], &north = hands[2], &east = hands[3];
    for (int i = 0; i < 5; ++i) {
        for (auto& h : hands) {
            h.insert(deck.back());
            deck.pop_back();
        }
    } 

    stringstream s;
    s << south << " " << west << " " << north << " " << east;
    REQUIRE(s.str() ==
        "10♠J♠Q♠K♠A♠"
        " 10\033[1;31m♥\033[0mJ\033[1;31m♥\033[0mQ\033[1;31m♥\033[0mK\033[1;31m♥\033[0mA\033[1;31m♥\033[0m"
        " 10\033[1;31m♦\033[0mJ\033[1;31m♦\033[0mQ\033[1;31m♦\033[0mK\033[1;31m♦\033[0mA\033[1;31m♦\033[0m"
        " 10♣J♣Q♣K♣A♣");
}