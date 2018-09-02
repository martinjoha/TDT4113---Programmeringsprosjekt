from Spiller import *
from Action import *


class Sequential(Spiller):

    #velger aksjon utifra hva det forrige var
    #stein, saks, papir, stein, saks, papir
    def __init__(self, name):
        super().__init__(self, name)
        self.current_number = 0

    def velg_aksjon(self):
        self.current_number = (self.current_number + 1) % 3
        return Action(self.current_number)

