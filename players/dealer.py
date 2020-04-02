from .player import Player
from deck import Deck


class Dealer(Player):

    name = "Dealer"

    def __init__(self, game_rules):
        super(Dealer, self).__init__(self.name, game_rules, budget=0)
        self.playing_deck = game_rules.get_playing_deck()
        self.discard_deck = Deck()

    def __str__(self):
        if not self.hand.get_cards():
            return f'{self.name} hand empty'
        hand_descr = 'Hand'
        hand_descr += ': ' + ', '.join(str(card)
                                       for card in self.hand.get_cards())
        value_descr = self.get_current_total()

        return f'{hand_descr} = {value_descr}'

    def get_card(self):
        if not self.has_cards():
            self.refill_playing_deck()

        return self.playing_deck.get_card()

    def has_cards(self):
        return self.playing_deck.has_cards()

    def refill_playing_deck(self):
        self.playing_deck = self.discard_deck
        self.discard_deck = Deck()

    def discard_cards(self, cards):
        self.discard_deck.add_cards(cards)

    def place_bet(self):
        pass

    def needs_card(self):
        return False
