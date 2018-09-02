from random import randint as rn
from Action import *
from Spiller import *


class MostCommon(Spiller):

    def __init__(self,name):
        Spiller.__init__(self, name)

    def velg_aksjon(self, motspiller):
        if motspiller not in Spiller.history:
            return Action(rn(0,2))
        else:
            player_history = Spiller.history[motspiller]
            stein = player_history.count(Action(0))
            saks = player_history.count(Action(1))
            papir = player_history.count(Action(2))
            frequence = [stein, saks, papir]
            most_common = frequence.index(max(frequence))
            return Action(self.best_move(most_common))



