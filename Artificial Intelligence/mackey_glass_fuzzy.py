from math import pow
import numpy as np
import matplotlib.pyplot as plt

# Mackey-Glass differential eq. parameters
Beta = 0.2
Gamma = 0.1
Tau = 30
n = 10
# initializing an array of random values for numerical simulation
y = np.random.rand(Tau + 1)
# length of our simulation
samples = 600

# calculating Mackey-Glass eq. for samples
for _ in range(samples):
    value = y[-1] + Beta * y[-1 - Tau] / (1 + pow(y[-1 - Tau], n)) - Gamma * y[-1]
    y = np.r_[y, value]

# we dont need those first random values
y = y[-samples:]

# lets plot it
plt.figure()
plt.plot(y, label='Mackey-Glass')
plt.legend()
plt.xlabel('samples [-]')
plt.ylabel('x')
plt.grid(True)

# Look Up Table parameters
TrainingData = y[0:300]  # Training data for fuzzy system, we use only first 300 samples
TestingData = y  # We use all of our data for testing
NumStatements = 5  # Number of fuzzy-statements in fuzzy IF-THEN rule
NumFuzzySets = 7  # Number of Fuzzy Sets in input and output area


# define our membership function
def triangle(x, center, D):
    if x <= (center - D):
        return 0
    if x >= (center + D):
        return 0
    else:
        return -(1 / D) * abs(x - center) + 1


# Creating an array of fuzzy-sets centers
Minimum = min(TrainingData)
Maximum = max(TrainingData)
D = (Maximum - Minimum) / (NumFuzzySets - 1)
FuzzySetsCenters = []
for i in range(NumFuzzySets - 1):
    FuzzySetsCenters.append(Minimum + i * D)
FuzzySetsCenters.append(Maximum)

# creating INPUT-OUTPUT pairs
RulesData = []
for i in range(len(TrainingData) - NumStatements):
    rule = []
    for j in range(NumStatements):
        rule.append(TrainingData[i + j])
    RulesData.append(rule)

# fuzzy IF-THEN rules
FuzzyRules = []
for i in range(len(RulesData)):
    rulefp = []
    for j in range(NumStatements):
        fp = []
        for k in range(NumFuzzySets):
            _ = triangle(RulesData[i][j], FuzzySetsCenters[k], D)
            fp.append(_)
        rulefp.append(FuzzySetsCenters[fp.index(max(fp))])
    FuzzyRules.append(rulefp)


# function, which assign degree to a fuzzy IF-THEN rule
def DegreeRule(RuleData, FuzzyRule):
    value = 1
    for i in range(len(RuleData)):
        value = value * triangle(RuleData[i], FuzzyRule[i], D)
    return value


# Assign degrees to fuzzy IF-THEN rules and deleting conflict ones with lower degree
FRules = FuzzyRules.copy()
for i in range(len(FuzzyRules)):
    for j in range(i, len(FuzzyRules)):
        if FuzzyRules[i][:-1] == FuzzyRules[j][:-1] and not i == j:
            Degree1 = DegreeRule(RulesData[i], FuzzyRules[i])
            Degree2 = DegreeRule(RulesData[j], FuzzyRules[j])
            if Degree1 > Degree2:
                FRules[j] = None
            else:
                FRules[i] = None
        else:
            pass

# New, non-conflict fuzzy IF-THEN rules, our fuzzy system base
FuzzyRules = []
for i in range(len(FRules)):
    if not FRules[i] is None:
        FuzzyRules.append(FRules[i])


# function of our fuzzy system
def MamdaniValue(X, FuzzyRules, D):
    pom1 = 0
    pom2 = 0
    for FuzzyRule in FuzzyRules:
        pom3 = 1
        for i in range(len(X)):
            pom3 = pom3 * triangle(X[i], FuzzyRule[i], D)
        pom1 = pom1 + FuzzyRule[-1] * pom3
        pom2 = pom2 + pom3
    try:
        return pom1 / pom2
    except ZeroDivisionError:
        return 0


# Calculating predicted value, real Mackey-Glass and absolute deviation
TestingInputs = []
for i in range(len(TestingData) - NumStatements):
    vector = []
    for j in range(NumStatements - 1):
        vector.append(TestingData[i + j])
    TestingInputs.append(vector)

Predicted = []
for i in range(NumStatements):
    Predicted.append(TestingData[i])  # Insert values, for same lenght of arrays
for j in range(len(TestingData) - NumStatements):
    Predicted.append(MamdaniValue(TestingData[j:j + NumStatements - 1], FuzzyRules, D))

Deviation = []
for i in range(len(TestingData)):
    Deviation.append(abs(TestingData[i] - Predicted[i]))

# ploting predicted value, real Mackey-Glass and absolute deviation
plt.figure(dpi=80, figsize=(12, 8))
plt.plot(TestingData, 'b', label='Mackey-Glass')
plt.plot(Predicted, 'k', label='Mackey-Glass - LUT')
plt.plot(Deviation, 'r', label='Absolute Deviation')
plt.legend()
plt.xlabel('samples [-]')
plt.ylabel('x')
plt.grid(True)
plt.show()