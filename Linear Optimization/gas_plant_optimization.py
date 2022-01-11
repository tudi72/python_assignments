import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

price = np.array([200, 160, 205, 210, 150, 180, 550, 600,
                  400, 330, 160, 150, 160, 150, 350, 200,
                  380, 500, 550, 210, 230, 200, 190, 180., ])  # price for every hour in CZK

# variable
x = cp.Variable(price.size)

arr = x[:-1] - x[1:]
for xx in arr:
    print(xx)
# constraints
constraint = [
    x >= 40.,  # minimum power is 40
    x <= 180.,  # maximum power over 80 M
    cp.sum(x) == 80 * 24.0,  # average power must be 80
    cp.sum(x[:10]) == 500.,  # average power over first 10 hours must be 50
    x[:-1] - x[1:] <= 20.,  # should not exceed 20
    x[1:] - x[:-1] <= 20.  # should not exceed 20

]

# trying to get the objective
objective = cp.Maximize(x * price)

# solving the problem using a linear solver
problem = cp.Problem(objective, constraint)
problem.solve()

plt.plot(price)
plt.xlabel('hour')
plt.ylabel('price CZK')
plt.plot(x.value)
plt.show()

