import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_lottie import st_lottie
import requests


###############################################################################################

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_book = load_lottieurl('https://assets9.lottiefiles.com/temp/lf20_aKAfIn.json')
st_lottie(lottie_book, height=200)

st.title('RPMS Enrollment Statistics')

status_text = st.sidebar.empty()

options = st.sidebar.multiselect(
    'Include in chart:',
    ['All','White','Asian', 'Latino','African American','Unknown'])
###############################################################################################
st.header('School Demograpics')

df = pd.read_csv('data/Historical Demographic Data.csv')

# Show total, white, non-white, indivdual groups over time
fig = px.bar(df, x='Year', y=['White','Asian', 'Latino','African American','Unknown'], title="Enrollment by Demographic",
             labels={
                 "value": "Enrollment",
                 "Year": "School Year",
                 "variable": "Race/Ethnicity"
             }, height=600, width=900)
st.plotly_chart(fig)

###############################################################################################
st.header('Area Demographics')
# view neighborhood, city by income, different groups, stats