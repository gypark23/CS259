import pandas as pd
import numpy as np
from cryptography.fernet import Fernet
import random
from Crypto.Util import number
import binascii
from commonregex import CommonRegex
from datetime import datetime
import time
import re

#https://cryptography.io/en/latest/fernet/
def fernetEncrypt(string, key):
    string = string.encode('UTF-8')
    f = Fernet(key)
    token = f.encrypt(string)
    return token

def fernetDecrypt(token, key):
    #print("hi")
    f = Fernet(key)
    #if not byte
    if(type(token) != type(b'a')):
        #if not string
        if(type(token) != type('a')):
            return token
        
        if(not token[0:2] == "b'"):
            return token
        else:
            token = token[2:]
            token = token[:-1]
            token = bytes(token, 'raw_unicode_escape')
            return f.decrypt(token).decode('UTF-8')
    else:
        return f.decrypt(token).decode('UTF-8')


def columnDummyize(data, columns = [], param = 10):
    if(not columns):
        columns = data.columns

    todo = []

    for column in columns:
        count = len(pd.unique(data[column]))
        #we leave true/false undummied
        if(count < param and count > 2):
            todo.append(column)
    
    data = pd.get_dummies(data, columns = todo)
    return data

def deleteEmptyRow(data, columns = [], includeZero = False):

    #argument gave no columns therefore delete all rows
    if(not columns):
        if(includeZero):
            data = data.replace({0, np.nan})
        data = data.dropna()

    else:
        for column in columns:
            if(includeZero):
                data[column] = data[column].replace(0, np.nan)
        data = data.dropna(subset = columns)

    return data

def encryptCols(data, columns = []):

    key = Fernet.generate_key()
    f = Fernet(key)
    
    #save key to txt file
    with open('key.txt', 'w') as file: 
        file.write(key.decode('ascii'))

    #argument gave no columns therefore encrypt all
    if(not columns):
        data = data.applymap(lambda x: fernetEncrypt(str(x), key))
    else:
        for column in columns:
            #print(column)
            data[column] = data[column].apply(lambda x: fernetEncrypt(str(x), key))


    return data

def decryptCols(data, key, columns = []):
    key = key.encode('ascii')
    f = Fernet(key)
    
    #argument gave no columns therefore decrypt all
    if(not columns):
        data = data.applymap(lambda x: fernetDecrypt(x, key))
    else:
        for column in columns:
            data[column] = data[columns].applymap(lambda x: fernetDecrypt(x, key))

    return data

#return True if any of the column in Pandas Series include PII
def piiDetect(series):
    for index, value in series.items():
        parsed_text = CommonRegex(str(value))
        if(parsed_text.links or parsed_text.phones or parsed_text.emails
        or parsed_text.ips or parsed_text.credit_cards or parsed_text.btc_addresses or parsed_text.street_addresses):
            return True

    return False

def clean(filename, param = 10):
    
    data = pd.read_csv(filename)
    f = open('results.log', 'w')
    f.write("Summary Log of Autmoated Data Cleaning of file " + filename + "\n")
    prog_start = time.time()
    f.write(str(datetime.now()) + "\n")

    piicol = []
    nonpiicol = []
    nonpiicol_underten = []
    for column in data:
        if(piiDetect(data[column])):
            piicol.append(column)
        else:
            if(len(pd.unique(data[column])) < param and len(pd.unique(data[column])) > 2):
                nonpiicol_underten.append(column)
            nonpiicol.append(column)
    
    f.write("-----------------------\n")
    origRow = len(data)
    data = deleteEmptyRow(data)
    f.write("Total " + str(origRow - len(data)) + " rows were found to include NaN and thus were deleted:\n")
    
    f.write("-----------------------\n")
    f.write("The following column(s) were found to include Personally Identifiable Information (PII):\n")
    f.write(str(piicol) + "\n")
    f.write("These column(s) will be hashed with a key provided in key.txt\n")
    f.write("Note: If you believe there should be more columns to be encrypted/should not be encrypted\n")
    f.write("Try manual encryption/decryption using encryptCols and decryptCols\n")
    f.write("Start Hashing...\n")
    start_time = time.time()
    data = encryptCols(data, piicol)
    f.write("Done Hashing! in %s seconds\n" % (time.time() - start_time))
    f.write("Key saved in \"key.txt\"\n")
    f.write("Use this key to decrypt the text\n")


    f.write("-----------------------\n")
    f.write("These columns were found to include more than 2 but less than 10 unique values:\n")
    f.write(str(nonpiicol_underten) + "\n")
    f.write("These columns will be made into dummy variables")
    data = columnDummyize(data, nonpiicol)
    f.write("Dummy Variables Created!\n")
    f.write("Total " + str(len(data.columns) - len(piicol) - len(nonpiicol)) + " columns were created\n")

    f.write("-----------------------\n")
    f.write("Done! in %s seconds\n" % (time.time() - prog_start))
    f.write("Output CSV exported as \"" + filename[:-4] + ".csv\"")
    data.to_csv(filename[:-4] + "_cleaned.csv", index = False)
        