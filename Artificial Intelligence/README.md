# Mackey-Glass Time Series Prediction Using Look Up Table 

The purpose of this work is to create a fuzzy system for time series prediction of Mackey-Glass equation, which is delay differential equation:

The function approximation is done using the following formula: 

![image](https://user-images.githubusercontent.com/33194623/149630324-d13cfcfa-10cd-4154-9eab-4dfdc1eea988.png)

After we put the constants the function will look like this: 

![CodeCogsEqn](https://user-images.githubusercontent.com/33194623/149630075-cc90b407-1783-46ce-89f1-0b3187373a6d.png)

# Design of fuzzy system
The goal is to create a fuzzy system only from input-output data. We use only the first 300 values of x. The n represents number of statements in fuzzy IF-THEN rule. Thus we make a input-output pairs for creating fuzzy rules for look up table system only from input set.


    [x(0),x(1),...,x(n-1),x(n)]
    [x(1),x(2),...,x(n-1),x(n+1)]
    .
    .
    .
    [x(299-n),x(299-n + 1),...,x(298),x(299)]


We choose that our system is Look up table with product inference engine, triangular fuzzyfier and center average defuzzyfier:

![image](https://user-images.githubusercontent.com/33194623/149630249-00d4daba-5c5a-412c-b4a2-a8978d295ba1.png)

Since the number of input-output is usually large, and with each pair generating a single rule, there is high chance, that there are some conflict ones. Which means, there are rules with same IF part but different THEN parts. Therefore, we assign degree of a rule:

![image](https://user-images.githubusercontent.com/33194623/149630275-43e94085-fa7f-487e-923b-d84aea2b5c55.png)

Hence we choose non-conflict fuzzy rules, and from conflict rules we choose ones with the highes degree. Chosen Fuzzy Rules are our fuzzy system base.
