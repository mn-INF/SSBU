#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This tool predicts your chances of making top 8 at a bracket
given a certain selection of characters.
@author: Muna N (Infernape)
"""

#import statements
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
import pickle
import seaborn as sns
from sklearn import metrics

df = pd.read_excel('Offline Data.xlsx')

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

#creating pipeline with the vectorizer and the RF model
model = make_pipeline(tvec, RandomForestClassifier(n_estimators=200, random_state=0))
model.fit(X_train, y_train)

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

#Creating model file

# Save to file in the current working directory
pkl_filename = "model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)

# Load from file
with open(pkl_filename, 'rb') as file:
    pickle_model = pickle.load(file)
    
# Calculate the accuracy score with the saved model and predict target values
score = pickle_model.score(X_test, y_test)
print("Test score: {0:.2f} %".format(100 * score))
Ypredict = pickle_model.predict(X_test)

##loading the model from the saved file
pkl_filename = "model.pkl"
with open(pkl_filename, 'rb') as f_in:
    model = pickle.load(f_in)
