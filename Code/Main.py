#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:43:55 2019

@author: xiaohezhang
"""
import pandas as pd
import Data_Collection
import Cleaning
import Modeling
import Visulization
import Map
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:@localhost/twitter')

Data_Collection.execute()

sql = "select * from 24h_twitter;"
dft = pd.read_sql_query(sql,con = engine)

date = '20191104'

#date = Cleaning.today()
test = Cleaning.combine_test(dft)

#train = Cleaning.combine_train()
#train.to_csv('../data/trainset.csv')
train = pd.read_csv('../data/trainset.csv')

#Visulization.mapping(test,2)

X_train, X_test, y_train, y_test, X_result = Modeling.prepare(train,test)


#Modeling.call_log().score(X_test,y_test)
#pred = Modeling.call_svc().predict(X_test)
#
#misclass = Modeling.findmisclass(train, pred, y_test)
#misclass.to_csv('../result/misclassify.csv')


test['relevant'] = Modeling.call_log().predict(X_train)
test['relevant'].value_counts()


test[test['relevant'] == 1]['text']
test.to_csv(f'../result/{date}fire.csv')

Map.mapping(date)
