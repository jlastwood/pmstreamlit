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
from PIL import Image

    # set value for score in dictionary for selected risks
    # using timeline decide which risks are closed and probability

engagementscoresponsor = 70
sentimentscoresponsor = 70
retentionscoresponsor = 70
engagementproductteam = 0
sentimenttproductteam = 0
engagementscoreuser = 0
sentimenttscoreuser = 0

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Risks",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)             
    # with st.spinner("Loading  ..."):
if 'thepmheader' not in st.session_state:
     st.error('Please enter a plan')
     st.stop()

reporttitle("Risk Analysis", st.session_state['thepmheader'])

# get values for profile
phasenumber = st.session_state.plnlistphase
CPI = st.session_state.thepmcpi
SPI = st.session_state.thepmspi
engagementscoreteam = st.session_state.plnactivesam
sentimentscoreteam = st.session_state.plnactiveses
# open roles or weeks with full team less than 3
retention = st.session_state.plnactiveses
scopechange = len(st.session_state.plscopechange.split("."))
if len(st.session_state.plscopechange) < 6:
   scopechange = 0
earnedvalue = st.session_state.plnactiveses
roi = st.session_state.plnactiveses
latestart = st.session_state.plnactiveses
inspectfail = st.session_state.plnactiveses

with st.container():

     startrisks = getrisks()
     startframe = pd.DataFrame.from_dict(startrisks, orient="columns")
     myrisks = calculate_risks_json(startrisks, phasenumber, SPI, CPI, engagementscoreteam, sentimentscoreteam, retention, scopechange, earnedvalue, roi, latestart, inspectfail)
     dataframe = pd.DataFrame.from_dict(myrisks, orient="columns")
     groupscore = dataframe.groupby(['riskimpact', 'risktype']).size().groupby(level=1).max()

     startresponse = startframe['riskresponse'].value_counts()
     chartresponse = dataframe['riskresponse'].value_counts()
     chartprobability = dataframe['riskprobability'].value_counts()
     charttrigger = dataframe['risktrigger'].value_counts()
     chartscore = dataframe['riskscore'].value_counts()
     totalrisks = len(startframe)
     startmetric4 = int(startresponse['Avoid'])
     endmetric4 = int(chartresponse['Avoid'])
     startmetric5 = sum(dataframe['riskselect'] == 'N')
     startmetric3 = sum(startframe['riskprobability'] == '1')
     endmetric3 = sum(dataframe['riskprobability'] == '1-High')

     #st.write(chartresponse)
     #st.write(chartprobability)
     #st.write(chartscore)
     #st.write(charttrigger)
 
     col3, col4, col5, col6 = st.columns(4)
     col3.metric("Issues", int(endmetric3/startmetric3), endmetric3)
     col4.metric("Avoid", startmetric4, int(endmetric4/startmetric4))
     col5.metric("Closed", startmetric5, int(startmetric5/totalrisks))
     with col6:
      st.write("Phase:", phasenumber, "CPI:", CPI, "SPI:", SPI, "Engagement:", engagementscoreteam, "Sentiment:", sentimentscoreteam, "Retention:", "Scope", scopechange  )
 

     # st.table(dataframe)
     charttype = dataframe['risktype'].value_counts()
     chartscore = dataframe['riskscore'].value_counts()
     chartowner = dataframe['riskowner'].value_counts()

     #st.subheader("Risk by Type")
     #st.bar_chart(groupscore)

     st.subheader("Risk by Type and Impact")
     c = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='risktype',
       y='count(riskimpact)',
       color='riskimpact'
     )
     st.altair_chart(c, use_container_width=True)

     st.subheader("Risk by Owner and Score")
     st.write("The project manager owns and monitors most risks, but some are owned by other in the team such as the product owner, team or sponsor to monitor and inform the project manager when the risk becomes an issue.  ")
     d = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskowner',
       y='count(riskscore)',
       color='riskscore'
     )
     st.altair_chart(d, use_container_width=True)

     st.subheader("Risk by Owner and Timeline")
     st.write("Risks can be closed when the project advances to later phases.")
     d = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskowner',
       y='count(risktimeline)',
       color='risktimeline'
     )
     st.altair_chart(d, use_container_width=True)

     st.subheader("Risk by Owner and Trigger")
     st.write("Using triggers identify if risks have occurred or will occur.")
     f = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskowner',
       y='count(risktrigger)',
       color='risktrigger'
     )
     st.altair_chart(f, use_container_width=True)

     st.subheader("Risk by Response and Score")
     st.write("Avoid risks by putting some measures in place to reduce or eliminate the risk, such as POC, or regular change control meetings. ")
     e = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskresponse',
       y='count(riskscore)',
       color='riskprobability'
     )
     st.altair_chart(e, use_container_width=True)

     st.subheader("Heatmap Impact and Probability")
     heatmap = alt.Chart(dataframe.dropna()).mark_rect().encode(
       alt.X('riskimpact', title="Impact", scale=alt.Scale(reverse=True)),
       alt.Y('riskprobability', title="Probability"),
       alt.Color('count()', scale=alt.Scale(scheme='lightgreyred'))
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
     st.write("Risks after adjustments based on current project status.  Risk probability is increased when trigger is applied.  Risks are closed when timeline is applied."   )
 
     grid_response = AgGrid(
        dataframe,
        editable=False,
        height=300,
        filter=True,
        )

     st.write("Risks at start of project.")
     grid_response = AgGrid(
        startframe,
        editable=False,
        height=300,
        filter=True,
        )
     #updated = grid_response['data']
     #df = pd.DataFrame(updated)

