import matplotlib.pyplot as plt
import csv
import numpy as np
import random as rng

def setfirstdigit():
    distribution = [0.3010, 0.4771, 0.6020, 0.6980, 0.7772, 0.8441, 0.9021, 0.9533, 1.0]

    digit = 0
    randomNumber = rng.random()
    for j in range(0, len(distribution)):
        if randomNumber < distribution[j]:
            digit = j + 1
            break

    return digit

def addnextdigit(number, stopper, maxVal):

    if stopper == 1:
        return number

    addnext = 1

    while addnext == 1:
        digit = int(np.floor(10*rng.random()))

        if number*10 + digit <= maxVal: 
            number = number*10 + digit
            addnext = 0

    return number

def shallstop(number, stopper, minVal, maxVal, prob_stop):

    if stopper == 1:
        return 1

    if number < minVal:
        stopper = 0
    elif number * 10 >= maxVal:
        stopper = 1
    else:
        if rng.random() < prob_stop:
            stopper = 1
        else:
            stopper = 0
    
    return stopper

def getprobs(num_of_digits, minVal, maxVal, prob_method):

    probabilities = np.zeros(num_of_digits)
    if minVal == 0:
        min_num_of_digits = 1
    else:
        min_num_of_digits = int(np.floor(np.log10(minVal) + 1))

    for i in range(min_num_of_digits, num_of_digits):

        if prob_method == 0:
            probabilities[i] =  (1 / (num_of_digits - min_num_of_digits + 1))

        elif prob_method == 1:
            if i == min_num_of_digits:
                probabilities[i] = (10**i - minVal) / (maxVal - minVal + 1)
            elif i == num_of_digits:
                probabilities[i] = ((9 * 10**(i - 1)) - (10**i - maxVal)) / (maxVal - minVal + 1)
            else:
                probabilities[i] =  (9 * 10**(i - 1)) / (maxVal - minVal + 1)

    return probabilities
            
   
def getBenfordDistribution(length, minVal, maxVal):

    prob_method = 1
    artificial = 1


    if artificial == 0 and minVal > 0:
        print('Minimum possible value is higher than 0. Using the artificial method instead.')
        artificial = 1

    genNumbers = []

    if artificial == 0:
        #Generates the numbers in a natural way.
        genNumbers = [int(np.floor(np.exp(np.log10(maxVal)*rng.random()))) for i in range(0, length)]
    else:
        stoppers = np.zeros(length)
        prob_stops = getprobs(int(np.floor(np.log10(maxVal) + 1)), minVal, maxVal, prob_method)
        i = 1
        genNumbers = [setfirstdigit() for stopper in stoppers]
        while np.prod(stoppers) == 0:
            if i >= len(prob_stops): break
            stoppers = [shallstop(genNumbers[j], stoppers[j], minVal, maxVal, prob_stops[i]) for j in range(0, len(genNumbers))] 
            genNumbers = [addnextdigit(genNumbers[j], stoppers[j], maxVal) for j in range(0, len(stoppers))]
            i = i+1
        
    genNumbers = np.sort(genNumbers)
    genNumberStrings = [str(number) for number in genNumbers]

    genProbs = [0.0 for i in range(0, 9)]
    genCount = 0.0

    for i in range(0, len(genNumbers)):
        firstDigit = int(genNumberStrings[i][0]) - 1
        genProbs[firstDigit] += 1.0
        genCount += 1.0

    genProbs = [genProbs[i]/genCount for i in range(0, len(genProbs))]

    return genNumbers, genProbs


