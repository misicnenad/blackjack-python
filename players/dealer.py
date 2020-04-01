from .player import Player
from deck import Deck


class Dealer(Player):

    def __init__(self, name, blackjack_game, game_rules):
        super(Dealer, self).__init__(name, blackjack_game, budget=0)
        self.playing_deck = game_rules.get_playing_deck()
        self.discard_deck = Deck()

    def __str__(self):
        hand_descr = 'Hand'
        cards_descr = ', '.join(card for card in self.hand.get_cards())
        return f'{hand_descr}: {cards_descr}'

    def deal_initial_hands(self):
        while self.playing_deck.has_cards() and not self.blackjack_game.hands_initialized():
            card = self.playing_deck.get_card()
            self.blackjack_game.deal_card(card)

        if not self.playing_deck.has_cards() and not self.blackjack_game.hands_initialized():
            self.refill_playing_deck()

    def refill_playing_deck(self):
        self.playing_deck = self.discard_deck
        self.discard_deck = Deck()

    def discard_cards(self, cards):
        self.discard_deck.add_cards(cards)

    def place_bet(self):
        pass

    def needs_card(self):
        return False
