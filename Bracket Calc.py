#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This tool predicts your chances of making top 8 at a bracket
given a certain selection of characters.
@author: Muna Nwana (Infernape)
"""

#import statements
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn import metrics



df = pd.read_excel('Offline Data.xlsx')

#train/test split
x = df['Chars_All']

y = df['Top_8']


X_train, X_test, y_train, y_test = train_test_split(x, y, 
                                                               test_size=0.3, 
                                                               random_state=0)


#TFIDF-vectorizing the list of characters we play
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1,
                        ngram_range=(1, 2), 
                        stop_words='english')

fitted_vectorizer = tfidf.fit(X_train)
tfidf_vectorizer_vectors = fitted_vectorizer.transform(X_train)

#using a logistic regression model
#model = RandomForestClassifier(max_depth=2, random_state=0)
model = LogisticRegression(random_state=0)
model.fit(tfidf_vectorizer_vectors, y_train)
y_pred = model.predict(fitted_vectorizer.transform(X_test))

#full classification metrics report
print('\t\t\t\tCLASSIFICATIION METRICS\n')
print(metrics.classification_report(y_test, y_pred))


#graphing station for confusion matrix
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(8,8))
sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title("CONFUSION MATRIX - Top 8 Predictor (Logistic Regression)", size=16)
plt.show()
print()


#creating a sample bracket of characters you play in bracket

bracket_str = input('Please enter the list of characters you will play against: ')

bracket_calc = model.predict(fitted_vectorizer.transform([bracket_str]))
bracket_p = model.predict_proba(fitted_vectorizer.transform([bracket_str]))[0][1]

print('The characters in your bracket path are:', bracket_str)
print('Top 8 Prediction:', bracket_calc, 'with a success probability of:',
      round((bracket_p * 100),2))


