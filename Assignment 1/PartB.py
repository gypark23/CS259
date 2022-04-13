from random import random
from matplotlib import pyplot as plt
import pandas as pd
from scipy import rand
from sklearn import datasets
import csv

data = pd.read_csv('loan_data.csv')
data.dropna(subset=['race'], inplace = True)
data.dropna(subset=['gender'], inplace = True)
data.dropna(subset=['zip'], inplace = True)
data['income'].fillna((data['income'].mean()), inplace=True)
data[['approved']] *= 1
#data['years_to_pay'] = data['principal']/data['income']
data = pd.get_dummies(data, columns=['race', 'gender', 'type'])



"""
xvar = data[['gender_male', 'gender_non-binary', 'type_auto', 'type_home', 'type_personal',
'income', 'term', 'interest', 'principal', 'adj_bls_2']]
"""
"""
xvar = data[['type_auto', 'type_home', 'type_personal','income', 'term', 'interest', 'principal', 'adj_bls_2']]
"""
"""
xvar = data[['income', 'term', 'interest', 'principal', 'adj_bls_2']]
"""
"""
xvar = data[['race_asian', 'race_black', 'race_hispanic/latino', 'race_other', 'race_white',
'gender_female', 'gender_male', 'gender_non-binary', 'type_auto', 'type_home', 'type_personal',
'years_to_pay', 'term', 'interest', 'adj_bls_2']]
"""
"""
xvar = data[['race_asian', 'race_black', 'race_hispanic/latino', 'race_other', 'race_white',
'gender_female', 'gender_male', 'gender_non-binary', 'type_auto', 'type_home', 'type_personal',
'income', 'term', 'interest', 'principal', 'adj_bls_2', 'years_to_pay']]

"""
xvar = data[['race_asian', 'race_black', 'race_hispanic/latino', 'race_other', 'race_white',
'gender_female', 'gender_male', 'gender_non-binary', 'type_auto', 'type_home', 'type_personal',
'income', 'term', 'interest', 'principal', 'adj_bls_2']]


yvar = data[['approved']]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(xvar, yvar, test_size = 0.2, random_state= 9)
#X_train, X_test, y_train, y_test = train_test_split(xvar, yvar, test_size = 0.2)
#X_train, X_test, y_train, y_test = train_test_split(xvar, yvar, test_size = 0.2, random_state=109)

from sklearn import svm

clf = svm.SVC(kernel = 'linear')
clf.fit(X_train, y_train.values.ravel())
y_pred = clf.predict(X_test)

from sklearn import metrics
print("Accuracy:" , metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))
print("F1 Score:", metrics.f1_score(y_test, y_pred))

matrix = metrics.ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test)
plt.show()

#Final Variable Used: race, gender, type, income, term, interest, principal, adj_bls_2
#'race_asian', 'race_black', 'race_hispanic/latino', 'race_other', 'race_white', 'gender_female', 'gender_male', 'gender_non-binary', 'type_auto', 'type_home', 'type_personal', 'income', 'term', 'interest', 'principal', 'adj_bls_2'