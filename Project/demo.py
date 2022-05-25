import base64
import pandas as pd
import numpy as np
from src import autodc



#data to be cleaned
data = pd.read_csv("data/loan_data.csv")
#fake data from https://www.briandunning.com/sample-data/
data_2 = pd.read_csv("data/us-500.csv")

#data cleaning
autodc.clean("data/us-500.csv")
autodc.clean("data/loan_data.csv")