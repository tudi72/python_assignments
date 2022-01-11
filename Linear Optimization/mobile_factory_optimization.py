import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# finding the best solution to maximize the profit of the whole factory

price_a = np.full(12, 325.)

price_b = np.array([300, 300, 290, 275, 275, 280,
                    260, 250, 230, 200, 210, 190.])

price_c = np.array([100, 110, 98, 115, 200, 220,
                    210, 500, 500, 490, 487, 550.])

profit_a = cp.Variable(12)
profit_b = cp.Variable(12)
profit_c = cp.Variable(12)

phone_a = cp.Variable(12)
phone_b = cp.Variable(12)
phone_c = cp.Variable(12)


profit_constraint = [
    profit_a[:-1] - profit_a[1:] == 0.,  # profit for A will be constant for every following month
    profit_b[1:] - profit_b[:-1] <= 0.,  # profit will be lowering for phone type B every month
    profit_c[1:] - profit_c[:-1] >= 0.,  # profit will increase every month for type C
    np.sum([phone_a[0], phone_b[0], phone_c[0]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[1], phone_b[1], phone_c[1]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[2], phone_b[2], phone_c[2]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[3], phone_b[3], phone_c[3]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[4], phone_b[4], phone_c[4]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[5], phone_b[5], phone_c[5]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[6], phone_b[6], phone_c[6]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[7], phone_b[7], phone_c[7]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[8], phone_b[8], phone_c[8]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[9], phone_b[9], phone_c[9]], axis=0) <= 10000.,  # factory cannot produce more than 10.000 / month
    np.sum([phone_a[10], phone_b[10], phone_c[10]], axis=0) <= 10000.,  # factory cannot produce more than 10.000/month
    np.sum([phone_a[11], phone_b[11], phone_c[11]], axis=0) <= 10000.,  # factory cannot produce more than 10.000/month

    np.sum(phone_a) >= 24000.,  # type A produces more than 2000 per month or at least 24.000 per year
    np.sum(phone_b) >= 24000.,  # type B produces more than 2000 per month or at least 24.000 per year
    np.sum(phone_c) >= 24000.,  # type B produces more than 2000 per month or at least 24.000 per year

    phone_c[6:] <= 5000.,  # type C cannot produces more than 5000 in the second half of year
    phone_b <= 4500.,  # type B cannot produce more than 4500 per month
    phone_a[:-6] <= 4000.,  # type A cannot exceed 4000 in the first half of the month
]

objective = cp.Maximize(phone_a * price_a * profit_a + phone_b * price_b * profit_b + phone_c * price_c * profit_c)
problem = cp.Problem(objective, profit_constraint)

problem.solve()
print(problem)

