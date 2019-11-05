
import pandas as pd
import folium
from folium.plugins import MeasureControl

#!pip install reverse_geocoder
#df = pd.read_csv('../result/20191101fire.csv')
states = '../data/us-states.json'
statename = pd.read_json('../data/state.json')

def readfile(date):
    filename = f'../result/{date}fire.csv'
    df = pd.read_csv(filename)
    return df


def mapping(date):
    df = readfile(date)
    # create empty map zoomed in on San Francisco
    m = folium.Map( location = (39,-98), zoom_start = 4)
    folium.TileLayer('openstreetmap').add_to(m)
    
    cluster1 = folium.plugins.MarkerCluster(name="Not Relevant").add_to(m)
    cluster2 = folium.plugins.MarkerCluster(name="Relevant").add_to(m)
    
    # add a marker for every record in the filtered data, use a clustered view
    for i in df.index:
        if df.loc[i,'relevant'] == 0:
            tweet = df.loc[i,'text']
            location = (df.loc[i,'twlong'],df.loc[i,'twlat'])
            state = df.loc[i,'state']
            county = df.loc[i,'name']
            url = df.loc[i,'url']
            folium.Marker(location = [df.loc[i,'twlat'],df.loc[i,'twlong']],
                          popup='<b>Tweet: </b>%s<br></br><b>Location: </b>%s<br></br><b>State: </b>%s<br></br><b>County: </b>%s<br></br><b>URL: </b><a href="%s" target="_blank">%s</a>'%(tweet,location,state,county,url,url),
                          icon = folium.Icon(icon = 'fire',color='red')).add_to(cluster1)
    
        elif df.loc[i,'relevant'] == 1:
            tweet = df.loc[i,'text']
            location = (df.loc[i,'twlong'],df.loc[i,'twlat'])
            state = df.loc[i,'state']
            county = df.loc[i,'name']
            url = df.loc[i,'url']
            folium.Marker(location = [df.loc[i,'twlat'],df.loc[i,'twlong']],
                          popup='<b>Tweet: </b>%s<br></br><b>Location: </b>%s<br></br><b>State: </b>%s<br></br><b>County: </b>%s<br></br><b>URL: </b><a href="%s" target="_blank">%s</a>'%(tweet,location,state,county,url,url),
                          icon = folium.Icon(icon = 'fire',color='red')).add_to(cluster2)
    
    # add circle for searching
    #for j in df.index:
    #    folium.CircleMarker(location = [df.loc[j,'Latitude'],df.loc[j,'Longitude']],
    #                        radius = 10,
    #                        color = '#FF0000',
    #                        fill = True,
    #                        fill_color = '#FF0000').add_to(m)
      
    statedf = pd.DataFrame()
    ind = df[['Latitude','Longitude']].drop_duplicates().index
    df.loc[ind,'state'].value_counts()
    statedf['state'] = df.loc[ind,'state'].value_counts().index
    statedf['value'] = df.loc[ind,'state'].value_counts().values
    statedf
    wholestate = statename.merge(statedf, left_on = 'name', right_on = 'state', how = 'left').drop(['state','abbreviation'],axis = 1).fillna(0)
    
    
    m.choropleth(
            geo_data = states,
            name= '# of Fire detected',
            data = wholestate,
            columns = ['name','value'],
            key_on = 'feature.properties.name',
            fill_color = 'YlOrRd',
            fill_opacity = 0.7,
            line_opacotu = 0.2,
            legend_name = 'Fire Count',
            )
    
    
    folium.LayerControl().add_to(m)
    m.add_child(MeasureControl())
    
    filepath = f'../{date}map.html'
    m.save(filepath)
