"""Page for viewing the awesome Project risks"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
from risklist import getrisks
import pandas as pd
import altair as alt

def calculate_risks_json(risks):
    # set value for score in dictionary for selected risks

    # using timeline decide which risks are closed and probability
    timeline = 20
    phase = 'Planning'
    phasenumber = '2'
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

    for d in risks:
        d['riskselect'] = 'N'
        # timeframe when risk will have an impact
        # the risk probablility can be 0 when risk has elapsed
        if d['risktimeline'] > '4':
           d['riskselect'] = 'Y'
        if d['risktimeline'] < '5' and timeline < 90:
           d['riskselect'] = 'Y'
        if d['risktimeline'] < '3' and timeline < 50:
           d['riskselect'] = 'Y'
        #   d['riskprobability'] = '0'
        #   d['riskimpact'] = '0'
        #   d['riskscore'] = '0'

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
        if d['riskimpact'] == '' and d['riskprobability'] == '':
           d['riskimpact'] = '2'
           d['riskprobability'] = '2'
           d['riskscore'] = 'Moderate'
        return(selectedrisks) 

@st.cache
def get_plan_markdown() -> str:
    """ enter plan
    """
    url = pathlib.Path(__file__).parent.parent.parent / "AWESOME-STREAMLIT.md"
    with open(url, mode="r") as file:
        readme_md_contents = "".join(file.readlines())
    return readme_md_contents.split("\n", 3)[-1]


def write():
    """Method used to write the page in the app.py file"""
    ast.shared.components.title_awesome("Risks")
    # with st.spinner("Loading  ..."):
    if 'plnumber' not in st.session_state:
     #st.session_state.plnumber = ""
     st.error('Please enter a plan')
     return()

    with st.form("my_risks"):
     st.write("Project Number: ", st.session_state.plnumber)

     col1, col2, col3, col4, col5 = st.columns(5)
     col1.metric("Highest", "70 °F", "1.2 °F")
     col2.metric("High", "9 mph", "-8%")
     col3.metric("Moderate", "86%", "4%")
     col4.metric("Low", "86%", "4%")
     col5.metric("Very Low", "86%", "4%")

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Project Information</h4>", unsafe_allow_html=True)
     startrisks = getrisks()
     myrisks = calculate_risks_json(startrisks)
     dataframe = pd.DataFrame.from_dict(myrisks, orient="columns")
     groupscore = dataframe.groupby(['riskscore', 'risktype']).size().groupby(level=1).max()
     my_expander0 = st.expander("text") 
     with my_expander0:
      col6, col7, col8 = st.columns(3)
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
     st.write(dataframe)
     st.json(myrisks)

     submit = st.form_submit_button("Update Risks")
     if submit:
        st.success("success")