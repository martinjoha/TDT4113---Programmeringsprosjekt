
class Action:
    # 0: stein 1: saks 2: papir
    valid_moves = [0, 1, 2]
    beats = {0: 1, 1: 2, 2: 0}
    name = {0: 'stein', 1: 'saks', 2: 'papir'}

    def __init__(self, move):
        self.move = self.valid_moves[move]

    def __eq__(self, other):
        return self.move == other.move

    def __gt__(self, other):
        return self.beats[self.move] == other.move

    def __str__(self):
        return self.name[self.move]

    def __repr__(self):
        return self.name[self.move]

    def get_num(self):
        return self.move

    def get_value(self,index):
        return self.valid_moves[index]

    def main(self):
        a = Action(2)
        print(a)


a = Action(1)
b = Action(2)
print(a>b)

a = Action(1)
a.main()
