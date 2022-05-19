import matplotlib.pyplot as plt

xvar = [0, 1, 2, 3, 4, 5, 6, 7]
yvar = [0, 0, 0, 0, 8.14438838744907, 33.1342306695855, 343.486959121503, 1980.33294301231]

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