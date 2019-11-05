#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:13:01 2019

@author: xiaohezhang
"""

import pandas as pd
import numpy as np
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from nltk.corpus import stopwords

import pickle
#import Cleaning
#
##Cleaning.today()
#df = pd.read_csv('../data/trainset.csv')
#dt = Cleaning.combine_test('20191102')


def prepare(df,dt):
    #return X_train, X_test, y_train, y_test, X_result
    stop = stopwords.words('english') + ["http",'https', "co",'amp','CA','california']
    X = df['text']
    y = df['relevant']
    Xresult = dt['text']
    X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 42,stratify = y)

    tvect = TfidfVectorizer(max_features= 2000, stop_words= stop, ngram_range=(1,2))

    X_train = pd.DataFrame(tvect.fit_transform(X_train).toarray() ,columns = tvect.get_feature_names())
    X_test = pd.DataFrame(tvect.transform(X_test).toarray() ,columns = tvect.get_feature_names())
    X_result = pd.DataFrame(tvect.transform(Xresult).toarray() ,columns = tvect.get_feature_names())
    
    return X_train, X_test, y_train, y_test, X_result

#X_train, X_test, y_train, y_test, X_result = prepare(df,dt)
# Used for tunning the model
#    pipe_log = {
#                'C':[1e-9,1e-4,1,1e4,1e9]
#                }
#    
#    
#    pipe_svc = {
#                'C':[ 0.1,1,10],
#                'kernel':['rbf'],
#                'gamma': ['scale']
#    }
#    
#    pipe_rf = {
#            'n_estimators':[100,200,400],
#            'max_depth':[10,15,20],
#            'min_samples_leaf':[6,7,8]
#    }
#    
#    g_log = GridSearchCV(LogisticRegression(), pipe_log, cv = 3, verbose= 3, n_jobs = -1)
#    g_svc = GridSearchCV(SVC(), pipe_svc , cv = 3, verbose= 3, n_jobs = -1)
#    g_rf = GridSearchCV(RandomForestClassifier(), pipe_rf, cv = 3, verbose= 3, n_jobs = -1)
# Using this function to get score for training, testing and operate time

def get_score(X_train,X_test,g_model):
    t0 = time.time()
    g_model.fit(X_train,y_train)
    model = g_model.best_estimator_
    param = g_model.best_params_
    t1 = time.time() - t0
    return [model.score(X_train, y_train), model.score(X_test, y_test), param, t1] 

def build_log(X_train,y_train):
    log = LogisticRegression(C = 1)
    log.fit(X_train, y_train)
    pickle.dump(log,open('../Model/log_model.sav','wb'))
    
def build_rf(X_train,y_train):
    rf = RandomForestClassifier(n_estimators = 400,
                                max_depth = 20,
                                min_samples_leaf = 6)
    rf.fit(X_train,y_train)
    pickle.dump(rf,open('../Model/rf_model.sav','wb'))
    
    
def build_svc(X_train,y_train):
    svc = SVC(C = 1, kernel = 'rbf', gamma = 'scale')
    svc.fit(X_train,y_train)
    pickle.dump(svc,open('../Model/svc_model.sav','wb'))
    
def build_ann(X_train,y_train):
    ANN = Sequential()
    ANN.add(
            Dense(
                     units = 1000,
                     kernel_initializer = 'uniform', 
                     activation = 'relu',
                     input_dim=2000)
              )
    ANN.add(
            Dense(
                     units = 1000,
                     kernel_initializer = 'uniform', 
                     activation = 'relu'
                    )
              )
    ANN.add(
            Dense(
                     units = 1,
                     kernel_initializer = 'uniform', 
                     activation = 'sigmoid'
                    )
              )    
    ANN.compile(optimizer='adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    ANN.fit(np.array(X_train), np.array(y_train), batch_size = 10, epochs = 10)
    ANN.save_weights('../Model/ann_model_weights.h5')

#
#build_log(X_train, y_train)    
#build_rf(X_train,y_train)
#build_svc(X_train,y_train)
#build_ann()




def call_log():
    return pickle.load(open('../Model/log_model.sav','rb'))
def call_svc():
    return pickle.load(open('../Model/svc_model.sav','rb'))
def call_rf():
    return pickle.load(open('../Model/rf_model.sav','rb'))

def call_ann():
    ANN = Sequential()
    ANN.add(
            Dense(
                     units = 1000,
                     kernel_initializer = 'uniform', 
                     activation = 'relu',
                     input_dim=2000)
              )
    ANN.add(
            Dense(
                     units = 1000,
                     kernel_initializer = 'uniform', 
                     activation = 'relu'
                    )
              )
    ANN.add(
            Dense(
                     units = 1,
                     kernel_initializer = 'uniform', 
                     activation = 'sigmoid'
                    )
              )    
    ANN.compile(optimizer='adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    ANN.load_weights('../Model/ANN_model_weights.h5')
    return ANN
#
#xx = call_log().score(X_test,y_test)
#xx

def findmisclass(df, pred,y_test):
    dtest = df.loc[y_test.index,:]
    dtest['pred'] = [int(i) for i in pred]
    ind = []
    for i in dtest.index:
        if dtest.loc[i,'relevant'] != dtest.loc[i,'pred']:
            ind.append(i)
    return dtest.loc[ind,:]

    







