from enum import Enum
from players.hand import Hand
from players.dealer import Dealer, Player


class PlayerStatus(Enum):
    PLAYING = 1
    BEAT_THE_DEALER = 2
    BLACKJACK = 3
    TWENTY_ONE = 4
    BUST = 5
    BETTING = 6
    WAITING = 7


class BlackjackGame():

    _dealer_already_added_exception_descr = "Dealer already added"

    def __init__(self, game_rules, dealer, players):
        self.game_rules = game_rules
        self.last_player_played_index = -1
        self.dealer = dealer
        self.players_status_dict = {
            player: PlayerStatus.WAITING for player in players}

        dealer.add_game(self)
        for p in self.players_status_dict:
            p.add_game(self)

    def remove_player(self, player_to_remove):
        to_remove = next(
            player for player in self.players_status_dict if player_to_remove.name == player.name)
        self.players_status_dict.pop(to_remove)

    def hands_initialized(self):
        return (all(self.game_rules.valid_initial_hand(p.get_hand()) for p in self.players_status_dict)
                and self.game_rules.valid_initial_hand(self.dealer.get_hand()))

    def deal_card_in_order(self):
        players = list(self.players_status_dict.keys())
        participants = players + [self.dealer]
        num_of_players = len(participants)
        next_player_index = (
            self.last_player_played_index + 1) % num_of_players
        self.last_player_played_index = next_player_index

        next_player = participants[next_player_index]

        card = self.dealer.get_card()
        if self.game_rules.card_face_down_check(next_player):
            card.set_face_down()
        next_player.add_card(card)

    def get_state_description(self):
        dealer_descr = str(self.dealer)
        players_descr = '\n'.join(
            map(lambda player: str(player) + '. PlayerStatus: '
                + str(self.players_status_dict[player].name), self.players_status_dict))
        return f'Players:\n{dealer_descr}\n{players_descr}\n'

    def deal_initial_hands(self):
        while not self.hands_initialized():
            self.deal_card_in_order()

    def play(self):
        while self.players_status_dict:
            print(self.get_state_description())

            for player in self.players_status_dict:
                self.players_status_dict[player] = PlayerStatus.BETTING
                player.place_bet()
                print(self.get_state_description())
                self.players_status_dict[player] = PlayerStatus.PLAYING

            self.deal_initial_hands()

            for player in self.players_status_dict:
                player
                if self.game_rules.blackjack(player.get_hand()):
                    print(f'{player} has a Blackjack! Hand: {player.get_hand()}')
                    self.players_status_dict[player] = PlayerStatus.BLACKJACK
                    break

            print(self.get_state_description())

            for player in (p for p in self.players_status_dict if self.players_status_dict[p] == PlayerStatus.PLAYING):
                while player.needs_card():
                    card = self.dealer.get_card()
                    player.add_card(card)
                    value = player.get_current_total()
                    if not self.game_rules.valid_value(value):
                        print(f'{player.get_name()} busts! Total value: {value}')
                        self.players_status_dict[player] = PlayerStatus.BUST
                        break
                    if self.game_rules.winning_value(value):
                        print(
                            f'{player.get_name()} has a 21! Total value: {value}')
                        self.players_status_dict[player] = PlayerStatus.TWENTY_ONE
                        break

            self.dealer.reveal_hole_card()
            while self.dealer.needs_card():
                card = self.dealer.get_card()
                self.dealer.add_card(card)
                value = self.dealer.get_current_total()
                if not self.game_rules.valid_value(value):
                    print(f'{self.dealer.get_name()} busts! Total value: {value}')
                    break

            dealer_hand = self.dealer.get_hand()

            players_to_remove = []
            for player in self.players_status_dict:
                player_hand = player.get_hand()
                payout = self.game_rules.get_payout(player_hand, dealer_hand)
                player.modify_budget_by(payout)
                if not player.wants_to_play():
                    players_to_remove.append(player)
                    continue

            print(self.get_state_description())

            for player in players_to_remove:
                self.players_status_dict.pop(player)

            for player in self.players_status_dict:
                self.players_status_dict[player] = PlayerStatus.WAITING

        print('Game over')
