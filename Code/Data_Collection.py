#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:43:56 2019

@author: xiaohezhang
"""


import pandas as pd
import time
import datetime
import progressbar
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:@localhost/twitter')

import twitter
api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='-',
                  access_token_secret='')

#print(api.VerifyCredentials())

def create_table(x):
    result = {
        'created':[],
        'text':[],
        'latitude':[],
        'longitude':[],
    }
    for i in range(len(x)):
        result['created'].append(pd.Timestamp(x[i].created_at_in_seconds, unit='s'))
        result['text'].append(x[i].text)
        try: result['latitude'].append(x[i].geo['coordinates'][0])
        except: result['latitude'].append(0)
        try: result['longitude'].append(x[i].geo['coordinates'][1])
        except: result['longitude'].append(0)
    return pd.DataFrame(result, columns = ['created','text','latitude','longitude'])

def get_data(term = None, since = None, until = None, geocode = None,):
    output = pd.DataFrame()
    for i in range(1):
        search = api.GetSearch(term, since = since, until = until, geocode = geocode, lang='en',count = 100)
        output = pd.concat([output, create_table(search)], axis = 0)
        time.sleep(5.1)
    return output

def livefire():
    url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv"
    df = pd.read_csv(url)
    df.rename({'latitude':'Latitude','longitude':'Longitude'}, inplace = True, axis = 1)
    return df[df['confidence']>=50]

def shrinkfire():
    df = livefire()
    for i in df.index:
        df.loc[i,'time'] = pd.to_datetime(str(df.loc[i,'acq_date'])+'-'+ str(df.loc[i,'acq_time']),format='%Y-%m-%d-%H%M')
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    df[df['acq_date'] == today]
    df['hour'] = df['acq_time'].map(lambda x: int(x/100))
    return df


def searchfire(dfc,radia = 5):
    coordinates = {'loc':[],
                   'time':[]}
    result = pd.DataFrame()
    for i in dfc.index:
        coordinates['loc'].append(f"{dfc.loc[i,'Latitude']},{dfc.loc[i,'Longitude']},{radia}mi")
        coordinates['time'].append(dfc.loc[i,'time'])
    bar = progressbar.ProgressBar(maxval=len(coordinates['loc']), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for j in range(len(coordinates['loc'])):
        dfj = get_data(geocode=coordinates['loc'][j],since = coordinates['time'][j].date().strftime('%Y%m%d'))
        dfj['locationcoor'] = coordinates['loc'][j]
        dfj['collected_time'] = coordinates['time'][j]
        dfj.to_sql('alltwitter',con = engine, if_exists = 'append', index = False)
        result = pd.concat([result,dfj], axis = 0)
        bar.update(j+1)
    bar.finish()
    return result


def execute():
    df = livefire()
    firetweet = searchfire(df,radia = 10)
    return firetweet

def save(firetweet):
    date = datetime.datetime.today().strftime('%Y%m%d')
    filename = f'../data/{date}firedata.csv'
    firetweet.to_csv(filename)
