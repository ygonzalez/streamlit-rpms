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
st.title('RPMS Enrollment Statistics')

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_book = load_lottieurl('https://assets9.lottiefiles.com/temp/lf20_aKAfIn.json')
st_lottie(lottie_book, height=200)

# status_text = st.sidebar.empty()
st.write(st.secrets["password"])
# password_guess = st.text_input('What is the Password?')
# if password_guess != st.secrets["password"]:
#     st.stop()

###############################################################################################
# st.header('Enrollment Demograpics')

df = pd.read_csv('data/Historical Demographic Data.csv')
st.subheader('Enrollment Demographics - Raw Counts')
options = st.multiselect(
    'Include in chart:',
    ['White','Asian', 'Latino','African American','Multi-racial','Prefer Not To Answer'],
    default = ['White','Asian', 'Latino','African American','Multi-racial','Prefer Not To Answer']
)
# Show total, white, non-white, individual groups over time
fig = px.bar(df, x='Year', y=options,
             title="Enrollment by Demographic - Raw Counts",
             labels={
                 "value": "Enrollment",
                 "Year": "School Year",
                 "variable": "Race/Ethnicity"
             }, height=600, width=900)
st.plotly_chart(fig)

st.subheader('2021-2022')

col1, col2, col3, col4, col5= st.columns(5)
col1.metric("Asian", "40", "-5")
col2.metric("African American", "9", "-1")
col3.metric("Latino", "33", "-5")
col4.metric("Multi-racial", "10", "10")
col5.metric("Non-White", "92", "0")
###############################################################################################
st.markdown('---')

st.subheader('Enrollment Demographics - %')

options2 = st.multiselect(
    'Include in chart:',
    ['White %','Asian %', 'Latino %','African American %','Multi-racial %'],
    default = ['White %','Asian %', 'Latino %','African American %','Multi-racial %']
)
# Show total, white, non-white, individual groups over time
fig2 = px.bar(df, x='Year', y=options2,
             title="Enrollment by Demographic - %",
             labels={
                 "value": "Enrollment",
                 "Year": "School Year",
                 "variable": "Race/Ethnicity"
             }, height=600, width=900)
st.plotly_chart(fig2)
# race/ethnicity by program
###############################################################################################
st.subheader('2021-2022')

col1, col2, col3, col4, col5= st.columns(5)
col1.metric("Asian", "11.2 %", "-2.3 %")
col2.metric("African American", "2.53 %", "-0.48 %")
col3.metric("Latino", "9.24 %", "-1.87 %")
col4.metric("Multi-racial", "2.8 %", "2.8 %")
col5.metric("Non-White", "25.77 %", "-1.83 %")
###############################################################################################
st.markdown('---')
st.header('Area Demographics')
# view neighborhood, city by income, different groups, stats

# reading in the polygon shapefile
chi_zips = gpd.read_file(r"Boundaries - ZIP Codes/geo_export_a9707f61-f834-4e7b-b8a5-0f0ff4c8412d.shp")
x_map=chi_zips.centroid.x.mean()
y_map=chi_zips.centroid.y.mean()+.01

mymap = folium.Map(location=[y_map, x_map], zoom_start=10,tiles=None)
folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
# folium_static(mymap)

# area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
area_stats = pd.read_csv('data/zip_demos.csv', dtype={'zip':str})
chi_zips = pd.merge(chi_zips, area_stats, how='left', on='zip')

demos = ['White', "Black", "Latino", "Asian"]

demo = st.selectbox(
   'Select demographic',
   demos)

st.subheader(f'{demo} population in %')

choropleth = folium.Choropleth(
 geo_data=chi_zips,
 name='Choropleth',
 data=chi_zips,
 columns=['zip',demo],
 key_on="feature.properties.zip",
#  fill_color='YlGnBu',
    line_weight=1,
 legend_name=f'{demo} population in %',
 smooth_factor=0
).add_to(mymap)


# add labels indicating the name of the community
style_function = "font-size: 15px; font-weight: bold"
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['zip'], style=style_function, labels=False))

# create a layer control
folium.LayerControl().add_to(mymap)


folium_static(mymap)
