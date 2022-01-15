# Imports
import random
import time

class individual:
    def __init__(self, genes):
        self.genes = genes

    def __str__(self):
        return 'Individual with genes:  ' + str(self.genes)

    def calc_fit(self, function):
        return function(self.genes)

    def mutate(self, propability, function):
        if random.random() < propability:
            self.genes = function(self.genes)
        else:
            pass


def fit(genes):
    score = 0
    for g in genes:
        if g == 'a':
            score += 1
        else:
            pass
    return score


def mutation(genes):
    index = random.randint(0, len(genes) - 1)
    try:
        pom = genes[index]
        genes[index] = genes[index + 1]
        genes[index + 1] = pom
    except:
        pom = genes[index]
        genes[index] = genes[index - 1]
        genes[index - 1] = pom
    return genes


def copulate(i1, i2):
    lengen = len(i1.genes)
    new_genes = i1.genes + i2.genes
    while lengen < len(new_genes):
        _ = new_genes.pop(int(len(new_genes) / 2))
    return individual(new_genes)


def proliferate(individuals):
    i = 0
    j = 0
    while i < int(len(individuals) / 2):
        new_i = copulate(individuals[i], individuals[i + 1])
        individuals[-1 - j] = new_i
        i += 2
        j += 1
    return individuals


class island:
    def __init__(self, individuals):
        self.individuals = individuals

    def step(self, proliferate, propability_mutation=0.1):
        dummy = x = self.individuals
        self.individuals = sorted(x, key=lambda x: x.calc_fit(fit), reverse=True)
        self.individuals = proliferate(self.individuals)
        for ind in self.individuals:
            ind.mutate(propability_mutation, mutation)

    def __str__(self):
        string = """\n"""
        for ind in self.individuals:
            string += str(ind)
            string += '\n'
        return string


i1 = individual(['a', 'a', 'b', 'd', 'a', 'c'])
print(i1)
i1.mutate(0.9, mutation)
print(i1)
print(i1.calc_fit(fit))

G = ['a','b','c','d']
Individuals = []
for _ in range(20):
    genes = []
    for char in range(6):
        genes.append(random.choice(G))
    Individuals.append(individual(genes))

Population = island(Individuals)
print('Initial Generation')
print(Population)
print('___________________ \n')

for i in range(40):
    Population.step(proliferate)
    print('Generation {}'.format(i))
    print('___________________ \n')
    print(Population)
