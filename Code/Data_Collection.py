#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:43:56 2019

@author: xiaohezhang
"""

# Import libaries
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import time
import datetime
from mpl_toolkits.basemap import Basemap
import progressbar


import twitter
api = twitter.Api(consumer_key='YfkfmWvtZAz7SS9GHRZzpleNc',
                  consumer_secret='O9sQl3eHtq6EMbKh5vsvLwaaiLXRKNVhfd50mb7yEa83LX6NPK',
                  access_token_key='2453541001-sJHmhzs9LD7y37FIJTuQQDMXEhybFpIqTGuEkHG',
                  access_token_secret='VR0tUAq74JTW5bmkKtyPwdjBBOkVMAV0eKBL8pU2wmMAm')

#print(api.VerifyCredentials())

def create_table(x):
    result = {
        'created':[],
        'text':[],
        'location':[],
        'hashtags':[]
    }
    for i in range(len(x)):
        result['created'].append(pd.Timestamp(x[i].created_at_in_seconds, unit='s'))
        result['text'].append(x[i].text)
        result['location'].append(x[i].geo)
        result['hashtags'].append(x[i].hashtags)
    return pd.DataFrame(result, columns = ['created','text','location','hashtags'])

def get_data(term = None, since = None, until = None, geocode = None,):
    output = pd.DataFrame()
    for i in range(1):
        search = api.GetSearch(term, since = since, until = until, geocode = geocode, lang='en',count = 100)
        output = pd.concat([output, create_table(search)], axis = 0)
        time.sleep(3)
#         print(f'Fetching data {(i+1)*100}')
    return output


def reset_today():
    url = 'https://satepsanone.nesdis.noaa.gov/pub/FIRE/HMS/KML/'
    today = datetime.datetime.today().strftime('%Y%m%d')
    return requests.get(url+f'fire{today}.kml').content

def livefire(x):
    soup = BeautifulSoup(x, 'lxml')
    raw = soup.find_all(['coordinates','description'])
    firecorr = []
    for i in range(0, len(raw),2):
        date = raw[i].text.split()[3] + raw[i].text.split()[5]
        cord = raw[i+1].text.split(',')[:-1]
        d1 = datetime.datetime(int(date[0:4]), 1, 1) + datetime.timedelta(int(date[4:7]) - 1)
        d2 = pd.to_datetime(d1)
        d2 = d2.replace(hour = int(date[7:9]), minute = int(date[9:11]))
        firecorr.append(list([d2])+cord)
    return pd.DataFrame(firecorr, columns = ['Time','Longitude','Latitude'])



def cleandf(df):
#     df.drop_duplicates('Time', inplace = True)
    df['Longitude'] = round(df['Longitude'].astype(float),3)
    df['Latitude'] = round(df['Latitude'].astype(float),3)
    df['Longituder'] = round(df['Longitude'].astype(float),0)
    df['Latituder'] = round(df['Latitude'].astype(float),0)
    df.drop_duplicates(['Longituder','Latituder'], inplace = True)
    df = df[(df['Longitude']<-60) | (df['Longitude']>-130)]
    df = df[(df['Latitude']<50) | (df['Latitude']>20)]
    df.drop(['Longituder','Latituder'], axis = 1, inplace = True)
    return df.sort_values('Time', ascending = False)

def mapping(dfc,i):
    plt.figure(figsize = (15,13))
    m = Basemap( projection = 'mill',
               llcrnrlat= 20,
               llcrnrlon= -130,
               urcrnrlat=50,
               urcrnrlon=-60,
               resolution='l')
    m.drawcoastlines()
    m.drawcountries(linewidth = 2)
    m.drawstates(color = 'b')
    x,y = m(list(dfc['Longitude']),list(dfc['Latitude']))
    x1,y1 = m(dfc.loc[i,'Longitude'],dfc.loc[i,'Latitude'])

    m.plot(x,y, 'X', markersize = 10, color = 'orange')
    m.plot(x1,y1, "*", markersize = 20, color = 'red')
    plt.title('Live Fire Map');
    
#mapping(dfc,dfc.index[4])
def searchfire(dfc,radia = 5):
    coordinates = []
    result = pd.DataFrame()
    for i in dfc.index:
        coordinates.append(f"{dfc.loc[i,'Latitude']},{dfc.loc[i,'Longitude']},{radia}mi")
    bar = progressbar.ProgressBar(maxval=len(coordinates), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for j in range(len(coordinates)):
        dfj = get_data(geocode=coordinates[j])
        dfj['locationcoor'] = coordinates[j]
        result = pd.concat([result,dfj], axis = 0)
        bar.update(j+1)
    bar.finish()
    return result


def execute():
    today = reset_today()
    df = livefire(today)
    dfc = cleandf(df)  
    firetweet = searchfire(dfc,radia = 10)
    return firetweet


def save(firetweet):
    date = datetime.datetime.today().strftime('%Y%m%d')
    filename = f'../data/{date}firedata.csv'
    firetweet.to_csv(filename)


# =============================================================================
# ur ="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.csv"
# data = pd.read_csv(ur)
# 
# data = data[['time','longitude','latitude']]
# data.columns = ['Time','Longitude','Latitude']
# x = searchfire(data)
# 
# x.iloc[:,-1]
# 
# new = x.merge(data, right_on = data.index, left_on = 'location#')
# new.columns
# 
# new[['text','Time','location','Longitude','Latitude']].to_csv('earthquake_testing.csv')
# =============================================================================
