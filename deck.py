from random import shuffle


class Deck():

    def __init__(self, cards = []):
        self.cards = cards
        shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()

    def add_cards(self, cards):
        self.cards.extend(cards)
        shuffle(self.cards)

    def has_cards(self):
        return bool(self.cards)

    def reshuffle_deck(self):
        shuffle(self.cards)
