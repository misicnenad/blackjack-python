from enum import Enum
from players.hand import Hand
from players.dealer import Dealer, Player


class Status(Enum):
    PLAYING = 1
    WON = 2
    BUST = 3


class BlackjackGame():

    _dealer_already_added_exception_descr = "Dealer already added"

    def __init__(self, game_rules, dealer, players):
        self.game_rules = game_rules
        self.last_player_played_index = -1
        self.dealer_status_tuple = (dealer, Status.PLAYING)
        self.players = [(player, Status.PLAYING) for player in players]

        dealer.add_game(self)
        for p, _ in self.players:
            p.add_game(self)

    def remove_player(self, player):
        to_remove = next(item for item in self.players if player.name == item[0].name)
        self.players.remove(to_remove)

    def hands_initialized(self):
        return (all(self.game_rules.valid_initial_hand(p.get_hand()) for p, _ in self.players)
                and self.game_rules.valid_initial_hand(self.dealer_status_tuple[0].get_hand()))

    def deal_card_in_order(self):
        players = [p for p, _ in self.players]
        participants = players + [self.dealer_status_tuple[0]]
        num_of_players = len(participants)
        next_player_index = (
            self.last_player_played_index + 1) % num_of_players
        self.last_player_played_index = next_player_index

        next_player = participants[next_player_index]

        card = self.dealer_status_tuple[0].get_card()
        if self.game_rules.card_face_down_check(next_player):
            card.set_face_down()
        next_player.add_card(card)

    def get_state_description(self):
        dealer_descr = str(self.dealer_status_tuple[0]) + '. Status: ' + str(self.dealer_status_tuple[1])
        players_descr = '\n'.join(map(lambda tup: str(tup[0]) + '. Status: ' + str(tup[1]), self.players))
        return f'Players:\n{dealer_descr}\n{players_descr}\n'

    def deal_initial_hands(self):
        while not self.hands_initialized():
            self.deal_card_in_order()

    def play(self):
        print(self.get_state_description())

        for player, _ in self.players:
            player.place_bet()
            print(self.get_state_description())

        self.deal_initial_hands()

        print(self.get_state_description())

        for i, (player, _) in enumerate(self.players):
            while player.needs_card():
                card = self.dealer_status_tuple[0].get_card()
                player.add_card(card)
                value = player.get_current_total()
                if not self.game_rules.valid_value(value):
                    print(f'{player} busts! Total value: {value}')
                    status = Status.BUST

