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

    # set value for score in dictionary for selected risks
    # using timeline decide which risks are closed and probability

timeline = 20
phase = 'Planning'
phasenumber = st.session_state['plnlistphase']
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

def calculate_risks_json(risks):
   for d in risks:
        d['riskselect'] = 'Y'
        #  when phase exceeds timeline setting, then probability is 0, risk is closed
        if phasenumber > int( d['risktimeline'] ):
           d['riskprobability'] = '0'
        # timeframe when risk will have an impact
        # the risk probablility can be 0 when risk has elapsed
        if d['risktimeline'] > '4':
           d['riskselect'] = 'Y'
        if d['risktimeline'] < '5' and timeline < 90:
           d['riskselect'] = 'Y'
        if d['risktimeline'] < '3' and timeline < 50:
           d['riskselect'] = 'Y'

   selectedrisks = [d for d in risks if d['riskselect'] == 'Y']
           
    #  set the score value and count scores and risktable
   for d in selectedrisks:
        if d['riskimpact'] == '3' and d['riskprobability'] == '3':
           d['riskscore'] = 'Highest'
        if d['riskimpact'] == '1' and d['riskprobability'] == '3':
           d['riskscore'] = 'Moderate'
        if d['riskimpact'] == '3' and d['riskprobability'] == '1':
           d['riskscore'] = 'Moderate'
        if d['riskimpact'] == '1' and d['riskprobability'] == '1':
           d['riskscore'] = 'Lowest'
        if d['riskimpact'] == '3' and d['riskprobability'] == '2':
           d['riskscore'] = '4'
        if d['riskimpact'] == '1' and d['riskprobability'] == '2':
           d['riskscore'] = '2'
        if d['riskimpact'] == '2' and d['riskprobability'] == '1':
           d['riskscore'] = '2'
        if d['riskimpact'] == '2' and d['riskprobability'] == '3':
           d['riskscore'] = '4'
        if d['riskimpact'] == '2' and d['riskprobability'] == '2':
           d['riskscore'] = 'Moderate'
        if d['riskprobability'] == '0':
           d['riskscore'] = 'Closed'
        if d['riskimpact'] == '' and d['riskprobability'] == '':
           d['riskimpact'] = '2'
           d['riskscore'] = 'Moderate'
        return(selectedrisks) 

if 'plpnumber' not in st.session_state:
     st.error('Please enter a plan')

reporttitle("Risk Analysis", st.session_state['thepmheader'])

with st.container():
     startrisks = getrisks()
     startframe = pd.DataFrame.from_dict(startrisks, orient="columns")
     myrisks = calculate_risks_json(startrisks)
     dataframe = pd.DataFrame.from_dict(myrisks, orient="columns")
     groupscore = dataframe.groupby(['riskscore', 'risktype']).size().groupby(level=1).max()

     totalmetric = startframe.shape[0]
     startmetric1 = len(startframe['riskprobability'] == '1')
     endmetric1 = len(dataframe['riskprobability'] == '2')
     startmetric2 = len(startframe['riskimpact'] == '3')
     endmetric2 = len(dataframe['riskimpact'] == '3')
     startmetric3 = len(startframe['riskprobability'] == '3')
     endmetric3 = len(dataframe['riskprobability'] == '3')
     startmetric4 = len(startframe['riskresponse'] == 'Avoid')
     endmetric4 = len(dataframe['riskresponse'] == 'Avoid')
     endmetric5 = sum(dataframe['riskprobability'] == '0')
     startmetric5 = int(totalmetric - endmetric5) 

     col1, col2, col3, col4, col5 = st.columns(5)
     col1.metric("Low", endmetric1, startmetric1)
     col2.metric("Impact", endmetric2, startmetric2)
     col3.metric("Issues", endmetric3, startmetric3)
     col4.metric("Avoid", endmetric4, startmetric4)
     col5.metric("Closed", endmetric5, startmetric5)

     # st.table(dataframe)
     charttype = dataframe['risktype'].value_counts()
     chartscore = dataframe['riskscore'].value_counts()
     chartowner = dataframe['riskowner'].value_counts()
     chartresponse = dataframe['riskresponse'].value_counts()
     st.header("Risk by group Score")
     st.bar_chart(groupscore)
     st.header("Risk by Type and Impact")
     c = alt.Chart(dataframe).mark_bar().encode(
       x='risktype',
       y='count(riskimpact)',
       color='riskimpact'
     )
     st.altair_chart(c, use_container_width=True)

     st.header("Risk by Owner and Impact")
     d = alt.Chart(dataframe).mark_bar().encode(
       x='riskowner',
       y='count(riskscore)',
       color='riskscore'
     )
     st.altair_chart(d, use_container_width=True)

     st.header("Risk by Probability and Response")
     e = alt.Chart(dataframe).mark_bar().encode(
       x='riskresponse',
       y='count(riskscore)',
       color='riskprobability'
     )
     st.altair_chart(e, use_container_width=True)

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
     
     df = dataframe

     grid_response = AgGrid(
        dataframe,
        editable=True,
        height=300,
        )

     updated = grid_response['data']
     df = pd.DataFrame(updated)

