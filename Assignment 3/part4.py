import plotly.express as px
import json
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
location_data = open('data/location_history.json')
location_dict = json.load(location_data)
location_list = location_dict["Location History"]

latitudelist = []
longitudelist = []
ziplist = []
latlong = ()
i = 0
for locations in location_list:
    string = locations["Latitude, Longitude"]
    comma = string.index(",")
    latitude = float(string[0:6])
    longitude = float(string[comma + 2:comma + 9])
    latitudelist.append(latitude)
    longitudelist.append(longitude)

latlong = pd.DataFrame({'lat':latitudelist, 'long':longitudelist})

import pandas as pd


import plotly.express as px
#https://plotly.com/python/lines-on-mapbox/
fig = px.line_mapbox(latlong, lat="lat", lon="long", zoom=1, height=300)
fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=12, mapbox_center_lat = 41.792, mapbox_center_lon =  -87.6,
    margin={"r":0,"t":0,"l":0,"b":0})
fig.write_image("pics/hydepark.png", scale = 5)


fig2 = px.line_mapbox(latlong, lat="lat", lon="long", zoom=1, height=300)
fig2.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat = 41.792, mapbox_center_lon =  -87.6,
    margin={"r":0,"t":0,"l":0,"b":0})
fig2.show()
fig2.write_image("pics/chicago.png", scale = 5)


fig3 = px.line_mapbox(latlong, lat="lat", lon="long", zoom=1, height=300)
fig3.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=0, mapbox_center_lat = 35, mapbox_center_lon =  0,
    margin={"r":0,"t":0,"l":0,"b":0})
fig3.show()
fig3.write_image("pics/world.png", scale = 5)
#print(results)


pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0,20, border = 1, ln = 1, txt='We know from where to where you traveled!', align = 'C')
pdf.set_font('Arial',size=12)
pdf.cell(0,20, ln=1, txt = "Let us show the route you took for your travel!!!")
pdf.cell(0,20, border = 1, ln=1, txt = "Hyde Park")
pdf.image("pics/hydepark.png", w=175, h=75)
pdf.cell(0,20, border = 1, ln=1, txt = "Chicago")
pdf.image("pics/chicago.png", w=175, h=75)
pdf.add_page()
pdf.cell(0,20, border = 1, ln=1, txt = "World")
pdf.image("pics/world.png", w=175, h=75)
pdf.output("data_fun_visualization_privacy.pdf")