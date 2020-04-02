from blackjack_game import BlackjackGame, Dealer, Player
from game_rules import GameRules


if __name__ == "__main__":
    rules = GameRules()

    dealer = Dealer(rules)

    number_of_players = int(input("Please input the number of players: "))
    players = list(map(lambda n: Player(f'Player {n}', rules),
                       range(1, number_of_players + 1)))

    game = BlackjackGame(rules, dealer, players)

    game.play()
