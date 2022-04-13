import json
import os
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import pandas as pd
import cartopy.crs as ccrs
from matplotlib.backends.backend_pdf import PdfPages

font_color = '#525252'
hfont = {'fontname':'Calibri'}
facecolor = '#eaeaf2'
color_red = '#fd625e'
color_blue = '#01b8aa'

os.mkdir("pics")

user_profile = open('data/user_profile.json')
user_profile_dict = json.load(user_profile)
breakdown = user_profile_dict['Breakdown of Time Spent on App']
breakdown_labels = []
breakdown_percentage = []
for element in breakdown:
    breakdown_percentage.append(float("".join(re.findall('\d*\.?\d+', element))))
    breakdown_labels.append(element.partition(":")[0])

fig1, ax1 = plt.subplots()
ax1.pie(breakdown_percentage, labels = breakdown_labels, autopct = '%1.1f%%')
ax1.set_title('Breakdown of Time Spent on App', fontsize = 18, color = color_blue)
ax1.axis('equal')
plt.savefig("pics/breakdown.png", dpi=1000)
plt.close()

events = user_profile_dict["Engagement"]
engagement_sent = [0, 0, 0, 0]
engagement_received = [0, 0, 0, 0]
engagement_sent[0] = events[1]['Occurrences']
engagement_sent[1] = events[0]['Occurrences']
engagement_sent[2] = events[3]['Occurrences']
engagement_sent[3] = events[4]['Occurrences']
engagement_received[0] = events[11]['Occurrences']
engagement_received[1] = events[12]['Occurrences']
engagement_received[2] = events[13]['Occurrences']
engagement_received[3] = events[8]['Occurrences']

engagement_category = ["Chats", "Direct Snaps", "Snap", "Story"]
engagement_df = pd.DataFrame({'Category': engagement_category, 'Sent':engagement_sent, 'Received': engagement_received})

#https://sharkcoder.com/data-visualization/mpl-bidirectional
fig2, axes = plt.subplots(figsize=(15,5), facecolor = facecolor, ncols=2, sharey=True)
fig2.tight_layout()
hbar1 = axes[0].barh(engagement_category, engagement_df["Sent"], color = color_red)
axes[0].set_title("Sent", fontsize = 18, color = color_red)
hbar2 = axes[1].barh(engagement_category, engagement_df["Received"], color = color_blue)
axes[1].set_title("Received", fontsize = 18, color = color_blue)
axes[0].invert_xaxis()
axes[0].yaxis.tick_left()
axes[0].set_xticks([20, 40, 60, 80, 100, 120, 140, 160])
axes[1].set_xticks([20, 40, 60, 80, 100, 120, 140, 160])
axes[0].spines['right'].set_color('white')
axes[1].spines['left'].set_color('white')
plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
plt.savefig("pics/sentreceived.png",dpi=1000)


plt.close()
#https://stackoverflow.com/questions/64705422/is-there-a-way-to-take-country-two-letter-alpha-codes-and-display-them-on-a-map
countryCode = pd.read_csv("https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv")
country = user_profile_dict["App Profile"]["Country"]
latitude = 0
longitude = 0
for index, row in countryCode.iterrows():
    temp = row[1][2:4]
    if(country == temp):
        latitude=(float(row[5][2:-1]))
        longitude=(float(row[4][2:-1]))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
plt.plot(latitude, longitude,  markersize=2, marker='o', color='red')
plt.text(latitude - 3, longitude - 12, country,
        horizontalalignment='right',
        transform=ccrs.Geodetic())

plt.savefig('pics/map.png', dpi=1000)



account= open('data/account.json')
account_dict = json.load(account)
basicinfo = account_dict["Basic Information"]
username = basicinfo["Username"]
name = basicinfo["Name"]
date = basicinfo["Creation Date"]
device_history = account_dict["Device History"]
phone = device_history[0]["Make"] + " " + device_history[0]["Model"]



#https://pyfpdf.readthedocs.io/en/latest/reference/cell/index.html
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(50)
pdf.cell(0,20, border = 1, ln = 1, txt='Snapchat Summary Dashboard', align = 'C')
pdf.cell(0,20, border = 0, ln = 1, txt='Account Info', align = 'L')
pdf.set_font('Arial', 'B', 12)
pdf.cell(0,5, border = 0, ln = 1, txt = "Name: " + name)
pdf.cell(0,5, border = 0, ln = 1, txt = "User Name: " + username)
pdf.cell(0,5, border = 0, ln = 1, txt = "Creation Date: " + date)
pdf.cell(0,5, border = 0, ln = 1, txt = "Phone: " + phone)
pdf.cell(120,5, border = 0, ln = 0, txt = "Breakdown of Time Spent in Snapchat: ")
pdf.cell(0,5, border = 0, ln = 1, txt = "Location: ")
pdf.image("pics/map.png", x = 100, y = 80, h = 80, w = 100)
pdf.image("pics/breakdown.png", h=80, w=120)
pdf.cell(0,5, border = 0, ln = 1, txt = "Sent Snaps vs Received Snaps")
pdf.image("pics/sentreceived.png", h=80, w = 200)
pdf.output("data_subject_dashboard.pdf")