class Hand():

    def __init__(self):
        self.cards = []
        self.bet = 0

    def add_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def add_bet(self, bet):
        self.bet = bet

    def get_bet(self):
        return self.bet