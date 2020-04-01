from players.hand import Hand
from players.dealer import Dealer


class BlackjackGame():

    _dealer_already_added_exception_descr = "Dealer already added"

    def __init__(self, game_rules):
        self.game_rules = game_rules
        self.players = []
        self.dealer = None

    def add_player(self, player):
        if not isinstance(player, Dealer):
            self.players.append(player)
        
        if self.dealer != None:
            raise Exception(self._dealer_already_added_exception_descr)
        self.dealer = player

    def remove_player(self, player):
        self.players.remove(player)

    def hands_initialized(self):
        participants = self.players + [self.dealer]
        return all(self.game_rules.valid_initial_hand(p.get_hand()) for p in participants)