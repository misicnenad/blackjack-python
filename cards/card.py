from .card_suit import CardSuit
from .card_rank import CardRank


class Card():

    _face_down_descr = 'Face-down'

    def __init__(self, suit, rank, values, face_down=False):
        '''
        Create a Card. Expects a rank and card suit.
        '''
        self.suit = suit
        self.rank = rank
        self.values = values
        self.face_down = face_down

    def __str__(self):
        rank = self._rank_to_string()
        suit = self.suit.name.capitalize()
        descr = f'{rank} of {suit}' if not self.face_down else self._face_down_descr
        return descr

    def __hash__(self):
        values_hash = 1
        for value in self.values:
            values_hash ^= hash(value)
        return hash(self.suit) ^ hash(self.rank) ^ values_hash

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False

        return (self.suit == other.suit
                and self.rank == other.rank
                and set(self.values) == set(other.values))

    def _rank_to_string(self):
        if self.rank.value < CardRank.JACK.value and self.rank != CardRank.ACE:
            return self.rank.value

        return self.rank.name.capitalize()

    def set_face_up(self):
        self.face_down = False

    def set_face_down(self):
        self.face_down = True

    def get_values(self):
        return self.values if not self.face_down else []