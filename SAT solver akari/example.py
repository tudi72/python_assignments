import pycosat
import itertools
from itertools import combinations


cnf = [[1, 2, 3], [-1, -2, -3]]
# cnf = CardEnc.atmost(lits=[1, 2, 3], encoding=EncType.pairwise)

literals = [1,2,3]
def def_constraint_two(cnf,literals):
    smth = set()
    for l in literals:
        for comb in itertools.combinations(literals,2):
            for x in literals:
                if x != comb[0] and x!= comb[1]:
                    cnf.append([comb[0],comb[1],-x])
    return cnf
# smth = list(itertools.islice(pycosat.itersolve(cnf), 3))
cnf = def_constraint_two(cnf,literals)
for clause in cnf:
    print(clause)
