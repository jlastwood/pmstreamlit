"""Page for viewing the awesome Project risks"""
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
#from scripts.risklist import getrisks
from scripts.thepmutilities import reporttitle, gradiant_header
from scripts.riskgenerate import calculate_risks_json

#  https://asana.com/resources/risk-register
#  incorporate this
#  https://www.stakeholdermap.com/risk/register-common-project-risks.html
#  https://www.carmichaelireland.ie/app/uploads/2022/03/Sample-Completed-Risk-Register.pdf
#  https://www.indeed.com/hire/c/info/project-risk-registers
#  https://risk-academy.ru/download/example-of-a-completed-risk-register/
#  https://www.dhs.gov/sites/default/files/publications/bw11_foia_cbp_007329_-_007334.pdf
#  https://www.thepensionsregulator.gov.uk › pd
#  https://www.warrington.gov.uk/sites/default/files/2019-10/risk_register.pdf
#  https://www.rocketlane.com/blogs/how-to-create-a-project-risk-register-free-template


    # set value for score in dictionary for selected risks
    # using timeline decide which risks are closed and probability

engagementscoresponsor = 70
sentimentscoresponsor = 70
retentionscoresponsor = 70
engagementproductteam = 0
sentimenttproductteam = 0
engagementscoreuser = 0
sentimenttscoreuser = 0

st.session_state.update(st.session_state)

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Risk Analysis",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)             
    # with st.spinner("Loading  ..."):
gradiant_header ('The PM Monitor Risk Analysis')
if 'thepmheader' not in st.session_state:
     st.error('Please enter a plan')
     st.stop()

reporttitle("Risk Analysis", st.session_state['thepmheader'])

# get values for profile
phasenumber = st.session_state.thepmphase
CPI = st.session_state.thepmcpi
SPI = st.session_state.thepmspi
engagementscoreteam = st.session_state.plnactivesam
sentimentscoreteam = st.session_state.plnactiveses
# open roles or weeks with full team less than 3
retention = st.session_state.plnopenroles
scopechange = len(st.session_state.plscopechange.split("."))
if len(st.session_state.plscopechange) < 6:
   scopechange = 0
earnedvalue = st.session_state.plnactiveses
roi = st.session_state.thepmannualroi
latestart = st.session_state.plnactiveses
inspectfail = st.session_state.thepminspectflag

with st.container():

#     startrisks = getrisks()
#     startframe = pd.DataFrame.from_dict(startrisks, orient="columns")
     (myrisks, issues, risks, totalrisks, risksummary)  = calculate_risks_json(phasenumber, SPI, CPI, engagementscoreteam, sentimentscoreteam, retention, scopechange, earnedvalue, roi, latestart, inspectfail)
     dataframe = pd.DataFrame.from_dict(myrisks, orient="columns")
     groupscore = dataframe.groupby(['riskimpact', 'risktype']).size().groupby(level=1).max()
     st.header("Risk Detail")
     editeddf = st.data_editor(
        dataframe,
        column_config={
        "riskselect": st.column_config.SelectboxColumn(
            "Select",
            help="Issues to raise for management action",
            width="small",
            options=[
                "N",
                "Y",
                "I",
            ],
            required=True,
        ),
         "risktype": "Type",
         "riskowner": "Owner",
         "riskscore": "Score",
         "riskdescription": "Description"
         },
         disabled=("risktype", "riskowner", "riskscore", "riskdescription"),
         hide_index=True,
         use_container_width=True,
         height=200,
     )

     startresponse = myrisks['riskresponse'].value_counts()
     chartresponse = dataframe['riskresponse'].value_counts()
     chartprobability = dataframe['riskprobability'].value_counts()
     charttrigger = dataframe['risktrigger'].value_counts()
     chartscore = dataframe['riskscore'].value_counts()
     closed = sum(dataframe['riskselect'] == 'N')
     startmetric4 = sum(myrisks['riskresponse'] == 'Avoid')
     endmetric4 = sum(dataframe['riskresponse'] == 'Avoid')
     startmetric5 = sum(dataframe['riskselect'] == 'N')
     startmetric3 = sum(myrisks['riskprobability'] == '1-High')
     endmetric3 = sum(dataframe['riskprobability'] == '1-High')

     #st.write(risksummary)

     col3, col4, col5 = st.columns(3)
     col3.metric("Issues", issues)
     col4.metric("Risks", risks)
     col5.metric("Closed", startmetric5, int(startmetric5/totalrisks))

     #st.dataframe(dataframe)
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
     d = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskowner',
       y='count(riskscore)',
       color='riskscore'
     )
     st.altair_chart(d, use_container_width=True)
     st.write("The project manager owns and monitors most risks, but some are owned by other in the team such as the product owner, team or sponsor to monitor and inform the project manager when the risk becomes an issue.  ")

     st.subheader("Risk by Class and Timeline")
     st.write("Risks are closed when the project advances to later phases as they no longer are applicable")
     d = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskclassification',
       y='count(risktimeline)',
       color='risktimeline'
     )
     st.altair_chart(d, use_container_width=True)

     st.subheader("Risk by Response and Trigger")
     st.write("Using triggers risks in the current phase will be flagged as issues ", phasenumber, SPI, CPI, engagementscoreteam, sentimentscoreteam, retention, scopechange, earnedvalue, roi, latestart, inspectfail)
     f = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x=alt.X('riskresponse', title="Response"),
       y=alt.Y('count(risktrigger)'),
       color='risktrigger'
     )
     st.altair_chart(f, use_container_width=True)

     st.subheader("Risk by Response and Score")
     st.write("Avoid risks by defining strategies to avoid or mitigate to reduce the risk, such as POC, or regular change control meetings. ")
     e = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskresponse',
       y='count(riskscore)',
       color='riskprobability'
     )
     st.altair_chart(e, use_container_width=True)

     st.subheader("Risk by Classification and Trigger")
     st.write("The triggers are the fact based information that results in a risk becoming an issue ")
     e = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x='riskclassification',
       y='count(riskscore)',
       color='risktrigger'
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

     #st.header("Risk Detail")
     #st.dataframe(dataframe, hide_index=True)
 

