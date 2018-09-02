from Action import *
from Spiller import *

from random import randint as rn

class Random(Spiller):

#Velger tilfeldig hvilket trekk som velges

    def velg_aksjon(self):
        return Action(rn(0, 2))
