from Spiller import *
from Action import *
from random import randint as rn


class SingleGame():

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.p1 = 0
        self.p2 = 0

    def play_game(self):
        self.player1_action = self.player1.velg_aksjon(self.player2)
        self.player2_action = self.player2.velg_aksjon(self.player1)
        if self.get_winner() == self.player1:
            self.p1 += 1
        elif self.get_winner() == self.player2:
            self.p2 += 1
        else:
            self.p1 += 0.5
            self.p2 += 0.5

        self.player1.motta_resultat(self.player2, self.player2_action)
        self.player2.motta_restultat(self.player1, self.player1_action)

    def get_winner(self):
        if self.player1_action > self.player2_action:
            return self.player1
        elif self.player2_action > self.player1_action:
            return self.player2
        return 0

    def __str__(self):
        return str(self.player1) + ': ' + str(self.player1_action) + '. ' + str(self.player2) + ': '
        + str(self.player2_action) + '-->' + str(get_winner())


a = Random('hei')
b = Random('hoi')
c = SingleGame(a,b)
c.play_game()

