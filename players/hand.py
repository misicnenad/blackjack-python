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
        card_values = filter(lambda cv: len(cv) > 0,
                             (map(lambda c: c.get_values(), self.cards)))
        return set(map(sum, itertools.product(*card_values)))

    def add_bet(self, bet):
        self.bet = bet

    def get_bet(self):
        return self.bet
