"""Page for viewing the awesome Project risks"""
import streamlit as st
import pandas as pd
import pandas as pd
import altair as alt
from PIL import Image
#from scripts.risklist import getrisks
from scripts.thepmutilities import reporttitle, gradiant_header
from scripts.riskgenerate import calculate_risks_json
from scripts.cssscripts import page_media_print

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

page_media_print()

# with st.spinner("Loading  ..."):
gradiant_header ('The PM Monitor Risk Analysis')
if 'thepmheader' not in st.session_state:
     st.error('Please enter a plan')
     st.stop()

reporttitle("Risk Analysis", st.session_state['thepmheader'])

# get values for profile
# phasenumber = st.session_state.thepmphase
# CPI = st.session_state.thepmcpi
# SPI = st.session_state.thepmspi
# engagementscoreteam = st.session_state.plnactivesam
# sentimentscoreteam = st.session_state.plnactiveses
# open roles or weeks with full team less than 3
# retention = st.session_state.plnopenroles
# scopechange = len(st.session_state.plscopechange.split("."))
# if len(st.session_state.plscopechange) < 6:
#    scopechange = 0
# earnedvalue = st.session_state.plnactiveses
# roi = st.session_state.thepmannualroi
# latestart = st.session_state.plnactiveses
# inspectfail = st.session_state.plntestsfailed

with st.container():

#     startrisks = getrisks()
#     startframe = pd.DataFrame.from_dict(startrisks, orient="columns")
     (myrisks, issues, risks, totalrisks, risksummary)  = calculate_risks_json()
     # setting impact based on project settings
     #dataframe = pd.DataFrame.from_dict(myrisks, orient="columns")
     dataframe = pd.DataFrame(myrisks)
     impactlist = ['High','Very Low', 'Low', 'Moderate', 'High', 'Very High'] 
     impactno = ['1','3', '3', '2', '1', '1'] 
     srange=f"{impactno[st.session_state.plnteamrange]}-{impactlist[st.session_state.plnteamrange]}"
     dataframe.loc[dataframe['riskclassification'] == "Team", 'riskimpact'] = srange
     dataframe.loc[dataframe['riskclassification'] == "Communication", 'riskimpact'] = srange
     dataframe.loc[dataframe['riskclassification'] == "Stakeholders", 'riskimpact'] = srange
     srange=f"{st.session_state.plnscoperange}-{impactlist[st.session_state.plnscoperange]}"
     dataframe.loc[dataframe['riskclassification'] == "Change", 'riskimpact'] = srange
     dataframe.loc[dataframe['riskclassification'] == "Requirements", 'riskimpact'] = srange

     # #if there are mitigation strategies, set to mitigatei and if not set to Accept
     if len(st.session_state.plpscopecontingency) > 50:
       dataframe.loc[dataframe['riskclassification'] == "Requirements", 'riskresponse'] = "Mitigate"
       dataframe.loc[dataframe['riskclassification'] == "Scope", 'riskresponse'] = "Mitigate"
       dataframe.loc[dataframe['riskclassification'] == "Change", 'riskresponse'] = "Mitigate"
     else:
       dataframe.loc[dataframe['riskclassification'] == "Requirements", 'riskresponse'] = "Accept"
       dataframe.loc[dataframe['riskclassification'] == "Scope", 'riskresponse'] = "Accept"
       dataframe.loc[dataframe['riskclassification'] == "Change", 'riskresponse'] = "Accept"

     for line in st.session_state.plpriskreporttransfer.split(","):
        dataframe.loc[dataframe['riskclassification'] == line, 'riskresponse'] = "Transfer"
        # dataframe.loc[dataframe['riskclassification'] == line, 'riskowner'] = "Third Party"
     for line in st.session_state.plpriskreportaccept.split(","):
        dataframe.loc[dataframe['riskclassification'] == line, 'riskresponse'] = "Accept"

     # st.write(dataframe)

     # recalculate the score impact and probablity
     groupscore = dataframe.groupby(['riskimpact', 'risktype']).size().groupby(level=1).max()

     #st.header("Risk Detail")
     #editeddf = st.data_editor(
     #   dataframe,
     #   column_config={
     #   "riskselect": st.column_config.SelectboxColumn(
     #       "Select",
     #       help="Issues to raise for management action",
     #       width="small",
     #       options=[
     #           "N",
     #           "Y",
     #           "I",
     #       ],
     #       required=True,
     #   ),
     #    "risktype": "Type",
     #    "riskowner": "Owner",
     #    "riskscore": "Score",
     #    "riskdescription": "Description"
     #    },
     #    disabled=("risktype", "riskowner", "riskscore", "riskdescription"),
     #    hide_index=True,
     #    use_container_width=True,
     #    height=200,
     #)

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
       x=alt.X('risktype', title="Type"),
       y='count(riskimpact)',
       color=alt.Color('riskimpact', title="Impact")
     )
     st.altair_chart(c, use_container_width=True)
     st.write("Impact and Probability determine the score, high, medium and low")

     st.subheader("Risk by Owner and Score")
     d = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x=alt.X('riskowner', title="Owner"),
       y='count(riskscore)',
       color=alt.Color('riskscore', title="Score")
     )
     st.altair_chart(d, use_container_width=True)
     st.write("The project manager owns and monitors most project risks, but some are owned by other in the team such as the product owner, team or sponsor to monitor and inform the project manager when the risk becomes an issue.  ")

     st.subheader("Risk by Class and Timeline")
     d = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x=alt.X('riskclassification', title="Classification"),
       y='count(risktimeline)',
       color=alt.Color('risktimeline', title="Timeline")
     )
     st.altair_chart(d, use_container_width=True)
     st.write("Risks are closed when the project advances to later phases as they no longer are applicable")

     st.subheader("Risk by Response and Trigger")
     f = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x=alt.X('riskresponse', title="Response"),
       y=alt.Y('count(risktrigger)'),
       color='risktrigger'
     )
     st.altair_chart(f, use_container_width=True)
     st.write("Triggers assist in the monitoring of risks.  Triggers monitor risks based on facts or information that is available about the progress or status of the project or product, such as the cost, CPI, or schedule, SPI.")

     st.subheader("Risk by Response and Score")
     e = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x=alt.X('riskresponse', title="Response"),
       y='count(riskscore)',
       color=alt.Color('riskprobability', title="Probability")
     )
     st.altair_chart(e, use_container_width=True)
     st.write("Avoid and mitigate risks by defining strategies to avoid or mitigate to reduce the risk, such as POC, or regular change control meetings.  Transfer risks using insurance,  transfer risk usually has a cost, such as making periodic payments. Using fixed price agreements is also a way to transfer risk.  ")

     st.subheader("Risk by Classification and Trigger")
     e = alt.Chart(dataframe.dropna()).mark_bar().encode(
       x=alt.X('riskclassification', title="Classification"),
       y='count(riskscore)',
       color=alt.Color('risktrigger', title="Trigger")
     )
     st.altair_chart(e, use_container_width=True)
     st.write("Triggers assist in the monitoring of risks.  Triggers monitor risks based on facts or information that is available about the progress or status of the project or product, such as the cost, CPI, or schedule, SPI.")

     #  alt.Y('riskimpact', title="Impact", scale=alt.Scale(reverse=True)),
     #  alt.Color('count(riskscore)', scale=alt.Scale(scheme='lightgreyred'))
     st.subheader("Heatmap Impact and Probability")
     heatmap = alt.Chart(dataframe.dropna()).mark_rect().encode(
       alt.Y('riskimpact', title="Impact"),
       alt.X('riskprobability', title="Probability"),
       alt.Color('riskscore', title="Score", scale=alt.Scale(scheme='set1'))
       #alt.Color('riskscore')
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
     st.write("The combinatin of impact and probabilty set a score.  The team should focus on mitigation of the highest risks and accept risks with low scores.  It is costly to try to monitor and mitigate all risks.")

     # st.header("Risk Details Report")
     # st.dataframe(dataframe, use_container_width=True)

     st.header("Risk Mitigation Plans")
     st.write("Scope Mitigation") 
     st.write(st.session_state.plpscopecontingency)

     st.write("Time Mitigation") 
     st.write(st.session_state.plptimecontingency)
 
     st.write("Budget Mitigation") 
     st.write(st.session_state.plpbudgetcontingency)

     st.write("Team Mitigation") 
     st.write(st.session_state.plpteamcontingency)

     st.write("Resource Mitigation") 
     st.write(st.session_state.plpresourcecontingency)

st.header("Risk Register")
owners = pd.unique(dataframe['riskowner'])

for owner in owners:
     st.write("Risks monitored by ", owner)
     cols = ['risktype', 'riskscore', 'riskdescription', 'risktimeline', 'riskselect']
     myissues = (dataframe[dataframe['riskowner'] == owner])
     subissues = myissues[cols].sort_values(by=['riskselect', 'riskscore'])
     # st.table(subissues.head(5))
     st.table(subissues)

st.write("##")
successmsg = f'The PM Monitor {st.session_state.plpname} charter presented by {st.session_state.plpmname} on {st.session_state.pldcharterdate}.  Thank you for using The PM Monitor https://thepmmonitor.streamlit.app '
st.success(successmsg)
