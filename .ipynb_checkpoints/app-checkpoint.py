import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_lottie import st_lottie
import requests
import geopandas as gpd
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster


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
password_guess = st.text_input('What is the Password?', type="password")
if password_guess != st.secrets["password"]:
    st.stop()

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

st.subheader('2022-2023')

col1, col2, col3, col4, col5= st.columns(5)
col1.metric("Asian", "38", "-2")
col2.metric("African American", "9", "0")
col3.metric("Latino", "28", "-5")
col4.metric("Multi-racial", "17", "7")
col5.metric("Non-White", "92", "0")
###############################################################################################
st.markdown('---')

st.subheader('Enrollment Demographics - Percent')

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
st.subheader('2022-2023')

col1, col2, col3, col4, col5= st.columns(5)
col1.metric("Asian", "11 %", "0 %")
col2.metric("African American", "2.6 %", "0 %")
col3.metric("Latino", "8.1 %", "1 %")
col4.metric("Multi-racial", "5 %", "3 %")
col5.metric("Non-White", "26.2 %", ".43 %")
###############################################################################################
st.markdown('---')
st.subheader('Enrollment Demographics by Program')

# df = pd.read_csv('data/final_student_list.csv')
df = pd.read_csv('data/2022/2022_student_list.csv')
# Show total, white, non-white, individual groups over time
# options3 = ['Toddler','Childrens House 3YO','Childrens House 4YO','Kindergarten', 'First', 'Second',  'Third', 'Fourth','Fifth','Sixth','Seventh', 'Eighth']
fig3 = px.histogram(df, x='Current Grade', color='ethnicity',
             title="Enrollment by Program",
             labels={
                 "value": "Enrollment",
                 "Year": "School Year",
                 "variable": "Race/Ethnicity"
             },
               height=600, width=900)
fig3.update_xaxes(categoryorder='array', categoryarray= ['Toddler',"Children's House 3YO","Children's House 4YO",'Kindergarten', 'First', 'Second',  'Third', 'Fourth','Fifth','Sixth','Seventh', 'Eighth'])

st.plotly_chart(fig3)

###############################################################################################

st.markdown('---')
st.header('Area Demographics')
# view neighborhood, city by income, different groups, stats

# reading in the polygon shapefile
chi_zips = gpd.read_file(r"Boundaries - ZIP Codes/geo_export_a9707f61-f834-4e7b-b8a5-0f0ff4c8412d.shp")
x_map=chi_zips.centroid.x.mean()
y_map=chi_zips.centroid.y.mean()-.02

mymap = folium.Map(location=[y_map, x_map], zoom_start=11,tiles=None)
folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
# folium_static(mymap)

# area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
area_stats = pd.read_csv('data/zip_demos.csv', dtype={'zip':str})
chi_zips = pd.merge(chi_zips, area_stats, how='left', on='zip')
# st.write(chi_zips.head())
demos = ['White', "Black", "Latino", "Asian"]

demo = st.selectbox(
   'Select demographic',
   demos)

st.subheader(f'{demo} population in %')

view_students = st.checkbox('View Student Locations')
# st.write(chi_zips.head)
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

# add point for RPMS
cluster = MarkerCluster().add_to(mymap)
style_function = "font-size: 15px; font-weight: bold"
folium.Marker(location=[41.980250,-87.675000], tooltip = "<h3>RPMS</h3>", popup = 'RPMS', style=style_function).add_to(cluster)

# add points for student locations
if view_students:
    student_locations = pd.read_csv('data/2022/student_locations_2022.csv')
    locationlist = student_locations.values.tolist()
    marker_cluster = MarkerCluster().add_to(mymap)
    for point in range(0, len(locationlist)):
        folium.Marker(locationlist[point]).add_to(marker_cluster)

# add labels indicating the name of the community
style_function = "font-size: 15px; font-weight: bold"
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['zip'], style=style_function, labels=False))

# create a layer control
folium.LayerControl().add_to(mymap)


folium_static(mymap, width=750, height=850)

# Summary Data for 60640

st.markdown('#### Demographics for Lincoln Square')
col1, col2, col3, col4= st.columns(4)
col1.metric("Asian", "12.8 %")
col2.metric("Black", "5.5 %")
col3.metric("Latino", "21.11 %")
col4.metric("White", "60.2 %")

st.markdown('#### Demographics for Edgewater')
col1, col2, col3, col4= st.columns(4)
col1.metric("Asian", "9.6 %")
col2.metric("Black", "10.2 %")
col3.metric("Latino", "17 %")
col4.metric("White", "62.6 %")

st.markdown('#### Demographics for Ravenswood')
col1, col2, col3, col4= st.columns(4)
col1.metric("Asian", "7.8 %")
col2.metric("Black", "3.1 %")
col3.metric("Latino", "20.7 %")
col4.metric("White", "67.9 %")