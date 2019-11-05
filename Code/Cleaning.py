#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:44:04 2019

@author: xiaohezhang
"""
#!pip install emoji
#!pip install emot --upgrade

import pandas as pd
import re
from nltk.stem.porter import PorterStemmer
import datetime
import reverse_geocoder as rg 
import emoji

#cafire_origin = pd.read_csv('./data/california_wildfires_final_data.csv')
#kaggle_origin = pd.read_csv('./data/kaggle.csv')

stem = PorterStemmer()

def textclean(x):
    x = re.sub(r"http\S+", "", x).lower()
    x = re.sub(r"@\S+", '',x)
    x = emoji.demojize(x)
    x = re.sub("[^a-zA-Z0-9_]", " ", x)
    x = stem.stem(x)
    return x

def fetchurl(x):
    try: return 'https://t.co/'+x.split('https://t.co/')[1]
    except: return 0


def confident(trainset):
    trainset['confident'] = trainset['confident'].map(lambda x: 1 if x>0.5 else 0)
    trainset[trainset['confident'] == 0]['relevant'] = 1-trainset[trainset['confident'] == 0]['relevant']
    trainset['relevant'].dropna(inplace = True)
    trainset['relevant'] = trainset['relevant'].astype(int)
    trainset.drop('confident', axis = 1,inplace = True)
    return trainset



def combine_train():    
    cafire_origin = pd.read_csv('../data/california_wildfires_final_data.csv')
    kaggle_origin = pd.read_csv('../data/kaggle.csv')
    trainfire = cafire_origin[['text_human','text_human_conf','tweet_text']]
    kaggle = kaggle_origin[['choose_one','choose_one:confidence','text']]

    trainfire.columns = ['relevant','confident','text']
    kaggle.columns = ['relevant','confident','text']

    trainfire['relevant'] = trainfire['relevant'].map({'other_relevant_information':1,
                            'rescue_volunteering_or_donation_effort':1,
                            'infrastructure_and_utility_damage':1,
                            'injured_or_dead_people':1,
                            'affected_individuals':1,
                            'missing_or_found_people':1,
                            'vehicle_damage':1,
                            'not_relevant_or_cant_judge':1})
    trainfire['relevant'].fillna(0, inplace = True)
    trainfire['confident'].fillna(1, inplace = True)

    kaggle['relevant'] = kaggle['relevant'].map({'Relevant':1,'Not Relevant':0})
    kagglefire = kaggle[['fire' in kaggle.loc[i,'text'] for i in range(len(kaggle))]]
    kagglefire.fillna(0, inplace = True)

    misclass = kaggle[kaggle['relevant'] == 0.0] 
    trainset = pd.concat([misclass,kagglefire,trainfire], axis = 0)
    trainset['index'] = list(range(len(trainset)))
    trainset.set_index('index', inplace = True)
    trainset['text'] = trainset['text'].map(lambda x: textclean(x))
    trainset = confident(trainset)
    return trainset


def get_geo(df):
    li = []
    for i in df.index:
        li.append((df.loc[i,'Latitude'],df.loc[i,'Longitude']))
    df['coor'] = rg.search(li)  
    for i in df.index:
        df.loc[i,'name'] = df.loc[i,'coor']['name']
        df.loc[i,'country'] = df.loc[i,'coor']['cc']
        df.loc[i,'state'] = df.loc[i,'coor']['admin1']
    return df[df['country'] == 'US']

def cleantest(df):
    df.fillna(0,inplace = True)
    df['Longitude'] = df.locationcoor.map(lambda x: float(x.split(',')[1]))
    df['Latitude'] = df.locationcoor.map(lambda x: float(x.split(',')[0]))
    for i in df.index:
        if  df.loc[i,'location'] == 0:
            df.loc[i,'twlong'] = df.loc[i,'Longitude'] 
            df.loc[i,'twlat'] = df.loc[i,'Latitude']
        else:
            df.loc[i,'twlong'] = df.loc[i,'location'].split(':')[2].split('}')[0].split('[')[1].split(']')[0].split(',')[1]
            df.loc[i,'twlat'] = df.loc[i,'location'].split(':')[2].split('}')[0].split('[')[1].split(']')[0].split(',')[0]
    return df


def today():
    return datetime.datetime.today().strftime('%Y%m%d')

def combine_test(date):
#    df = pd.concat([df1,df2],axis = 0)

    filename = f'../data/{date}firedata.csv'
    df = pd.read_csv(filename)
    df.drop('Unnamed: 0', axis = 1, inplace = True)

    df['index'] = list(range(df.shape[0]))
    df.set_index('index', inplace=True)
    df = cleantest(df)
    df = get_geo(df)
    df['url'] = df['text'].map(fetchurl)
    df['text'] = df['text'].map(lambda x: textclean(x))
    return df.drop(['locationcoor','location'], axis = 1)


#stop = stopwords.words('english') + ["http",'https', "co",'amp', 'california']

#cloudfire = ''
#for i in trainset.index:
#    if trainset.loc[i,'relevant'] == 1.0:
#        cloudfire = cloudfire + ' ' + trainset.loc[i,'text'].lower()
#        
#        
#cloudnone = ''
#for i in trainset.index:
#    if trainset.loc[i,'relevant'] == 0.0:
#        cloudnone = cloudnone + ' ' + trainset.loc[i,'text'].lower()
#        
#plt.figure(figsize = (13,10))
#wordcloud = WordCloud(stopwords= stop, width = 800, height=400, ranks_only= 200, background_color='white').generate(cloudfire)
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")
#plt.show()
#
#plt.figure(figsize = (13,10))
#wordcloud = WordCloud(stopwords= stop, width = 800, height=400, ranks_only= 200,background_color='white').generate(cloudnone)
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")
#plt.show()










