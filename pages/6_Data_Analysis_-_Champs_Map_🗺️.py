import folium
import pandas as pd
import streamlit as st

from folium.plugins import HeatMap
from streamlit_folium import st_folium

purpose_colour = {'3Ds': 'blue',
                  'Nationals': 'purple'}

st.set_page_config(layout='wide')
st.sidebar.success('Select a page above.')

st.header("Champs Map 🗺️")

st.markdown("""Where have all the champs been held? Are they evenly distributed, or concentrated in one area?""")

df = pd.read_csv('NFAS Locations.csv')
df['Year'] = df['Year'].astype(str)
df['Champs Year'] = df['Champs'] + ': ' + df['Year'] + ': ' + df['Site']

m = folium.Map(location=[df.Latitude.mean(), df.Longitude.mean()], tiles='CartoDB positron',
               zoom_start=6, control_scale=True)

# Loop through each row in the dataframe
for i, row in df.iterrows():
    iframe = folium.IFrame(str(row["Champs Year"]))

    # Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=200, max_width=300)

    try:
        icon_color = purpose_colour[row['Champs']]
    except:
        icon_color = 'gray'

    # Add each row to the map
    folium.Marker(location=[row['Latitude'], row['Longitude']],
                  popup=popup,
                  icon=folium.Icon(color=icon_color),
                  c=row['Champs Year']).add_to(m)

grouped = df.groupby(['Latitude', 'Longitude']).size().reset_index(name='Count')

map_values1 = grouped[['Latitude', 'Longitude', 'Count']]

data = map_values1.values.tolist()

hm = HeatMap(data, gradient={0.1: 'blue', 0.3: 'lime', 0.5: 'yellow', 0.7: 'orange', 1: 'red'},
             min_opacity=0.05,
             max_opacity=0.9,
             radius=20,
             use_local_extrema=False)  # .add_to(base_map)

# base_map
m.add_child(hm)
st_data = st_folium(m, width=1000)

st.markdown("""This pin map with heatmap behind it does show there has been quite a concentration of competitions in the
            middle of the country. These have been heavily focused around Nottingham.""")
