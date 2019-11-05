# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

stop = stopwords.words('english') + ["http",'https', "co",'amp', 'california']

def wordcloud(df,relevant):
    cloudfire = ''
    for i in df.index:
        if df.loc[i,'relevant'] == relevant:
            cloudfire = cloudfire + ' ' + df.loc[i,'text'].lower()
    plt.figure(figsize = (13,10))
    wordcloud = WordCloud(stopwords= stop, width = 800, height=400, ranks_only= 200, background_color='white').generate(cloudfire)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def mapping(df,i):    
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
    x,y = m(list(df['Longitude']),list(df['Latitude']))
    x1,y1 = m(df.loc[i,'Longitude'], df.loc[i,'Latitude'])

    m.plot(x,y, 'X', markersize = 10, color = 'orange')
#    m.plot(x1,y1, "*", markersize = 20, color = 'red')
    plt.title('Live Fire Map');
    