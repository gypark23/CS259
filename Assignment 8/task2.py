from numpy import character
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import unicodedata

urllist = pd.read_csv("top-1m.csv", header = None)
urllinks = urllist[1].to_list()

param = 500
urllinks = urllinks[:param]
#urllinks = ["instagram.com"]
first_w3c, second_w3c, third_w3c, fourth_w3c = 0, 0, 0, 0
first_mdn, second_mdn, third_mdn = 0, 0, 0

#csv from https://www.w3schools.com/tags/ref_language_codes.asp
languages = pd.read_csv("language.csv", sep = "	")
languages_inverse = pd.read_csv("language_1.csv", sep = "	")

language_dict = dict(zip(languages['ISO Code'], languages['Language']))
language_count = {language : 0 for language in languages['Language']}
language_inverse_dict = dict(zip(languages_inverse['Language'], languages_inverse['ISO Code']))

character_count = {}
def readMetaW3C(meta):
    for m in meta:
        m = str(m).lower().replace(" ", "")
        if m.find('http-equiv="content-type"') > -1 and m.find('content="text/html') > -1 and m.find('charset=utf-8') > -1:
            return 0, 1, 0, 0
        elif m.find('charset=utf-8') > -1:
            return 1, 0, 0, 0
        elif m.find('charset=') > -1:
            return 0, 0, 1, 0
        
    return 0, 0, 0, 1

def readMetaMDN(htmltag, meta):
    for h in htmltag:
        h = str(h).lower().replace(" ", "")
        if h.find('lang=') > -1:
            return 1, 0, 0
    for m in meta:
        m = str(m).lower().replace(" ", "")
        if(m.find('content-language') > -1):
            return 0, 1, 0
    
    return 0, 0, 1

#https://docs.python.org/3/library/re.html
def findLang(htmltag, meta):
    for h in htmltag:
        h = str(h).lower()
        arr = re.findall('lang="[^ |>]*"', h)
        for string in arr:
            languagecode = string[6:8]
            if(languagecode in language_dict):
                language_count[language_dict[languagecode]] += 1
    for m in meta:
        m = str(m).lower()
        arr = re.findall('lang="[^ |>]*"', m)
        for string in arr:
            languagecode = string[6:8]
            if(languagecode in language_dict):
                language_count[language_dict[languagecode]] += 1
        arr = re.findall('content-language" content="[^ |>]*"', m)
        for string in arr:
            languagecode = string[26:28]
            if(languagecode in language_dict):
                language_count[language_dict[languagecode]] += 1

def characterCount(soup):
    text = soup.getText()
    for char in text:
        try:
            if(unicodedata.name(char) in character_count):
                character_count[unicodedata.name(char)] += 1
            else:
                character_count[unicodedata.name(char)] = 1
        except:
            pass


#https://realpython.com/python-web-scraping-practical-introduction/
for link in urllinks:
    try:
        print("For " + link)
        page = urlopen('http://' + link, timeout = 3)
        html = page.read()
        soup = BeautifulSoup(html, features = 'html.parser')
        meta = soup.find_all("meta")
        htmltag = soup.find_all("html")
        a, b, c, d = readMetaW3C(meta)
        first_w3c += a
        second_w3c += b
        third_w3c += c
        fourth_w3c += d
        a, b, c = readMetaMDN(htmltag, meta)
        first_mdn += a
        second_mdn += b
        third_mdn += c
        findLang(htmltag, meta)
        characterCount(soup)

    except:
        print("Failed for " + link)

valid = first_w3c + second_w3c + third_w3c + fourth_w3c
print("------Summary------")
print("Among " + str(param) + " websites: ")
print(str(param - valid) + " Websites failed to load")
print("------W3C------")
print("Among " + str(valid) + " opened websites, according to W3C Internationalization Guide: ")
print(str(first_w3c/valid * 100) + "% (" + str(first_w3c) + ") websites used the first, short method")
print(str(second_w3c/valid * 100) + "% (" + str(second_w3c) + ") websites used the second, longer method")
print(str(third_w3c/valid * 100) + "% (" + str(third_w3c) + ") websites indicated some different character encoding")
print(str(fourth_w3c/valid * 100) + "% (" + str(fourth_w3c) + ") websites didn't indicate the character encoding")
print("------MDN------")
print("Among " + str(valid) + " opened websites, according to The Mozilla Develop Network Guide: ")
print(str(first_mdn/valid * 100) + "% (" + str(first_mdn) + ") websites used the preferred method")
print(str(second_mdn/valid * 100) + "% (" + str(second_mdn) + ") websites used the discouraged method")
print(str(third_mdn/valid * 100) + "% (" + str(third_mdn) + ") websites didn't indicate the language of the page")

language_count_df = pd.DataFrame(language_count.items())
language_count_df = language_count_df.sort_values(1, ascending = False)
language_count_df = language_count_df.rename(columns = {0 : 'Language', 1 : 'Occurence'})
language_count_df["Code"] = language_count_df["Language"].apply(lambda x: language_inverse_dict[x])
language_count_df = language_count_df[['Language', 'Code', 'Occurence']]
language_count_df_style = language_count_df.style
language_count_df.to_html('LanguageFreq.html', border = 0)

character_count_df = pd.DataFrame(character_count.items())
character_count_df = character_count_df.sort_values(1, ascending = False)
character_count_df = character_count_df.rename(columns = {0 : 'Character Name', 1 : 'Occurence'})
character_count_df = character_count_df.head(100)
character_count_df["Character"] = character_count_df['Character Name'].apply(lambda x: unicodedata.lookup(x))
character_count_df = character_count_df[['Character', 'Character Name', 'Occurence']]
character_count_df_style = character_count_df.style
character_count_df.to_html('CharacterFreq.html', border = 0)

import matplotlib.pyplot as plt
from pandas.plotting import table

ax = plt.subplot(111, frame_on = False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
plt.tight_layout()
table(ax, language_count_df)
plt.savefig("language_count.png", bbox_inches = 'tight', dpi = 500)
plt.show()

ax = plt.subplot(111, frame_on = False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
plt.tight_layout()
table(ax, character_count_df)
plt.savefig("character_count.png", bbox_inches = 'tight', dpi = 500)
plt.show()

