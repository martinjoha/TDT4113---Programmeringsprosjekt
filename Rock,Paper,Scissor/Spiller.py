from Action import *
from random import randint as rn
import matplotlib.pyplot as plt


class Spiller:

    moves = ['stein','saks','papir']
    history = {}

    def __init__(self, name):
        self.name = name
        Spiller.history[self] = []

    # skal velge hvilket trekk spiller skal ta. Denne endrer seg etter hvilken type spiller det er.

    def velg_aksjon(self):
        return

    def get_player_history(self, player):
        return self.history[player]

    # mottar resultatet av et spill, og legger til trekket for motspiller til history
    def motta_resultat(self, opponent, trekk):
        Spiller.history[opponent].append(trekk)

    def oppgi_navn(self):
        return self.name

    # toString fra java
    def __str__(self):
        return self.name

    def best_move(self, move):
        a = {1: 0, 2: 1, 0: 2}
        return Action(a[move])


#         NY KLASSE #######
class Sequential(Spiller):

    # velger aksjon utifra hva det forrige var
    # stein, saks, papir, stein, saks, papir
    def __init__(self, name):
        super().__init__(name)
        self.current_number = 0

    def velg_aksjon(self, opponent):
        self.current_number = (self.current_number + 1) % 3
        return Action(self.current_number)


# ####### NY KLASSE ######
class Random(Spiller):

    def velg_aksjon(self, opponent):
        return Action(rn(0, 2))


# ###### NY KLASSE ######
class MostCommon(Spiller):

    def __init__(self, name):
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
            return self.best_move(most_common)


# ###### NY KLASSE ######
class Historian(Spiller):

    def __init__(self, name, number):
        super().__init__(name)
        self.number = number

    # Sjekker først om historien til motspiller er lang nok til å kunne danne noe grunnlag for historien.
    # Hvis ikke velger den random trekk
    # Deretter lager jeg en liste med subsekvensen vi er inne i nå.
    # Lager også en liste for frekvens av trekk som kommer etter den subsekvensen vi nå er i
    # Iterer derfor baklengs for å finne ut om det er noen like subsekvenser av den jeg startet med
    # Hvis det er sånn legger jeg til indeksen av det neste trekket til listen frequency

    def velg_aksjon(self, motspiller):
        if len(Spiller.history[motspiller]) < self.number:
            return Action(rn(0,2))
        sub_sequence = Spiller.history[motspiller][- self.number:]
        player_history = self.get_player_history(motspiller)
        frequency = [0, 0, 0]
        for i in range(len(player_history) - self.number - 2, 0, -1):
            if Spiller.history[motspiller][i: i + self.number] == sub_sequence:
                move = player_history[i + self.number]
                frequency[move.get_num()] += 1
        if max(frequency) < 1:
            return Action(rn(0,2))
        else:
            return self.best_move(frequency.index(max(frequency)))


# #### NY KLASSE #####
class SingleGame:

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
        self.player2.motta_resultat(self.player1, self.player1_action)

    def get_winner(self):
        if self.player1_action > self.player2_action:
            return self.player1
        elif self.player2_action > self.player1_action:
            return self.player2
        return 0

    def __str__(self):
        return str(self.player1) + ': ' + str(self.player1_action) + '. ' + str(self.player2) + ': ' + \
               str(self.player2_action) + '--> ' + str(self.get_winner())


class Tournament:

    def __init__(self, p1, p2, games):
        self.p1 = p1
        self.p2 = p2
        self.games = games
        self.p1_points = 0
        self.p2_points = 0

    def single_game(self):
        a = SingleGame(self.p1, self.p2)
        a.play_game()
        if a.get_winner() == 0:
            self.p1_points += 0.5
            self.p2_points += 0.5
        elif a.get_winner() == self.p1:
            self.p1_points += 1
        else:
            self.p2_points += 1
        return str(a)

    def multiple_games(self):
        win_percentage = []
        games = 0
        for i in range(self.games):
            self.single_game()
            p1_win = self.p1_points / (self.p1_points + self.p2_points)
            win_percentage.append(p1_win)
            games += 1

        #print("Spiller 1 vant " + str((win_percentage[-1])*100) + '% av kampene, og spiller 2 vant ' + str((1-p1_win)*100) + '% av kampene')

        plt.ylabel('win percentage')
        plt.xlabel('games played')
        plt.ylim(0, 1)
        plt.plot(win_percentage)
        plt.show()




def main():

    player1 = None
    player2 = None
    name1 = input("Hva heter du?")
    type1 = int(input("Hvordan spiller vil du være? \n1: random \n2: Sekvensiell \n3: Mest Vanlig \n4: Historiker"))
    if type1 == 4:
        games_remembered = int(input("Hvor mange spill vil du ha i historien til subsekvensene? 1, 2 eller 3?"))
        player1 = Historian(name1, games_remembered)
    elif type1 == 3:
        player1 = MostCommon(name1)
    elif type1 == 2:
        player1 = Sequential(name1)
    else:
        player1 = Random(name1)

    name2 = input("Hva heter motspiller?")
    type2 = int(input("Hvordan spiller er det?  \n1: random \n2: Sekvensiell \n3: Mest Vanlig \n4: Historiker"))
    if type2 == 4:
        games_remembered = int(input("Hvor mange spill vil du ha i historien til subsekvensene? 1, 2 eller 3?"))
        player2 = Historian(name2, games_remembered)
    elif type2 == 3:
        player2 = MostCommon(name2)
    elif type2 == 2:
        player2 = Sequential(name2)
    else:
        player2 = Random(name2)

    number_of_games = int(input("Hvor mange spill skal dere spille?"))

    t = Tournament(player1, player2, number_of_games)
    t.multiple_games()


main()
#a = Historian('Martin', 3)
#b = Sequential('Henrik')
# c = Tournament(a, b, 100)
#c.multiple_games()

