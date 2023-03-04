"""Page for viewing the awesome Project risks"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
from risklist import getrisks
import pandas as pd
import altair as alt
from st_aggrid import AgGrid
from utilities import reporttitle
from riskgenerate import calculate_risks_json

    # set value for score in dictionary for selected risks
    # using timeline decide which risks are closed and probability

timeline = 20
phase = 'Planning'
engagementscoresponsor = 70
sentimentscoresponsor = 70
retentionscoresponsor = 70
engagementscoreteam = 80
sentimenttscoreteam = 80
engagementproductteam = 0
sentimenttproductteam = 0
engagementscoreuser = 0
sentimenttscoreuer = 0
CPI = 3
SPI = 4

    # with st.spinner("Loading  ..."):
if 'thepmheader' not in st.session_state:
     #st.session_state.plnumber = ""
     st.error('Please enter a plan')
reporttitle("Risk Analysis", st.session_state['thepmheader'])

phasenumber = st.session_state['plnlistphase']
with st.container():

     startrisks = getrisks()
     startframe = pd.DataFrame.from_dict(startrisks, orient="columns")
     st.write(phasenumber)
     myrisks = calculate_risks_json(startrisks, phasenumber)
     dataframe = pd.DataFrame.from_dict(myrisks, orient="columns")
     groupscore = dataframe.groupby(['riskscore', 'risktype']).size().groupby(level=1).max()

     startresponse = startframe['riskresponse'].value_counts()
     chartresponse = dataframe['riskresponse'].value_counts()
     chartprobability = dataframe['riskprobability'].value_counts()
     chartscore = dataframe['riskscore'].value_counts()
     totalrisks = len(startframe)
     #startmetric5 = startframe.riskselect.value_counts().checked
     startmetric4 = int(startresponse['Avoid'])
     endmetric4 = int(chartresponse['Avoid'])
     startmetric5 = sum(dataframe['riskselect'] == 'N')
     startmetric3 = sum(dataframe['riskprobability'] == '3')
     endmetric3 = sum(dataframe['riskprobability'] == 3)

     st.write(chartresponse)
     st.write(chartprobability)
     st.write(chartscore)
 
     col1, col2, col3, col4, col5 = st.columns(5)
     col1.metric("Highest", "70 °F", "1.2 °F")
     col2.metric("High", "9 mph", "-8%")
     col3.metric("Issues", int(endmetric3/startmetric3), endmetric3)
     col4.metric("Avoid", startmetric4, int(endmetric4/startmetric4))
     col5.metric("Closed", startmetric5, int(startmetric5/totalrisks))
 

     # st.table(dataframe)
     charttype = dataframe['risktype'].value_counts()
     chartscore = dataframe['riskscore'].value_counts()
     chartowner = dataframe['riskowner'].value_counts()

     st.subheader("Risk by group Score and Impact")
     st.bar_chart(groupscore)
     st.subheader("Risk by Type and Impact")
     c = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='risktype',
       y='count(riskimpact)',
       color='riskimpact'
     )
     st.altair_chart(c, use_container_width=True)

     st.subheader("Risk by Owner and Score")
     d = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskowner',
       y='count(riskscore)',
       color='riskscore'
     )
     st.altair_chart(d, use_container_width=True)

     st.subheader("Risk by Response and Score")
     e = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskresponse',
       y='count(riskscore)',
       color='riskprobability'
     )
     st.altair_chart(e, use_container_width=True)

     st.subheader("Heatmap Impact and Probability")
     heatmap = alt.Chart(dataframe).mark_rect().encode(
       alt.X('riskimpact'),
       alt.Y('riskprobability'),
       alt.Color('count()', scale=alt.Scale(scheme='redyellowblue'))
     )

     points = alt.Chart(dataframe).mark_circle(
       color='black',
       size=5,
     ).encode(
       x='riskimpact',
       y='riskprobability',
     )

     f = heatmap + points
     st.altair_chart(f, use_container_width=True)
     st.header("Risk Details")
     #st.write(dataframe)
     #st.json(myrisks)
     
     grid_response = AgGrid(
        dataframe,
        editable=False,
        height=300,
        )

     grid_response = AgGrid(
        startframe,
        editable=False,
        height=300,
        )
     #updated = grid_response['data']
     #df = pd.DataFrame(updated)

