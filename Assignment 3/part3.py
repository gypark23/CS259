import json
import os
import re
import matplotlib as mpl
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates
from datetime import datetime


story_history_data = open('data/story_history.json')
story_history_dict = json.load(story_history_data)
story_views = story_history_dict["Your Story Views"]


maxval = 0
datelist = []
storyviewlist = []
maxdate = ""
storyviewsbytime = list(0 for i in range(24))
for story in story_views:
    if(story["Story Views"] > maxval):
        maxval = story["Story Views"]
        maxdate = story["Story Date"]
    date = story["Story Date"]
    datelist.append(datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]), int(date[17:19])))
    storyviewlist.append(int(story["Story Views"]))
    storyviewsbytime[int(date[11:13]) % 24] += int(story["Story Views"])

maxtime = max(storyviewsbytime)
maxtimeindex = storyviewsbytime.index(maxtime)

#https://stackoverflow.com/questions/1574088/plotting-time-in-python-with-matplotlib
x_values = datelist
y_values = storyviewlist
"""
plt.plot_date(x_values, y_values)
plt.gcf().autofmt_xdate()
"""

fig, ax = plt.subplots()
sc = ax.scatter(x_values,y_values, c = y_values, cmap = 'plasma')
ax.get_yaxis().set_visible(False)
fig.colorbar(sc)
fig.autofmt_xdate()
fig.suptitle("Story Views by Date")
plt.xlabel("Date")
plt.ylabel("Views")
plt.savefig("pics/story.png", dpi = 500)
plt.close()


x_values = list(range(0,24))
y_values = storyviewsbytime
fig, ax = plt.subplots()
sc = ax.scatter(x_values,y_values, c = y_values, cmap = 'plasma')
ax.get_yaxis().set_visible(False)
fig.colorbar(sc)
fig.suptitle("Story Views by Time")
plt.xlabel("Time")
plt.ylabel("Views")
plt.savefig("pics/storyviewsbytime.png", dpi = 500)
plt.close()

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0,20, border = 1, ln = 1, txt='Your Popularity in Recent 7 Days (Story Views)', align = 'C')
pdf.set_font('Arial',size=12)
pdf.cell(0,20, border = 0, ln = 1, txt='You gained total ' + str(sum(storyviewlist)) + " views for your Story in recent 7 days.")
pdf.image("pics/story.png", x = 30, w=150, h = 100)
pdf.cell(0,5, border = 0, ln = 1, txt= "It seems you got the most views on " + maxdate)
pdf.cell(0,5, border = 0, ln = 1, txt= "with most views of " + str(maxval))
pdf.image("pics/storyviewsbytime.png", x = 30, w=150, h = 100)
pdf.cell(0,5, border = 0, ln = 1, txt= "It seems you got the most views at " + str(maxtimeindex)  + ":00")
pdf.cell(0,5, border = 0, ln = 1, txt= "with most views of " + str(maxtime))
pdf.output("data_fun_visualization_non_privacy.pdf")