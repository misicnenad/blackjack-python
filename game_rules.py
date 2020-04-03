from deck import Deck
from cards.card import Card
from cards.card_rank import CardRank
from cards.card_suit import CardSuit
from players.dealer import Dealer


class GameRules():

    _card_max_value = 10
    _ace_max_value = 11
    _minimum_cards_in_hand = 2
    _winning_value = 21
    _minimum_budget = 100
    _dealer_min_stop_drawing_value = 17
    _blackjack_card_count = 2

    _blackjack_payout_ratio = (3, 2)
    _push_payout = (1, 1)
    _default_payout_ratio = (2, 1)
    _player_bust_payout = 0

    def __init__(self):
        card_rank_values = self._init_card_rank_values()
        cards = self._init_cards(card_rank_values)
        self.deck = Deck(cards)

    def _init_card_rank_values(self):
        rank_values = {rank: [rank.value] if rank.value <
                       CardRank.JACK.value else [self._card_max_value] for rank in CardRank}

        ace_card_values = [values for rank,
                           values in rank_values.items() if rank == CardRank.ACE]
        for values in ace_card_values:
            values.append(self._ace_max_value)

        return rank_values

    def _init_cards(self, card_rank_values):
        cards = []

        for suit in CardSuit:
            for rank, values in card_rank_values.items():
                card = Card(suit, rank, values)
                cards.append(card)

        return cards

    def get_playing_deck(self):
        return self.deck

    def get_minimum_budget(self):
        return self._minimum_budget

    def valid_initial_hand(self, hand):
        return len(hand.get_cards()) == self._minimum_cards_in_hand

    def card_face_down_check(self, participant):
        return isinstance(participant, Dealer) and not participant.get_hand().get_cards()

    def valid_value(self, value):
        return value <= self._winning_value

    def dealer_should_draw(self, dealer):
        total = dealer.get_current_total()
        if total < self._dealer_min_stop_drawing_value:
            return True

        hand = dealer.get_hand()
        return self.soft(hand) and total == self._dealer_min_stop_drawing_value

    def soft(self, hand):
        return any(c.get_rank() == CardRank.ACE for c in hand.get_cards())
        
    def get_payout(self, player_hand, dealer_hand):
        player_total = player_hand.get_current_total()
        dealer_total = dealer_hand.get_current_total()
        payout_ratio_type = self._default_payout_ratio

        if not self.valid_value(dealer_total):
            if self.blackjack(player_hand):
                payout_ratio_type = self._blackjack_payout_ratio

        if player_total < dealer_total:
            return self._player_bust_payout

        if player_total == dealer_total:
            payout_ratio_type = self._push_payout

        return self._convert_to_payout(player_total, payout_ratio_type)
    
    def _convert_to_payout(self, amount, payout_ratio):
        return (amount / payout_ratio[1]) * payout_ratio[0]

    def blackjack(self, hand):
        cards = hand.get_cards()
        if len(cards) != self._blackjack_card_count or hand.get_current_total() != self._winning_value:
            return False

        ace = next((c.get_rank() == CardRank.ACE for c in cards), None)
        ten_value_card = next((c.get_values()[0] == CardRank.TEN.value for c in cards), None)
        return ace and ten_value_card

    def winning_value(self, value):
        return value == self._winning_value
