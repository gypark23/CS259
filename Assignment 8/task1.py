import hashlib
from itertools import count
import random
import energyusage
import matplotlib.pyplot as plt

def hash256(string):
    m = hashlib.sha256()
    m.update(string.encode())
    return m.hexdigest()

#mining by incrementing (part 1-1)
def mine(prev_hash, transaction, target):
    for i in count():
        hexstr = hex(i)
        concat = hexstr + prev_hash + transaction
        hashstr = hash256(concat)
        dechash = int(hashstr, 16)
        if(dechash < target):
            print(i)
            return i

#mining by random nonce (part 1-2)
def randommine(prev_hash, transaction, target):
    num = 0
    while True:
        nonce = random.randint(0, pow(2, 256))
        hexstr = hex(nonce)
        concat = hexstr + prev_hash + transaction
        hashstr = hash256(concat)
        dechash = int(hashstr, 16)
        num += 1
        if(dechash < target):
            return num, nonce
    

prev_hash = '00000003ef809ab31c2339e3938349437161a40eb9d19162b0185bc5be78d2f8'
transaction = '14d65eb004b8fca9fa7873263ddfb0b0f3101be84ebb5f847ac6f9aaf2a17ebf'
target = pow(2, 228)

#part 1-1
print(mine(prev_hash, transaction, target))

#part 1-2
sum = 0
for i in range(5):
    num, nonce = randommine(prev_hash, transaction, target)
    print(nonce)
    print(num)
    sum += num

print("Average Number of Hashes: " + str(sum / 5))

#helper functions for energy usage
#part 1-4
def generateHash(nonce, prev_hash, transaction):
    concat = nonce + prev_hash + transaction
    hash256(concat)

def generateHashes(n):
    for i in range(n):
        generateHash(hex(i), prev_hash, transaction)


print("for 100000000 hashes")
energyusage.evaluate(generateHashes, 100000000, pdf = True, energyOutput = True)
print("for 250000000 hashes")
energyusage.evaluate(generateHashes, 250000000, pdf = True, energyOutput = True)

#for leading 0, 1, 2, 3 zeroes energy couldn't be calculated (too small energy usage), thus set at 0
xvar = [0, 1, 2, 3]
yvar = [0, 0, 0, 0]

for i in range(4, 8):
    print("Leading " + str(i) + " zeroes")
    time, energy, val = energyusage.evaluate(mine, prev_hash, transaction, pow(2, 256 - 4 * i), energyOutput = True, printToScreen = False)
    print(val)
    floatenergy = float(energy)
    xvar.append(i)
    #convert kWh to Joules
    yvar.append(floatenergy * 3600000)

xvar_pred = []
yvar_pred = []

from math import e

for i in range (7, 63):
    xvar_pred.append(i)
    yvar_pred.append(0.0037 * e ** (1.882 * i))    #exponential equation derived from excel

fig, ax = plt.subplots()
ax.plot(xvar, yvar, 'blue', label='measured')
plt.title("Consumption of Energy vs Number of Leading Zeroes (With Predictions)", fontsize = 8)
plt.xlabel("Number of Leading Zeroes")
plt.ylabel("Consumption of Energy (Joules)")
ax.plot(xvar_pred, yvar_pred, 'r--', label = 'Expected')
ax.legend(loc='best', frameon=False)
plt.savefig("figure.png", dpi = 500)
plt.clf()
plt.plot(xvar, yvar)
plt.title("Consumption of Energy vs Number of Leading Zeroes (With Actual Measurements)", fontsize = 8)
plt.xlabel("Number of Leading Zeroes")
plt.ylabel("Consumption of Energy (Joules)")
plt.savefig("figure_measured.png", dpi = 500)