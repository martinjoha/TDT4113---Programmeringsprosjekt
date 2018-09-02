from Spiller import *
from Action import *
from random import randint as rn

class Historian(Spiller):


    def __init__(self, name, number):
        super().__init__(self,name)
        self.number = number

    #Sjekker først om historien til motspiller er lang nok til å kunne danne noe grunnlag for historien.
    # Hvis ikke velger den random trekk
    #Deretter lager jeg en liste med subsekvensen vi er inne i nå.
    #Lager også en liste for frekvens av trekk som kommer etter den subsekvensen vi nå er i
    #Iterer derfor baklengs for å finne ut om det er noen like subsekvenser av den jeg startet med
    #Hvis det er sånn legger jeg til indeksen av det neste trekket til listen frequency

    def velg_aksjon(self, motspiller):
        if len(Spiller.history[motspiller]) < self.number:
            return Action(rn(0,2))
        sub_sequence = Spiller.history[motspiller][- self.number:]
        frequency = [0, 0, 0]
        for i in range(len(Spiller.history[motspiller]) - self.number - 1, 0, -1):
            if Spiller.history[motspiller][i: i + self.number] == sub_sequence:
                frequency[Action.get_index(Spiller.history[motspiller][i + self.number + 1])] += 1
        if max(frequency) == 0:
            return Action(rn(0,2))
        else:
            return self.best_move(self.moves[frequency.index(max(frequency))])
