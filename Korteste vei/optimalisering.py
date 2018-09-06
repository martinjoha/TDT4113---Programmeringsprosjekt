import random
import copy
import math
import matplotlib.pyplot as plt

class Optimizer:

    def __init__(self, max_iterations=25000):
        self.max_iterations = max_iterations
        self.bidrag_matrise = [[None] * 10 for x in range(10)]

    def straff(self, x):
        straff = 0
        for i in range(len(x) - 1):
            #print(x)
            if self.bidrag_matrise[x[i]][x[i+1]] is None:
                self.bidrag(x[i],x[i+1])
            straff += self.bidrag_matrise[x[i]][x[i+1]]
        if self.bidrag_matrise[x[-1]][x[0]] is None:
            self.bidrag(x[-1], x[0])
        straff += self.bidrag_matrise[x[-1]][x[0]]
        return straff

    def straff_2(self, x):
        straff = 0
        for i in range(len(x) -1):
            straff += self.bidrag_2(x[i], x[i+1])
        straff += self.bidrag_2(x[-1], x[0])
        return straff


    def bidrag(self, x, y):
        self.bidrag_matrise[x][y] = abs(math.sin((x-y)/10))

    def bidrag_2(self, x, y):
        return abs(math.sin((x-y)/10))

    def optimize(self, x):
        y = copy.deepcopy(x)
        n1 = random.randint(0, len(y) - 1)
        n2 = random.randint(0, len(y) - 1)
        while n1 == n2:
            n2 = random.randint(0, len(y) - 1)
        y[n1], y[n2] = y[n2], y[n1]
        y_straff = self.straff_2(y)
        x_straff = self.straff_2(x)
        if x_straff > y_straff:
            return [y, y_straff]
        return [x, x_straff]

    def solve(self, x):
        straffer = []
        for i in range(self.max_iterations):
            optimert = self.optimize(x)
            x = optimert[0]
            straffer.append(optimert[1])
        #plt.ylabel("Straff")
        #plt.xlabel("Iterasjoner")
        #plt.plot(straffer)
        #plt.show()
        return [x, self.straff_2(x), straffer]


class SimulatedAnnealing(Optimizer):

    def __init__(self, temperature):
        super().__init__()
        self. temperature = temperature


    def optimize(self, x):
        y = copy.deepcopy(x)
        n1 = random.randint(0, len(y) - 1)
        n2 = random.randint(0, len(y) - 1)
        while n1 == n2:
            n2 = random.randint(0, len(y) - 1)
        y[n1], y[n2] = y[n2], y[n1]
        y_straff = self.straff_2(y)
        x_straff = self.straff_2(x)
        if y_straff <= x_straff + (self.temperature * math.log(1/random.random())):
            self.temperature *= 0.995
            return [y, y_straff]
        return [x, x_straff]


def main():
    x = [1,3,6,2,9,0,8,5,4,7]
    s = Optimizer(1000)
    plt.xlabel("Iterations")
    plt.ylabel("Weight")
    for i in range(10):
        data = s.solve(x)
        plt.plot(data[2])
    plt.show()

main()




x = [1,3,6,2,9,0,8,5,4,7]
o = Optimizer(100)
#print(o.solve(x))
y = SimulatedAnnealing(100)
x = y.optimize(x)[0]
#print(x)
#print(y.solve(x))


