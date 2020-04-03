from .hand import Hand


class Player():

    _needs_card_descr = "{} receive another card? (y/n)\n"
    _bet_input_string = '{} how much do you bet? '
    _bet_again_descr = "Not enough money for the bet. Input bet again: "
    _not_enough_money_descr = "Not enough money\n"
    _play_again_descr = "{} continue playing? (y/n)\n"
    _exiting_game_descr = "{} exited game."
    _add_budget_descr = "How much to add to budget? Minimum budget is {}: "
    _min_budget_warning_descr = "Input more money. Minimum budget is {}"
    _min_budget = 100

    def __init__(self, name, game_rules, budget=None):
        self.name = name
        self.budget = budget if budget != None else game_rules.get_minimum_budget()
        self.game_rules = game_rules
        self.blackjack_game = None
        self.hand = Hand(game_rules)

    def __str__(self):
        if not self.hand.get_cards():
            return f'{self.name} hand empty'
        hand_descr = 'Hand'
        cards_descr = ', '.join(str(card) for card in self.hand.get_cards())
        bet_descr = f'Bet: {self.hand.get_bet()}'
        value_descr = self.get_current_total()

        return f'{hand_descr}: {cards_descr} = {value_descr}. {bet_descr}'

    def get_name(self):
        return self.name

    def add_game(self, game):
        self.blackjack_game = game

    def place_bet(self):
        print(f'{self.name}: your budget is {self.budget}.')
        if not self.budget:
            print(self._not_enough_money_descr)
            answer = input(self._play_again_descr.format(self.name))
            if answer != 'y':
                print(self._exiting_game_descr.format(self.name))
                self.blackjack_game.remove_player(self)
                pass
            self._input_budget()

        bet = self._input_bet()

        self.hand.add_bet(bet)
        self.budget -= bet

    def get_hand(self):
        return self.hand

    def get_current_total(self):
        return self.hand.get_current_total()

    def _input_bet(self):
        bet = int(input(self._bet_input_string))
        while bet > self.budget:
            print(self._bet_again_descr)
            bet = int(input(self._bet_input_string))

        return bet

    def get_bet(self):
        return self.hand.get_bet()

    def needs_card(self):
        answer = input(self._needs_card_descr.format(self.name))
        return answer == 'y'

    def _input_budget(self):
        budget = int(input(self._add_budget_descr.format(self._min_budget)))
        while budget < self._min_budget:
            print(self._min_budget_warning_descr.format(self._min_budget))
            budget = int(input(self._add_budget_descr.format(self._min_budget)))

        self.budget = budget

    def modify_budget_by(self, payout):
        self.budget += payout

    def add_card(self, card):
        self.hand.add_card(card)

    def reset_hand(self):
        self.hand = Hand(self.game_rules)

    def wants_to_play(self):
        return input(self._play_again_descr) == 'y'
