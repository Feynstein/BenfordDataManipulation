import matplotlib.pyplot as plt
import csv
import numpy as np
from matplotlib.lines import Line2D
import BenfordGenerator as gen



with open("COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", newline="") as csvfile:
    fullData = list(csv.reader(csvfile))
 

chinaProvinces = []
chinaNumberStrings = []
chinaNumbers = []
chinaGrowthRates = []

for currentData in fullData:
    if currentData[1] == "China":
        chinaProvinces.append(currentData[0])
        chinaNumberStrings.append([val for val in currentData[4:]])
        chinaNumbers.append([float(val) for val in currentData[4:]])
        chinaGrowthRates.append([])
  


for province in range(0, len(chinaNumbers)):
    currentData = chinaNumbers[province]
    for i in range(1, len(currentData)):
        if(currentData[i - 1] == 0):
            chinaGrowthRates[province].append(0.0)
        else:
            chinaGrowthRates[province].append(currentData[i]/currentData[i - 1])


benfordProbs = [np.log10((1 + d)/d) for d in range(1, 10)]

chinaProvProbs = []
goodChinaProvNumbers = []
chinaProvCounts = []
for prov in range(0, len(chinaProvinces)):

    chinaProvProbs.append([0.0 for i in range(0, 9)])
    goodChinaProvNumbers.append([])
    chinaProvCounts.append(0.0)

    currentNumbers = chinaNumbers[prov]
    currentGrowthRates = chinaGrowthRates[prov]
    currentNumberStrings = chinaNumberStrings[prov]
    for i in range(0, len(currentGrowthRates)):
        if currentGrowthRates[i] >= 1.1:
            goodChinaProvNumbers[-1].append(currentNumbers[i])
            firstDigit = int(currentNumberStrings[i][0]) - 1
            chinaProvProbs[-1][firstDigit] += 1.0
            chinaProvCounts[-1] += 1.0

    for i in range(0, len(chinaProvProbs[-1])):
        if chinaProvinces[prov] == "Tibet":
            chinaProvProbs[-1][i] = 0
        else:
            chinaProvProbs[-1][i] = chinaProvProbs[-1][i]/chinaProvCounts[-1]

fakeChinaProvProbs = []
fakeGoodChinaNumbers = []
allFakeGoodNumbers = []

chiValues = {}
bestChiRealDistributions = {}
bestChiFakeDistributions = {}
examinatedProvinces = []

for n in range(0, 1000):
    if n % 1000 == 0: print(100.0*n/100000)
    for prov in range(0, len(chinaProvinces)):

        if len(goodChinaProvNumbers[prov]) == 0 or np.mean(goodChinaProvNumbers[prov]) < 200: 
            continue
        elif not(prov in examinatedProvinces):
            examinatedProvinces.append(prov)
            chiValues[prov] = 1e06
                
        currentGoodNumbers = goodChinaProvNumbers[prov]
        length = len(currentGoodNumbers)
        minVal = int(np.min(currentGoodNumbers))
        maxVal = int(np.max(currentGoodNumbers))
        fakeGood, fakeProbs = gen.getBenfordDistribution(length, minVal, maxVal)
        fakeGoodChinaNumbers.append(fakeGood)
        fakeChinaProvProbs.append(fakeProbs)
        allFakeGoodNumbers.extend(fakeGood)

        chiSquared = 0.0

        realGood = goodChinaProvNumbers[prov]

        if len(realGood) != len(fakeGood):
            print("Distributions do not match")
            exit(0)

        for i in range(0, len(realGood)):
            chiSquared += ((realGood[i] - fakeGood[i])**2)/realGood[i]
        
        chiSquared = chiSquared/len(realGood)

        if chiSquared < chiValues[prov]:
            chiValues[prov] = chiSquared
            bestChiFakeDistributions[prov] = fakeGood
            bestChiRealDistributions[prov] = realGood


for key in chiValues:
    print("\\rule{{0pt}}{{2.5ex}}")
    print(chinaProvinces[key] + " & " + "{:.2f}".format(chiValues[key]) + " & " + str(int(np.max(goodChinaProvNumbers[key]))) + "\\\\ [0.5ex]")
    print("\\hline")

tmpList = []
for key in chiValues:
    if chiValues[key] < 200:
        tmpList.append(chiValues[key])

print("Mean Chi:" + str(np.mean(tmpList)) + " stdDev:" + str(np.std(tmpList)))


plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.xlabel("Arbitrary days")
plt.ylabel("Confirmed case numbers")
for key in bestChiFakeDistributions:
    if chinaProvinces[key] == "Hubei": continue
    plt.plot(bestChiFakeDistributions[key], "-.r")
for key in bestChiRealDistributions:
    if chinaProvinces[key] == "Hubei": continue
    plt.plot(bestChiRealDistributions[key], "-b")

custom_lines = [Line2D([0], [0], color="r", lw=2),
                Line2D([0], [0], color="b", lw=2)]

plt.gca().legend(custom_lines, ['Best Fake Data', 'Real Data'])
plt.savefig("fakeRealExample.png", dpi=100)
plt.show()




allFakeLog = np.log10(allFakeGoodNumbers)

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Probability Density")
plt.xlabel("Logarithmic values of the fake number distribution of China")
plt.hist(allFakeLog, bins=20, density=True)
plt.xticks([0.5*i for i in range(0, 11)])
plt.savefig("fakeChinaDistributions.png", dpi=100)
plt.show()

allFakeProbs = [0.0 for i in range(0, len(benfordProbs))]
allFakeGoodNumberStrings = [str(val) for val in allFakeGoodNumbers]
allFakeCount = 0.0

for i in range(0, len(allFakeGoodNumbers)):
    firstDigit = int(allFakeGoodNumberStrings[i][0]) - 1
    allFakeProbs[firstDigit] += 1.0
    allFakeCount += 1.0

allFakeProbs = [allFakeProbs[i]/allFakeCount for i in range(0, len(allFakeProbs))]

x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

plt.figure(figsize=(15, 10), facecolor="w", edgecolor="k")
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], benfordProbs, "o", label="Benford's")
plt.plot(x, allFakeProbs, label="All fake data Benford's")
plt.ylabel("Benford's distributions")
plt.xlabel("First digit of the number")
plt.legend()
plt.savefig("allfakeBenfordData.png")
plt.show()

fakedProvinces = []

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Computer generated confirmed cases with a growth rate > 10%")
plt.xlabel("Arbitrary Days")
for i in range(0, len(chinaProvinces)):
    if np.max(fakeGoodChinaNumbers[i]) > 100.0 and chinaProvinces[i] != "Hubei":
        fakedProvinces.append(i)
        color = next(plt.gca()._get_lines.prop_cycler)['color']
        plt.plot(fakeGoodChinaNumbers[i], label=chinaProvinces[i], color=color)
plt.legend(loc="upper left")
plt.savefig("fakeChinaGoodConfirmed.png")



plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Confirmed cases with a growth rate > 10%")
plt.xlabel("Arbitrary Days")
for i in range(0, len(chinaProvinces)):
    if not(i in fakedProvinces): continue
    color = next(plt.gca()._get_lines.prop_cycler)['color']
    plt.plot(goodChinaProvNumbers[i], label=chinaProvinces[i], color=color)
plt.legend(loc="upper left")
plt.savefig("chinaGoodConfirmed.png")



x = [i for i in range(1, 10)]

plt.figure(figsize=(15, 10), facecolor="w", edgecolor="k")
plt.plot(x, benfordProbs, "o", label="Benford's")
plt.ylabel("Computer Generated Benford's distributions")
plt.xlabel("First digit of the number")
for i in range(0, len(chinaProvinces)):
    if not(i in fakedProvinces): continue
    color = next(plt.gca()._get_lines.prop_cycler)['color']
    plt.plot(x, fakeChinaProvProbs[i], label=chinaProvinces[i], color=color)
plt.legend()
plt.savefig("fakeBenfordData.png")



plt.figure(figsize=(15, 10), facecolor="w", edgecolor="k")
plt.plot(x, benfordProbs, "o", label="Benford's")
plt.ylabel("Benford's distributions")
plt.xlabel("First digit of the number")
for i in range(0, len(chinaProvinces)):
    if not(i in fakedProvinces): continue
    color = next(plt.gca()._get_lines.prop_cycler)['color']
    plt.plot(x, chinaProvProbs[i], label=chinaProvinces[i], color=color)
plt.legend()
plt.savefig("provGoodData.png")


