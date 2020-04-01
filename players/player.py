from .hand import Hand


class Player():

    _needs_card_descr = "Receive another card? (y/n)\n"
    _bet_input_string = 'How much do you bet? '
    _bet_again_descr = "Not enough money for the bet. Input bet again: "
    _play_again_descr = "Not enough money. Continue playing? (y/n)\n"
    _exiting_game_descr = "Player {} exited game."
    _add_budget_descr = "How much to add to budget? Minimum budget is {}: "
    _min_budget_warning_descr = "Input more money. Minimum budget is {}"
    _min_budget = 100

    def __init__(self, name, blackjack_game, budget=_min_budget):
        self.name = name
        self.budget = budget
        self.blackjack_game = blackjack_game

        self.hand = Hand()
        self.blackjack_game.add_player(self)

    def __str__(self):
        hand_descr = 'Hand'
        cards_descr = ', '.join(card for card in self.hand.get_cards())
        bet_descr = f'Bet: {self.hand.get_bet()}'
        return f'{hand_descr}: {cards_descr}. {bet_descr}'

    def place_bet(self):
        print(f'Player {self.name}: your budget is {self.budget}.')
        if not self.budget:
            answer = input(self._play_again_descr)
            if answer != 'y':
                print(self._exiting_game_descr.format(self.name))
                self.blackjack_game.remove_player(self)
                pass
            self._add_budget()

        bet = self._get_bet()

        self.hand.add_bet(bet)
        self.budget -= bet

    def get_hand(self):
        return self.hand

    def _get_bet(self):
        bet = int(input(self._bet_input_string))
        while bet > self.budget:
            print(self._bet_again_descr)
            bet = int(input(self._bet_input_string))

        return bet

    def needs_card(self):
        answer = input(self._needs_card_descr)
        return answer == 'y'

    def _add_budget(self):
        budget = int(input(self._add_budget_descr.format(self._min_budget)))
        if budget < self._min_budget:
            print(self._min_budget_warning_descr.format(self._min_budget))
            self._add_budget()

        self.budget = budget 
