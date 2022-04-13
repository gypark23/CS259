import pandas as pd
import csv

#assume the original csv file is named download.csv
data = pd.read_csv('download.csv')
data['First Name'] = '*'
data['Last Name'] = '*'
data['ZIP Code'] = '*'
data.loc[data['Age'] <= 18, 'Age'] = "<= 18"
data.loc[data['Age'].apply(pd.to_numeric, errors = 'coerce').between(18, 41), 'Age'] = "19 - 40"
data.loc[data['Age'].apply(pd.to_numeric, errors = 'coerce').between(40, 66), 'Age'] = "41 - 65"
data.loc[data['Age'].apply(pd.to_numeric, errors = 'coerce').gt(66), 'Age'] = ">= 65"
data.to_csv('release.csv',index=False)