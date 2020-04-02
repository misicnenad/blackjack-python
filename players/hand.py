import itertools
from cards.card import Card, CardRank, CardSuit


class Hand():

    def __init__(self):
        self.cards = []
        self.bet = 0

    def add_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def get_values(self):
        if any(not c.get_values() for c in self.cards):
            return []
        value_lengths = [len(card.get_values()) for card in self.cards]
        num_of_sums = 1
        for vl in value_lengths:
            num_of_sums *= vl
        card_values = list(map(lambda c: c.get_values(), self.cards))

        return set(map(sum, itertools.product(*card_values)))

    def add_bet(self, bet):
        self.bet = bet

    def get_bet(self):
        return self.bet
