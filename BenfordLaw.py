import matplotlib.pyplot as plt
import csv
import numpy as np

import BenfordGenerator as gen

import itertools

with open("COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", newline="") as csvfile:
    fullData = list(csv.reader(csvfile))
 

chinaProvinces = []
chinaNumberStrings = []
chinaNumbers = []
chinaGrowthRates = []

italyNumberStrings = []
italyNumbers = []
italyGrowthRates = []

germanyNumberStrings = []
germanyNumbers = []
germanyGrowthRates = []

franceNumberStrings = []
franceNumbers = []
franceGrowthRates = []

for currentData in fullData:
    if currentData[1] == "China":
        chinaProvinces.append(currentData[0])
        chinaNumberStrings.append([val for val in currentData[4:]])
        chinaNumbers.append([float(val) for val in currentData[4:]])
        chinaGrowthRates.append([])
    elif currentData[1] == "Italy":
        italyNumberStrings = [val for val in currentData[4:]]
        italyNumbers = [float(val) for val in currentData[4:]]
    elif currentData[1] == "Germany":
        germanyNumberStrings = [val for val in currentData[4:]]
        germanyNumbers = [float(val) for val in currentData[4:]]
    elif currentData[1] == "France" and currentData[0] == "":
        franceNumberStrings = [val for val in currentData[4:]]
        franceNumbers = [float(val) for val in currentData[4:]]

for i in range(1, len(italyNumbers)):
    if italyNumbers[i - 1] == 0:
        italyGrowthRates.append(0.0)
    else:
        italyGrowthRates.append(italyNumbers[i]/italyNumbers[i - 1])

    if germanyNumbers[i - 1] == 0:
        germanyGrowthRates.append(0.0)
    else:
        germanyGrowthRates.append(germanyNumbers[i]/germanyNumbers[i - 1])

    if franceNumbers[i - 1] == 0:
        franceGrowthRates.append(0.0)
    else:
        franceGrowthRates.append(franceNumbers[i]/franceNumbers[i - 1])      


for province in range(0, len(chinaNumbers)):
    currentData = chinaNumbers[province]
    for i in range(1, len(currentData)):
        if(currentData[i - 1] == 0):
            chinaGrowthRates[province].append(0)
        else:
            chinaGrowthRates[province].append(currentData[i]/currentData[i - 1])


plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Confirmed cases")
plt.xlabel("Days since January 22th")
for i in range(0, len(chinaProvinces)):
    if chinaProvinces[i] == "Hubei":
        plt.plot(chinaNumbers[i], label=chinaProvinces[i])
    else:
        plt.plot(chinaNumbers[i])
plt.legend()
plt.savefig("chinaConfirmed.png")
plt.show()

# benfordProbs = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
benfordProbs = [np.log10((1 + d)/d) for d in range(1, 10)]

chinaProbs = [0.0 for i in range(0, len(benfordProbs))]
goodChinaNumbers = []
chinaCount = 0.0

hubeiProbs = [0.0 for i in range(0, len(benfordProbs))]
goodHubeiNumbers = []
hubeiCount = 0.0

rocProbs = [0.0 for i in range(0, len(benfordProbs))]
goodRocNumbers = []
rocCount = 0.0

for prov in range(0, len(chinaGrowthRates)):
    for i in range(0, len(chinaGrowthRates[prov])):
        if chinaGrowthRates[prov][i] >= 1.1:
            goodChinaNumbers.append(chinaNumbers[prov][i + 1])
            firstDigit = int(chinaNumberStrings[prov][i + 1][0]) - 1
            chinaProbs[firstDigit] += 1.0
            chinaCount += 1.0

            if chinaProvinces[prov] == "Hubei":
                goodHubeiNumbers.append(chinaNumbers[prov][i + 1])
                firstDigit = int(chinaNumberStrings[prov][i + 1][0]) - 1
                hubeiProbs[firstDigit] += 1.0
                hubeiCount += 1.0
            else:
                goodRocNumbers.append(chinaNumbers[prov][i + 1])
                firstDigit = int(chinaNumberStrings[prov][i + 1][0]) - 1
                rocProbs[firstDigit] += 1.0
                rocCount += 1.0

chinaProbs = [chinaProbs[i]/chinaCount for i in range(0, len(chinaProbs))]
hubeiProbs = [hubeiProbs[i]/hubeiCount for i in range(0, len(hubeiProbs))]
rocProbs = [rocProbs[i]/rocCount for i in range(0, len(rocProbs))]

italyProbs = [0.0 for i in range(0, len(benfordProbs))]
goodItalyNumbers = []
italyCount = 0.0

for i in range(0, len(italyGrowthRates)):
    if italyGrowthRates[i] >= 1.1:
        goodItalyNumbers.append(italyNumbers[i + 1])
        firstDigit = int(italyNumberStrings[i + 1][0]) - 1
        italyProbs[firstDigit] += 1.0
        italyCount += 1.0

italyProbs = [italyProbs[i]/italyCount for i in range(0, len(italyProbs))]


germanyProbs = [0.0 for i in range(0, len(benfordProbs))]
goodGermanyNumbers = []
germanyCount = 0.0

for i in range(0, len(germanyGrowthRates)):
    if germanyGrowthRates[i] >= 1.1:
        goodGermanyNumbers.append(germanyNumbers[i + 1])
        firstDigit = int(germanyNumberStrings[i + 1][0]) - 1
        germanyProbs[firstDigit] += 1.0
        germanyCount += 1.0

germanyProbs = [germanyProbs[i]/germanyCount for i in range(0, len(germanyProbs))]

franceProbs = [0.0 for i in range(0, len(benfordProbs))]
goodFranceNumbers = []
franceCount = 0.0

for i in range(0, len(germanyGrowthRates)):
    if franceGrowthRates[i] >= 1.1:
        goodFranceNumbers.append(franceNumbers[i + 1])
        firstDigit = int(franceNumberStrings[i + 1][0]) - 1
        franceProbs[firstDigit] += 1.0
        franceCount += 1.0

franceProbs = [franceProbs[i]/franceCount for i in range(0, len(franceProbs))]


chinaProvProbs = []
goodChinaProvNumbers = []
chinaProvCounts = []
for prov in range(0, len(chinaProvinces)):


    chinaProvProbs.append([0.0 for i in range(0, len(benfordProbs))])
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

for prov in range(0, len(chinaProvinces)):
    if chinaProvinces[prov] == "Tibet":
        fakeGoodChinaNumbers.append([0.0, 0.0])
        fakeChinaProvProbs.append([0.0 for i in range(0, 9)])
    else:
        currentGoodNumbers = goodChinaProvNumbers[prov]
        length = len(currentGoodNumbers)
        minVal = int(np.min(currentGoodNumbers))
        maxVal = int(np.max(currentGoodNumbers))
        fakeGood, fakeProbs = gen.getBenfordDistribution(length, minVal, maxVal)
        fakeGoodChinaNumbers.append(fakeGood)
        fakeChinaProvProbs.append(fakeProbs)
        allFakeGoodNumbers.extend(fakeGood)


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

exit(0)

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Benford's distributions for different countries")
plt.xlabel("First digit of the number")
plt.plot(x, chinaProbs, label="China")
plt.plot(x, italyProbs, label="Italy")
plt.plot(x, germanyProbs, label="Germany")
plt.plot(x, hubeiProbs, label="Hubei")
plt.plot(x, rocProbs, label="ROC")
plt.plot(x, franceProbs, label="France")
plt.plot(x, benfordProbs, "o", label="Benford's")
plt.legend(loc="top right")
plt.savefig("benford.png", dpi=100)
plt.show()


chinaChiSquare = 0.0
italyChiSquare = 0.0
germanyChiSquare = 0.0
franceChiSquare = 0.0
hubeiChiSquare = 0.0
rocChiSquare = 0.0

for i in range(0, len(chinaProbs)):
    chinaChiSquare += ((chinaProbs[i] - benfordProbs[i])**2)/benfordProbs[i]
    italyChiSquare += ((italyProbs[i] - benfordProbs[i])**2)/benfordProbs[i]
    germanyChiSquare += ((germanyProbs[i] - benfordProbs[i])**2)/benfordProbs[i]
    franceChiSquare += ((franceProbs[i] - benfordProbs[i])**2)/benfordProbs[i]
    hubeiChiSquare += ((hubeiProbs[i] - benfordProbs[i])**2)/benfordProbs[i]
    rocChiSquare += ((rocProbs[i] - benfordProbs[i])**2)/benfordProbs[i]

chinaChiSquare = chinaCount*chinaChiSquare
italyChiSquare = italyCount*italyChiSquare
germanyChiSquare = germanyCount*germanyChiSquare
franceChiSquare = franceCount*franceChiSquare
hubeiChiSquare = hubeiCount*hubeiChiSquare
rocChiSquare = rocCount*rocChiSquare

print("China:" + str(chinaChiSquare))
print("Italy:" + str(italyChiSquare))
print("Germany:" + str(germanyChiSquare))
print("France:" + str(franceChiSquare))
print("Hubei:" + str(hubeiChiSquare))
print("Rest of China (ROC)" + str(rocChiSquare))



chinaLogValues = np.log10(goodChinaNumbers)
italyLogValues = np.log10(goodItalyNumbers)
germanyLogValues = np.log10(goodGermanyNumbers)
franceLogValues = np.log10(goodFranceNumbers)
hubeiLogValues = np.log10(goodHubeiNumbers)
rocLogValues = np.log10(goodRocNumbers)

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Probability Density")
plt.xlabel("Logarithmic values of the number distribution of China")
plt.hist(chinaLogValues, bins=20, density=True)
plt.xticks([0.5*i for i in range(0, 11)])
plt.savefig("chinaDistributions.png", dpi=100)
plt.show()

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Probability Density")
plt.xlabel("Logarithmic values of the number distribution of Italy")
plt.hist(italyLogValues, bins=20, density=True)
plt.xticks([0.5*i for i in range(0, 11)])
plt.savefig("italyDistributions.png", dpi=100)
plt.show()

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Probability Density")
plt.xlabel("Logarithmic values of the number distribution of Germany")
plt.hist(germanyLogValues, bins=20, density=True)
plt.xticks([0.5*i for i in range(0, 11)])
plt.savefig("germanyDistributions.png", dpi=100)
plt.show()

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Probability Density")
plt.xlabel("Logarithmic values of the number distribution of France")
plt.hist(franceLogValues, bins=20, density=True)
plt.xticks([0.5*i for i in range(0, 11)])
plt.savefig("franceDistributions.png", dpi=100)
plt.show()

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Probability Density")
plt.xlabel("Logarithmic values of the number distribution of Hubei Province")
plt.hist(hubeiLogValues, bins=20, density=True)
plt.xticks([0.5*i for i in range(0, 11)])
plt.savefig("hubeiDistributions.png", dpi=100)
plt.show()

plt.figure(figsize=(11, 8), facecolor="w", edgecolor="k")
plt.ylabel("Probability Density")
plt.xlabel("Logarithmic values of the number distribution of The Rest of China (ROC)")
plt.hist(rocLogValues, bins=20, density=True)
plt.xticks([0.5*i for i in range(0, 11)])
plt.savefig("rocDistributions.png", dpi=100)
plt.show()