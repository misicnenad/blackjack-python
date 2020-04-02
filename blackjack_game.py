from players.hand import Hand
from players.dealer import Dealer, Player


class BlackjackGame():

    _dealer_already_added_exception_descr = "Dealer already added"

    def __init__(self, game_rules, dealer, players):
        self.game_rules = game_rules
        self.last_player_played_index = -1
        self.dealer = dealer
        self.players = players

        dealer.add_game(self)
        for p in self.players:
            p.add_game(self)

    def remove_player(self, player):
        self.players.remove(player)

    def hands_initialized(self):
        return (all(self.game_rules.valid_initial_hand(p.get_hand()) for p in self.players)
                and self.game_rules.valid_initial_hand(self.dealer.get_hand()))

    def deal_card(self, card):
        participants = self.players + [self.dealer]
        num_of_players = len(participants)
        next_player_index = (
            self.last_player_played_index + 1) % num_of_players
        self.last_player_played_index = next_player_index

        next_player = participants[next_player_index]

        if self.game_rules.card_face_down_check(next_player):
            card.set_face_down()
        next_player.add_card(card)

    def get_state_description(self):
        dealer_descr = str(self.dealer)
        players_descr = '\n'.join(map(lambda p: str(p), self.players))
        return f'Players:\n{dealer_descr}\n{players_descr}\n'

    def deal_initial_hands(self):
        while self.dealer.has_cards() and not self.hands_initialized():
            card = self.dealer.get_card()
            self.deal_card(card)

        if not self.dealer.has_cards() and not self.hands_initialized():
            self.dealer.refill_playing_deck()
            self.deal_initial_hands()

    def play(self):
        print(self.get_state_description())

        for player in self.players:
            player.place_bet()
            print(self.get_state_description())

        self.deal_initial_hands()

        print(self.get_state_description())

        # for player in self.players:
        #     while player.needs_card():
        #         dealer.deal_card()
