import json
import os
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

font_color = '#525252'
hfont = {'fontname':'Calibri'}
facecolor = '#eaeaf2'
color_red = '#fd625e'
color_blue = '#01b8aa'

friends_data = open('data/friends.json')
friends_dict = json.load(friends_data)
friends_list = friends_dict["Friends"]
friends_len = len(friends_list)
friends_list = friends_list[0:5]
for friend in friends_list:
    friend['Username'] = friend['Username'].replace(friend['Username'][2:], "**********")
    friend['Display Name'] = friend['Display Name'].replace(friend['Display Name'][2:], "**********")
friends_DataFrame = pd.DataFrame(friends_list)

fig1, ax1 = plt.subplots()
ax1.axis('off')
ax1.axis('tight')
ax1.set_title("5 Random Friends")
ax1.table(cellText = friends_DataFrame.values, colLabels = friends_DataFrame.columns, loc = 'center')
fig1.tight_layout()
plt.savefig('pics/friends.png', dpi = 300)



friend_requests_list = friends_dict["Friend Requests Sent"]
friend_requests_len = len(friend_requests_list)
friend_requests_list = friend_requests_list[0:5]
for friend in friend_requests_list:
    friend['Username'] = friend['Username'].replace(friend['Username'][2:], "**********")
    friend['Display Name'] = friend['Display Name'].replace(friend['Display Name'][2:], "**********")
friend_requests_DataFrame = pd.DataFrame(friend_requests_list)

fig1, ax1 = plt.subplots()
ax1.axis('off')
ax1.axis('tight')
ax1.set_title("5 Random Friend Reqeusts Sent")
ax1.table(cellText = friend_requests_DataFrame.values, colLabels = friend_requests_DataFrame.columns, loc = 'center')
fig1.tight_layout()
plt.savefig('pics/friendrequests.png', dpi = 300)



blocked_friends_list = friends_dict["Blocked Users"]
blocked_friends_len = len(blocked_friends_list)
blocked_friends_list = blocked_friends_list[0:5]
for friend in blocked_friends_list:
    friend['Username'] = friend['Username'].replace(friend['Username'][2:], "**********")
    friend['Display Name'] = friend['Display Name'].replace(friend['Display Name'][2:], "**********")
blocked_friends_DataFrame = pd.DataFrame(blocked_friends_list)

fig1, ax1 = plt.subplots()
ax1.axis('off')
ax1.axis('tight')
ax1.set_title("5 Random Blocked Friends")
ax1.table(cellText = blocked_friends_DataFrame.values, colLabels = blocked_friends_DataFrame.columns, loc = 'center')
fig1.tight_layout()
plt.savefig('pics/blockedfriends.png', dpi = 300)


deleted_friends_list = friends_dict["Deleted Friends"]
deleted_friends_len = len(deleted_friends_list)
deleted_friends_list = deleted_friends_list[0:5]
for friend in deleted_friends_list:
    friend['Username'] = friend['Username'].replace(friend['Username'][2:], "**********")
    friend['Display Name'] = friend['Display Name'].replace(friend['Display Name'][2:], "**********")
deleted_friends_DataFrame = pd.DataFrame(deleted_friends_list)

fig1, ax1 = plt.subplots()
ax1.axis('off')
ax1.axis('tight')
ax1.set_title("5 Random Deleted Friends")
ax1.table(cellText = deleted_friends_DataFrame.values, colLabels = deleted_friends_DataFrame.columns, loc = 'center')
fig1.tight_layout()
plt.savefig('pics/deletedfriends.png', dpi = 300)

request_received_friends_list = friends_dict["Pending Requests"]
request_received_friends_len = len(request_received_friends_list)
request_received_friends_list = request_received_friends_list[0:5]
for friend in request_received_friends_list:
    friend['Username'] = friend['Username'].replace(friend['Username'][2:], "**********")
    friend['Display Name'] = friend['Display Name'].replace(friend['Display Name'][2:], "**********")
request_received_friends_DataFrame = pd.DataFrame(request_received_friends_list)

fig1, ax1 = plt.subplots()
ax1.axis('off')
ax1.axis('tight')
ax1.set_title("5 Random Requests Received ")
ax1.table(cellText = request_received_friends_DataFrame.values, colLabels = request_received_friends_DataFrame.columns, loc = 'center')
fig1.tight_layout()
plt.savefig('pics/requestreceivedfriends.png', dpi = 300)


#https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
friends_data = {'Total Friends':friends_len, 'Total Friend Requests Sent':friend_requests_len, 'Total Friend Requests Pending':request_received_friends_len,
        'Total Deleted Friends':deleted_friends_len, 'Total Blocked Friends':blocked_friends_len}
courses = list(friends_data.keys())
values = list(friends_data.values())
fig = plt.figure(figsize = (13, 5))
fig.tight_layout()
# creating the bar plot
plt.bar(courses, values, color ='yellow',
        width = 0.4)
for i in range(len(courses)):
    plt.text(i, values[i], values[i], ha = 'center')
plt.xlabel("Category")
plt.ylabel("Number of People")
plt.title("Friend Interactions Overview")
plt.savefig("pics/friendsoverview.png", dpi = 300)


snap_history_data = open('data/snap_history.json')
snap_history_dict = json.load(snap_history_data)
received_snap = snap_history_dict["Received Snap History"]
for snap in received_snap:
    snap['From'] = snap['From'].replace(snap['From'][2:], "**********")
sent_snap = snap_history_dict["Sent Snap History"]
for snap in sent_snap:
    snap['To'] = snap['To'].replace(snap['To'][2:], "**********")

received_snap_dataframe = pd.DataFrame(received_snap)
sent_snap_dataframe = pd.DataFrame(sent_snap)

fig1, ax1 = plt.subplots()
ax1.axis('off')
ax1.axis('tight')
ax1.set_title("Received Snaps")
ax1.table(cellText = received_snap_dataframe.values, colLabels = received_snap_dataframe.columns, loc = 'center')
fig1.tight_layout()
plt.savefig('pics/receivedsnaps.png', dpi = 300)
plt.close()

fig1, ax1 = plt.subplots()
ax1.axis('off')
ax1.axis('tight')
ax1.set_title("Sent Snaps")
ax1.table(cellText = sent_snap_dataframe.values, colLabels = sent_snap_dataframe.columns, loc = 'center')
fig1.tight_layout()
plt.savefig('pics/sentsnaps.png', dpi = 300)
plt.close()

chat_history_data = open('data/chat_history.json')
chat_history_dict = json.load(chat_history_data)
received_saved_chat = chat_history_dict["Received Saved Chat History"]
medianum = 0
textnum = 0
othernum = 0
lasttext = ""
lastdate = ""
for i in range(len(received_saved_chat)):
    if(received_saved_chat[i]["Media Type"] == "MEDIA"):
        medianum += 1
    elif(received_saved_chat[i]["Media Type"] == "TEXT"):
        lasttext = received_saved_chat[i]["Text"]
        lastdate = received_saved_chat[i]["Created"]
        textnum += 1
    else:
        othernum += 1

fig1, ax1 = plt.subplots()
breakdown_labels = ["Media", "Text", "Other"]
breakdown_percentage = [medianum, textnum, othernum]
ax1.pie(breakdown_percentage, labels = breakdown_labels, autopct = '%1.1f%%')
ax1.set_title('Breakdown of Saved Received Chats', fontsize = 18, color = color_blue)
ax1.axis('equal')
plt.savefig("pics/savedchatsbreakdown.png", dpi=300)
plt.close()


sent_saved_chat = chat_history_dict["Sent Saved Chat History"]
sentmedianum = 0
senttextnum = 0
sentothernum = 0
sentlasttext = ""
sentlastdate = ""
for i in range(len(sent_saved_chat)):
    if(sent_saved_chat[i]["Media Type"] == "MEDIA"):
        sentmedianum += 1
    elif(sent_saved_chat[i]["Media Type"] == "TEXT"):
        sentlasttext = sent_saved_chat[i]["Text"]
        sentlastdate = sent_saved_chat[i]["Created"]
        senttextnum += 1
    else:
        sentothernum += 1

fig1, ax1 = plt.subplots()
sentbreakdown_labels = ["Media", "Text", "Other"]
sentbreakdown_percentage = [sentmedianum, senttextnum, sentothernum]
ax1.pie(breakdown_percentage, labels = breakdown_labels, autopct = '%1.1f%%')
ax1.set_title('Breakdown of Saved Sent Chats', fontsize = 18, color = color_blue)
ax1.axis('equal')
plt.savefig("pics/savedsentchatsbreakdown.png", dpi=300)
plt.close()


media_total = [medianum, sentmedianum]
text_total = [textnum, senttextnum]
media_plus_text = [medianum + textnum, sentmedianum + senttextnum]
other_total = [othernum, sentothernum]
#https://www.geeksforgeeks.org/create-a-stacked-bar-plot-in-matplotlib/
plt.cla()
plt.bar(["Received", "Sent"], media_total, 0.6, color = 'g')
plt.bar(["Received", "Sent"], text_total, 0.6, bottom = media_total, color = 'b')
plt.bar(["Received", "Sent"], other_total, 0.6, bottom = media_plus_text, color = 'y')
plt.ylabel("Snaps")
plt.title("Analysis of Saved Received and Sent Snap Types")
plt.legend(["Media", "Text", "Others"])
plt.savefig("pics/stackedreceivedsent")
plt.close()



memories_data = open('data/memories_history.json')
memories_dict = json.load(memories_data)
memories_list = memories_dict["Saved Media"]
lastmemory = memories_list[len(memories_list) - 1]

videonum = 0
imagenum = 0
for memory in memories_list:
    if(memory["Media Type"] == "Video"):
        videonum += 1
    else:
        imagenum += 1

fig1, ax1 = plt.subplots()
memorybreakdown_labels = ["Video", "Image"]
memorybreakdown_percentage = [videonum, imagenum]
ax1.pie(memorybreakdown_percentage, labels = memorybreakdown_labels, autopct = '%1.1f%%')
ax1.set_title('Breakdown of Memory', fontsize = 18, color = color_blue)
ax1.axis('equal')
plt.savefig("pics/memorybreakdown.png", dpi=300)
plt.close()



memories_list = memories_list[0:5]

memories_DataFrame = pd.DataFrame(memories_list)
memories_DataFrame = memories_DataFrame.drop(columns = ["Download Link"], axis=1)
fig1, ax1 = plt.subplots()
ax1.axis('off')
ax1.axis('tight')
ax1.set_title("5 Most Recent Memories")
ax1.table(cellText = memories_DataFrame.values, colLabels = memories_DataFrame.columns, loc = 'center')
fig1.tight_layout()
plt.savefig('pics/memories.png', dpi = 300)







pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(50)
pdf.cell(0,20, border = 1, ln = 1, txt='Friend Summary Dashboard', align = 'C')
pdf.set_font('Arial', 'B', 12)
pdf.cell(0,20, ln = 1)
pdf.cell(0,5, border = 0, ln = 1, txt = "Overview:")
pdf.image('pics/friendsoverview.png', h=50, w=130, x = 80)
pdf.cell(0,5, border = 0, ln = 1, txt = "5 Random Friends:")
pdf.image('pics/friends.png', h=120, w = 200)
pdf.cell(0,5, border = 0, ln = 1, txt = "5 Random Friend Request Received:                                    5 Random Friend Request Sent:")
pdf.image('pics/friendrequests.png', h=60, w=100, x = 0, y = 245)
pdf.image('pics/requestreceivedfriends.png', h=60, w=100, x = 100, y = 245)
pdf.add_page()
pdf.cell(0,5, border = 0, ln = 1, txt = "5 Random Blocked Friends:")
pdf.image('pics/blockedfriends.png', h=120, w=200)
pdf.cell(0,5, border = 0, ln = 1, txt = "5 Random Deleted Friends:")
pdf.image('pics/deletedfriends.png', h=120, w=200)
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(50)
pdf.cell(0,20, border = 1, ln = 1, txt='Recently Received and Sent Snaps', align = 'C')
pdf.image('pics/receivedsnaps.png', w=120, h=80)
pdf.image('pics/sentsnaps.png', w=120,h=80)
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(50)
pdf.cell(0,20, border = 1, ln = 1, txt='Saved Snaps', align = 'C')
pdf.set_font('Arial', 'B', 12)
pdf.cell(0,20, ln = 1)
pdf.image("pics/stackedreceivedsent.png", w=93.6*2, h=72)
pdf.cell(0,20, ln = 1)
pdf.cell(0,5, border = 1, ln = 1, txt = "Recently Received Saved Snaps Overview:")
pdf.image('pics/savedchatsbreakdown.png', w=120, h=80)
pdf.cell(0,5, border = 0, ln = 1, txt = "Media: " + str(medianum))
pdf.cell(0,5, border = 0, ln = 1, txt = "Text: " + str(textnum))
pdf.cell(0,5, border = 0, ln = 1, txt = "Others: " + str(othernum))
pdf.cell(0,20, border = 0, ln = 1, txt = "Your very first saved received text message was...: ")
pdf.set_font('Arial', 'I', 12)
pdf.cell(0,5, border = 0, ln = 1, txt = "\"" +lasttext + "\"")
pdf.set_font('Arial', 'B', 12)
pdf.cell(0,5, border = 0, ln = 1, txt = "On " +lastdate)
pdf.cell(0,5, ln = 1)
pdf.cell(0,5, border = 1, ln = 1, txt = "Sent Saved Snaps Overview:")
pdf.image('pics/savedsentchatsbreakdown.png', w=120, h=80)
pdf.cell(0,5, border = 0, ln = 1, txt = "Media: " + str(sentmedianum))
pdf.cell(0,5, border = 0, ln = 1, txt = "Text: " + str(senttextnum))
pdf.cell(0,5, border = 0, ln = 1, txt = "Others: " + str(sentothernum))
pdf.cell(0,20, border = 0, ln = 1, txt = "Your very first saved sent text message was...: ")
pdf.set_font('Arial', 'I', 12)
pdf.cell(0,5, border = 0, ln = 1, txt = "\"" +sentlasttext + "\"")
pdf.set_font('Arial', 'B', 12)
pdf.cell(0,5, border = 0, ln = 1, txt = "On " +sentlastdate)

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0,20, border = 1, ln = 1, txt='Memories', align = 'C')
pdf.set_font('Arial', 'B', 12)
pdf.cell(0,20, ln = 1)
pdf.image("pics/memorybreakdown.png", w=120, h=80)
pdf.cell(0,20, ln = 1)
pdf.cell(0,5, border = 0, ln = 1, txt = "Video: " + str(videonum))
pdf.cell(0,5, border = 0, ln = 1, txt = "Image: " + str(imagenum))
pdf.cell(0,20)
pdf.image("pics/memories.png", x= 0, w=120, h=80)
pdf.cell(0,5, ln = 1)
pdf.cell(0,20, border = 0, ln = 1, txt = "Your very first saved memory was...: ")
pdf.set_font('Arial', 'I', 12)
pdf.cell(0,5, border = 0, ln = 1, txt = "a " +lastmemory["Media Type"])
pdf.set_font('Arial', 'B', 12)
pdf.cell(0,5, border = 0, ln = 1, txt = "On " +lastmemory["Date"])



pdf.output("data_privacy_dashboard.pdf")