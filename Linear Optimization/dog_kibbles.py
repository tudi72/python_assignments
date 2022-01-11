# grain 7.5 $
# carrot 9.2 $
# meat 60.0 $
# at least 18% percent is meat
# 45% percent must be grain

import cvxpy as cp

grain_price = 7.5
carrot_price = 9.2
meat_price = 60

# decision variables
grain, carrot, meat = cp.Variable(), cp.Variable(), cp.Variable()

# constraints
constraint = [
    grain <= 0.45,  # first constraint
    meat >= 0.18,  # second constraint
    grain >= 0.0, carrot >= 0.0, meat >= 0.0,  # non-zero constraint
    (grain + meat + carrot) == 1.0
]

objective = grain * grain_price + meat * meat_price + carrot * carrot_price

# formulate the problem
problem = cp.Problem(cp.Minimize(objective), constraint)

problem.solve()
print("Optimal dog food values:")
print('grain:', grain.value)
print('meat:', meat.value)
print('carrot:', carrot.value)
