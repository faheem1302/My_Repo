#Import Libraries
import paho.mqtt.client as mqtt
from tkinter import *
import time
import json
import folium
from folium import plugins
import datetime
import branca
from branca import colormap
import pandas as pd
from scipy import stats
import numpy as np
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pymysql

#Mosquitto Subscriber
def on_connect(client, userdata, flags, rc):
  client.subscribe("Eziosense")

def on_message(client, userdata, msg):
   json_string=msg.payload.decode()
   parsed_json=(json.loads(json_string))

#Database Login details
host="10.194.65.20"
port = 3306
db = "Eziosense"
user = "botlab"
password = "password"

#Connecting to Database
conn = pymysql.connect(host,user=user,port=port,passwd=password,db=db)
cord = pd.read_sql("select* from devicedetails;",conn)
#Mean Latitude and Longitude 
mean_lat = cord['lat'].mean()
mean_lon = cord['lon'].mean()    
'''
def fancy_html(row):
    i = row
    Date = datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')
    left_col_colour = "#2A799C"
    right_col_colour = "#C5DCE7"
    
    html = """<!DOCTYPE html>
<html style="margin-bottom:0">
<head>
<h4 style="margin-bottom:0"; width="300px"></h4>"""'PM Monitoring Device' + """
</head>
    <table style="height: 126px; width: 300px;">
<tbody>
<div>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Date</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Date) + """
</tr>
<tr>
</div>
</tbody>
</table>
</html>
"""
    return html
'''
#HEAT MAP
#Tile Layer Type and Attributions
attr = ('Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
)
tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.p'
kanton_map = folium.Map(location=[mean_lat, mean_lon], zoom_start=17)

#Add Minimap
minimap = plugins.MiniMap(toggle_display=True,tile_layer='Stamen Terrain')
kanton_map.add_child(minimap)

#Add FullScreen
plugins.Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    force_separate_button=True).add_to(kanton_map)

    
#creating a Marker for each point in the above table. Each point will get a popup with their zip
for row in cord.itertuples():
    #html1 = fancy_html(row)
    #iframe = branca.element.IFrame(html=html1,width=400,height=300)
    #popup = folium.Popup(iframe,parse_html=True)
    kanton_map.add_child(folium.Marker(location=[row.lat,row.lon],popup=[row.location_area]))

'''
#Applying HTML Visualization to all Markers
for i in range(0,len(cord)):
    html = fancy_html(i)
 
    iframe = branca.element.IFrame(html=html,width=400,height=300)
    popup = folium.Popup(iframe,parse_html=True)
    
    folium.Marker([cord['lat'].iloc[i],cord['lon'].iloc[i]],
                  popup=popup,icon=folium.Icon(icon='info-sign')).add_to(kanton_map)


#Adding Gradient in Heat Map
from folium.plugins import HeatMap

colormap2 = {0.0:'yellow', 0.2 :'#fc0', 0.4:'#f90', 0.6:'#f60', 0.8:'#f30', 1.0: 'red'}
data = [[28.5432, 77.1932, 1],[28.5447, 77.1915,0.5],
        [28.5433, 77.1924,0.6],[28.5451, 77.1923,0.3],
        [28.5455, 77.1941,0.8],[28.545, 77.1904,0.5],
        [28.5453, 77.1922,0.6],[28.5454, 77.1922,0.3],
        [28.5458, 77.1965,0.8]]

#Heat Map
HeatMap(data, radius=20,gradient=colormap2).add_to(kanton_map)

#Defining Legend
colormap1 = branca.colormap.linear.YlOrRd_09.scale(0, 1).to_step(6)
colormap1.caption = 'Particulate Pollutant Levels(ug/m3)'
kanton_map.add_child(colormap1)
kanton_map
'''
#Saving Data in HTML file
kanton_map.save("/home/faheem/Desktop/Local_HeatMap123.html")

client = mqtt.Client()
client.connect("10.194.65.20",1883,60)
client.on_connect = on_connect
client.on_message = on_message
while True:
    client.loop()  