from genericpath import exists
import json
from multiprocessing import Queue, Process
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qs
from scipy import spatial
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity
def scrape(link):
    # Code to turn the data from urllib requeset into html str taken from https://stackoverflow.com/questions/24153519/how-to-read-html-from-a-url-in-python-3
    fp = urlopen(link)
    html_str = fp.read().decode("utf8")
    fp.close()
    return html_str

#https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
def computeSim(list1):
    return cosine_similarity(list1)

"""
def parallel(id, list1, list2, start, end):
    maximumarray = []
    maxjarray = []
    for i in range(start, end):
        print(i)
        maximum = -1
        maxj = -1
        for j in range(2101):
            sum = computeSim(list1[i], list2[j])
            if(sum > maximum):
                maximum = sum
                maxj = j
        maximumarray.append(maximum)
        maxjarray.append(maxj)
    
    nums = range(start, end)
    ret = pd.DataFrame({'id': nums, 'maxj' : maxjarray, 'max' : maximumarray})    
    ret.to_csv('final' + str(id) + '.csv', index = False)
"""
data = pd.read_csv('user_artists.dat', header = 0, sep = '	', index_col = False)
 #only count songs that were listened more than 20 times
data.loc[data['weight'] < 20, 'weight'] = 0 
artistdata = pd.read_csv('artists.dat', header = 0, sep = '	', index_col = False)
#new = data["userID"].str.split(" ", n = 2, expand = True)

#https://stackoverflow.com/questions/43203215/map-unique-strings-to-integers-in-python
artistname = artistdata["name"]
id = artistdata["id"]
artistmap = dict(zip(artistname, id))

#https://www.pythontutorial.net/python-basics/python-check-if-file-exists/
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
if(not exists("output.dat")):
    html = scrape("https://computersecurityclass.com/")
    soup = BeautifulSoup(html, 'html.parser')
    names = []
    links = []
    for link in soup.find_all('a'):
        names.append(link.text)
        links.append(link.get('href'))

    repeatednames = []
    artist = []
    times = []

    for link in links:
        print("For " + link)
        htmllink = "https://computersecurityclass.com/" + link
        html = scrape(htmllink)
        soup = BeautifulSoup(html, 'html.parser')
        
        for var in soup.find_all('li'):
            for avar in var.find_all('a'):
                if artistmap.get(avar.text) is None:
                    artist.append(-1)
                else:
                    artist.append(artistmap[avar.text])
            time = var.text[-15:]
            time = re.sub('[^0-9,]', "", time)
            times.append(int(time.replace(",","")))
            repeatednames.append(link[:-5])


    webdata = pd.DataFrame({'Name':repeatednames, 'Artist':artist, 'Times':times})

    #only count songs that were listened more than 20 times
    webdata.loc[webdata['Times'] < 20, 'Times'] = 0   
    webdata.to_csv("output.dat", index = False)

    print("Done scrapping")

else:
    webdata = pd.read_csv("output.dat", index_col = False)
    names = webdata["Name"].unique()

nametoindex = dict(zip(names, range(0, 1783)))
indextoname = dict(zip(range(0,1783), names))
#for i in range(69969):


vectors =[[0 for i in range(18746)] for j in range(1783)]

for i in range(69970):
    if(webdata['Artist'][i] == -1):
        continue
    vectors[nametoindex[webdata['Name'][i]]][webdata['Artist'][i]] = webdata['Times'][i]

print("Vec Done")


refvectors = [[0 for i in range(18746)] for j in range(2101)]
for i in range(92834):
    refvectors[data['userID'][i]][data['artistID'][i]] = data['weight'][i]

print("Ref Vec Done")

concatted = vectors + refvectors   

a = computeSim(concatted)
maxarray = []
maxjarray = []

for i in range(1783):
    max = -1
    maxj = 0
    for j in range(1783, 3884):
        if(a[i][j] > max):
            max = a[i][j]
            maxj = j - 1783
    maxarray.append(max)
    maxjarray.append(maxj)
        
finaldf = pd.DataFrame({'Name' : names, 'Max' : maxarray, 'Maxj' : maxjarray})
#set threshold to 0.9
finaldf = finaldf[finaldf["Max"] > 0.90]

jsondict = dict(zip(finaldf['Name'], finaldf['Maxj']))
#https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/
#https://moonbooks.org/Articles/How-to-save-a-dictionary-in-a-json-file-with-python-/
with open("matches.json", "w") as outfile:
    json.dump(jsondict, outfile)
print("done tojson")