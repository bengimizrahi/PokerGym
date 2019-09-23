#include <iostream>
#include <string>
#include <set>
#include <array>
#include <algorithm>
#include <numeric>
#include <tuple>

class Card {
public:
    enum Rank {Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King, Ace, RankCount};
    enum Suit {Clubs, Diamonds, Hearts, Spades, SuitCount};

public:
    explicit Card(Rank rank, Suit suit)
     : rank_{rank}, suit_{suit}
    {
    }

public:
    auto rank() { return rank_; }
    auto suit() { return suit_; }

private:
    Rank rank_;
    Suit suit_;

    friend bool operator<(const Card& lhs, const Card& rhs)
    {
        return std::tie(lhs.rank_, lhs.suit_) < std::tie(rhs.rank_, rhs.suit_);
    }

    friend bool operator==(const Card& lhs, const Card& rhs)
    {
        return std::tie(lhs.rank_, lhs.suit_) == std::tie(rhs.rank_, rhs.suit_);
    }

    friend std::ostream& operator<<(std::ostream& out, const Card& card)
    {
        static std::string ranksRepr[] = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"};
        static std::string suitsRepr[] = {"\u2663", "\u2666", "\u2665", "\u2660"};
        out << ranksRepr[card.rank_];
        bool red = card.suit_ == Card::Suit::Diamonds || card.suit_ == Card::Suit::Hearts;
        if (red) {
            out << "\033[1;31m";
        }
        out << suitsRepr[card.suit_];
        if (red) {
            out << "\033[0m";
        }
        return out;
    }
};

class Ranking {
public:
    enum class Category {None, HighCard, Pair, DoublePair, ThreeOfAKind, Flush, Straight, FullHouse, FourOfAKind, StraightFlush};
public:
    Ranking(const std::set<Card>& cards)
     : category_{Category::None}
    {
        std::for_each(cards.begin(), cards.end(), [&](auto c) { ++(counts_[c.rank()]); });
        score_ = std::accumulate(counts_.rbegin(), counts_.rend(), 0ul,
                [](auto score, unsigned int c) { return (13 * score) + c; });
        auto result = std::accumulate(counts_.begin(), counts_.end(), 1,
                [](auto product, auto term) { return term ? product * term : product; });
        
        auto suits = std::accumulate(cards.begin(), cards.end(), std::set<Card::Suit>(),
                [](auto suits, auto card) { suits.insert(card.suit()); return suits; });
        auto first = std::find(counts_.begin(), counts_.end(), 1);
        auto last = std::find(counts_.rbegin(), counts_.rend(), 1);
        bool straight = std::distance(first, (last + 1).base()) == 4;
        bool flush = suits.size() == 1;
        
        switch (result) {
        case 1:
            if (straight && flush) { category_ = Category::StraightFlush; }
            else if (straight) { category_ = Category::Straight; }
            else if (flush) { category_ = Category::Flush; }
            else { category_ = Category::HighCard; }
            break;
        case 2:
            category_ = Category::Pair;
            break;
        case 4:
            if (std::find(counts_.begin(), counts_.end(), 4) != counts_.end()) {
                category_ = Category::FourOfAKind;
            }
            else {
                category_ = Category::DoublePair;
            }
            break;
        case 3:
            category_ = Category::ThreeOfAKind;
            break;
        case 6:
            category_ = Category::FullHouse;
            break;
        };
    }

public:
    auto category() { return category_; }

private:
    Category category_;
    std::array<unsigned int, Card::RankCount> counts_{};
    unsigned long int score_{0};

    friend bool operator<(const Ranking& lhs, const Ranking& rhs)
    {
        return lhs.category_ < rhs.category_ ||
                (lhs.category_ == rhs.category_ && lhs.score_ < rhs.score_);
    }
};

std::ostream& operator<<(std::ostream& out, const std::set<Card>& cards)
{
    for (auto c : cards) {
        out << c;
    }
    return out;
}