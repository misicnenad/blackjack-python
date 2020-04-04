import itertools
from decimal import Decimal
from cards.card import Card, CardRank, CardSuit


class Hand():

    def __init__(self, game_rules):
        self.game_rules = game_rules
        self.cards = []
        self.bet = Decimal(0)

    def __str__(self):
        if not self.get_cards():
            return f'Hand empty'
        hand_descr = 'Hand'
        cards_descr = ', '.join(str(card) for card in self.get_cards())
        bet = self.get_bet() if self.get_bet() > 0 else None
        bet_descr = f'Bet: {bet}'
        value_descr = self.get_current_total()

        return f'{hand_descr}: {cards_descr} = {value_descr}. {bet_descr}'

    def add_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def get_values(self):
        card_values = filter(lambda cv: len(cv) > 0,
                             (map(lambda c: c.get_values(), self.cards)))
        return set(map(sum, itertools.product(*card_values)))

    def get_current_total(self):
        all_values = self.get_values()
        valid_values = list(
            filter(lambda v: self.game_rules.valid_value(v), all_values))
        return min(all_values) if not valid_values else max(valid_values)

    def reveal_hole_card(self):
        for c in self.cards:
            c.set_face_up()

    def add_bet(self, bet):
        self.bet = bet

    def get_bet(self):
        return self.bet
