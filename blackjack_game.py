from players.hand import Hand
from players.dealer import Dealer, Player


class BlackjackGame():

    _dealer_already_added_exception_descr = "Dealer already added"

    def __init__(self, game_rules, participants):
        self.game_rules = game_rules
        self.last_participant_played_index = -1
        self.participants = participants

        for p in self.participants:
            p.add_game(self)

    def add_participant(self, participant):
        self.participants.append(participant)

    def remove_participant(self, participant):
        self.participants.remove(participant)

    def hands_initialized(self):
        return all(self.game_rules.valid_initial_hand(p.get_hand()) for p in self.participants)

    def deal_card(self, card):
        num_of_participants = len(self.participants)
        next_participant_index = (
            self.last_participant_played_index + 1) % num_of_participants
        self.last_participant_played_index = next_participant_index
        
        next_participant = self.participants[next_participant_index]
        
        if self.game_rules.card_face_down_check(next_participant):
            card.set_face_down()
        next_participant.add_card(card) 

    def get_state_description(self):
        players_descr = '\n'.join(map(lambda p: str(p), self.participants))
        return f'Participants:\n{players_descr}\n'

    def play(self):
        print(self.get_state_description())

        dealer = next(filter(lambda p: isinstance(p, Dealer), self.participants))   
        players = list(filter(lambda p: not isinstance(p, Dealer), self.participants))         

        for player in players:
            player.place_bet()
            print(self.get_state_description())

        dealer.deal_initial_hands()

        print(self.get_state_description())

