#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This tool predicts your chances of making top 8 at a bracket
given a certain selection of characters.
@author: Muna N (Infernape)
"""

#import statements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn import metrics



df = pd.read_excel('Tourney Data.xlsx')

'''
#text preprocessing
#nltk.download('all')

# create a list text

text = list(df['Chars_All'])

# preprocessing loop
lemmatizer = WordNetLemmatizer()
corpus = []

for i in range(len(text)):

    r = re.sub('[^a-zA-Z]', ' ', text[i])
    r = r.lower()
    r = r.split()
    r = [word for word in r if word not in stopwords.words('english')]
    r = [lemmatizer.lemmatize(word) for word in r]
    r = ' '.join(r)
    corpus.append(r)

#assign corpus to df['Chars_All']

df['Chars_All'] = corpus
'''

#train/test split
x = df['Chars_All']

y = df['Top_8']


X_train, X_test, y_train, y_test = train_test_split(x, y, 
                                                test_size=0.3, 
                                                random_state=0)


#TFIDF-vectorizing the list of characters we play
tvec = TfidfVectorizer(sublinear_tf=True, min_df=2,
                        ngram_range=(1, 2), 
                        stop_words='english')

#creating pipeline with the vectorizer and the classification model
model = make_pipeline(tvec, RandomForestClassifier(random_state=0))
model.fit(X_train, y_train)

fitted_vectorizer = tvec.fit(X_train)
tfidf_vectorizer_vectors = fitted_vectorizer.transform(X_train)

#just seeing if we can visualize this
'''
tvec_weights = tvec.fit_transform(X_train)
weights = np.asarray(tvec_weights.mean(axis=0)).ravel().tolist()
weights_df = pd.DataFrame({'term': tvec.get_feature_names_out(), 'weight': weights})
weights_df.to_csv('TFIDF_train.csv')
'''

#uaking predictions with the model

y_pred = model.predict(X_test)

#full classification metrics report
print('\t\t\t\tCLASSIFICATIION METRICS\n')
print(metrics.classification_report(y_test, y_pred))


#graphing station for confusion matrix
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(8,8))
sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title("CONFUSION MATRIX - Top 8 Predictor (Random Forest)", size=16)
plt.show()
print()


#creating a sample bracket of characters you play in bracket

bracket_str = input('Please enter the list of characters you will play against: ')
bracket_calc = model.predict([bracket_str])
bracket_p = model.predict_proba([bracket_str])[0][1]

print('The characters in your bracket path are:', bracket_str)
print('Top 8 Prediction:', bracket_calc, 'with a success probability of:',
      round((bracket_p * 100),2))
