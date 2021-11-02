import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_lottie import st_lottie
import requests
import geopandas as gpd
from streamlit_folium import folium_static
import folium
import branca.colormap as cm

###############################################################################################

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_book = load_lottieurl('https://assets9.lottiefiles.com/temp/lf20_aKAfIn.json')
st_lottie(lottie_book, height=200)

st.title('RPMS Enrollment Statistics')

# status_text = st.sidebar.empty()

options = st.multiselect(
    'Include in chart:',
    ['All','White','Asian', 'Latino','African American','Unknown'])
###############################################################################################
# st.header('School Demograpics')

df = pd.read_csv('data/Historical Demographic Data.csv')

# Show total, white, non-white, indivdual groups over time
fig = px.bar(df, x='Year', y=['White','Asian', 'Latino','African American','Unknown'], title="Enrollment by Demographic",
             labels={
                 "value": "Enrollment",
                 "Year": "School Year",
                 "variable": "Race/Ethnicity"
             }, height=600, width=900)
st.plotly_chart(fig)


# race/ethnicity by program
###############################################################################################
col1, col2, col3, col4 = st.columns(4)
col1.metric("Asian", "70 °F", "1.2 °F")
col2.metric("Latino", "9 mph", "-8%")
col3.metric("African American", "86%", "4%")
col4.metric("Non-White", "86%", "4%")
###############################################################################################

st.header('Area Demographics')
# view neighborhood, city by income, different groups, stats

# reading in the polygon shapefile
chi_zips = gpd.read_file(r"Boundaries - ZIP Codes/geo_export_a9707f61-f834-4e7b-b8a5-0f0ff4c8412d.shp")
x_map=chi_zips.centroid.x.mean()
y_map=chi_zips.centroid.y.mean()+.01

mymap = folium.Map(location=[y_map, x_map], zoom_start=10,tiles=None)
folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
# folium_static(mymap)

area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
chi_zips = pd.merge(chi_zips, area_stats, how='left', on='zip')

mymap.choropleth(
 geo_data=chi_zips,
 name='Choropleth',
 data=chi_zips,
 columns=['zip','latino_pop'],
 key_on="feature.properties.zip",
#  fill_color='YlGnBu',
#  fill_opacity=1,
 line_opacity=0.2,
 legend_name='Latino population in %',
 smooth_factor=0
)
folium_static(mymap)