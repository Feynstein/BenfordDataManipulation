import matplotlib.pyplot as plt
import csv
import numpy as np
from matplotlib.lines import Line2D
import BenfordGenerator as gen



with open("COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv", newline="") as csvfile:
    fullData = list(csv.reader(csvfile))


foundStates = []
stateTimeSeries = {}

for line in fullData:

    if line[0] == "UID" or line[5] == "" or line[4] == "" or float(line[4]) >= 80000: continue

    if not(line[6] in foundStates):
        stateTimeSeries[line[6]] = [int(i) for i in line[11:]]
        foundStates.append(line[6])
    else:
        stateTimeSeries[line[6]] = [stateTimeSeries[line[6]][i] + int(line[i + 11]) for i in range(0, len(line) - 11)]

stateTimeSeriesStrings = {}
stateTimeSeriesGrowth = {}

for key in stateTimeSeries:
    stateTimeSeriesStrings[key] = [str(i) for i in stateTimeSeries[key]]
    stateTimeSeriesGrowth[key] = []
    for i in range(1, len(stateTimeSeries[key])):
        if stateTimeSeries[key][i - 1] == 0:
            stateTimeSeriesGrowth[key].append(0)
        else:
            stateTimeSeriesGrowth[key].append(float(stateTimeSeries[key][i]/stateTimeSeries[key][i - 1]))

benfordProbs = [np.log10((1 + d)/d) for d in range(1, 10)]


usStateProbs = []
goodUSStateNumbers = []
usStateCounts = []
usStates = []

for key in stateTimeSeries:

    usStateProbs.append([0.0 for i in range(0, 9)])
    goodUSStateNumbers.append([])
    usStateCounts.append(0.0)
    usStates.append(key)

    currentNumbers = stateTimeSeries[key]
    currentGrowthRates = stateTimeSeriesGrowth[key]
    currentNumberStrings = stateTimeSeriesStrings[key]


    for i in range(0, len(currentGrowthRates)):
        if currentGrowthRates[i] >= 1.1:
            goodUSStateNumbers.append(currentNumbers[i])
            firstDigit = int(currentNumberStrings[i][0]) - 1
            usStateProbs[-1][firstDigit] += 1.0
            usStateCounts[-1] += 1.0

    for i in range(0, len(usStateProbs[-1])):
        if usStateCounts[-1] == 0:
            continue
        else:
            usStateProbs[-1][i] = usStateProbs[-1][i]/usStateCounts[-1]

x = [i for i in range(1, 10)]

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.plot(x, benfordProbs, "o", label="Benford's")
for i in range(30, 50):#len(usStateProbs)):
    plt.plot(x, usStateProbs[i], label=usStates[i])
plt.legend(loc="upper right")
plt.savefig("usBenford4.png")
plt.show()