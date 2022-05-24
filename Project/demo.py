import base64
import pandas as pd
import numpy as np
from src import autodc
from cryptography.fernet import Fernet
import binascii


orig = pd.read_csv("data/loan_data.csv")
data = pd.read_csv("data/loan_data.csv")
data_2 = pd.read_csv("data/us-500.csv")
"""
data = autodc.deleteEmptyRow(data, includeZero=True)
data = autodc.columnDummyize(data)

data = autodc.encryptCols(data)

f = open('key.txt', 'r')
key = f.read()
f.close()
data = autodc.decryptCols(data, key)

print(key)
"""
#data = autodc.decryptCols(data, key)
autodc.clean("data/us-500.csv")
autodc.clean("data/loan_data.csv")
after_clean = pd.read_csv("data/us-500_cleaned.csv")
f = open('key.txt', 'r')
key = f.read()
f.close()
"""
print(key)
print(after_clean["address"][0])
print(autodc.fernetDecrypt(after_clean["address"][0], key))
t = autodc.fernetEncrypt("abc", key)
to = str(t)[2:]
to = to[:-1]
tok_test = bytes(to, 'raw_unicode_escape')


#autodc.fernetDecrypt(base64.b64decode(str(tok)), key)
c = autodc.fernetDecrypt(tok_test, key)
print(c)
"""

#autodc.decryptCols(after_clean, key, ["address"])