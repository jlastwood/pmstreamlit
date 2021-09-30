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
    selectedrisks = [d for d in risks if d['riskselect'] > '0']

    for d in selectedrisks:
        if d['risktimeline'] == 'Any':
           d['riskselect'] = 'Y'
        else:
           d['riskselect'] = 'N'
           d['riskprobability'] = '0'
           d['riskimpact'] = '0'
           d['riskscore'] = '0'
           
    #  set the score value and count scores and risktable
    for d in selectedrisks:
        if d['riskimpact'] == '3' and d['riskprobability'] == '3':
           d['riskscore'] = '5'
        if d['riskimpact'] == '1' and d['riskprobability'] == '3':
           d['riskscore'] = '3'
        if d['riskimpact'] == '3' and d['riskprobability'] == '1':
           d['riskscore'] = '3'
        if d['riskimpact'] == '1' and d['riskprobability'] == '1':
           d['riskscore'] = '1'
        if d['riskimpact'] == '3' and d['riskprobability'] == '2':
           d['riskscore'] = '4'
        if d['riskimpact'] == '1' and d['riskprobability'] == '2':
           d['riskscore'] = '2'
        if d['riskimpact'] == '2' and d['riskprobability'] == '1':
           d['riskscore'] = '2'
        if d['riskimpact'] == '2' and d['riskprobability'] == '3':
           d['riskscore'] = '4'
        if d['riskimpact'] == '2' and d['riskprobability'] == '2':
           d['riskscore'] = '3'
        if d['riskimpact'] == '' and d['riskprobability'] == '':
           d['riskscore'] = '3'
        return(selectedrisks) 

@st.cache
def get_plan_markdown() -> str:
    """Enter the plan and return CPI and SPI
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
     st.error('Please create a plan')
     return()
    st.write("Project Number: ", st.session_state.plnumber)
    with st.form("my_risks"):
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
     with my_expander0:
      col1, col2 = st.columns(2)
      with col1:
       st.header("Risk by Risk Type")
       st.bar_chart(charttype)
      with col2:
       st.header("Risk by Risk Score")
       st.bar_chart(chartscore)
     st.header("Risk by group Score")
     st.bar_chart(groupscore)
     st.header("Risk by Owner")
     st.bar_chart(chartowner)
     st.header("Risk by response")
     st.bar_chart(chartresponse)
     st.header("Risk by Alt")
     c = alt.Chart(dataframe).mark_bar().encode(
       x='risktype',
       y='count(riskscore)',
       color='riskimpact'
     )
     st.altair_chart(c)
     #c = alt.Chart(dataframe).mark_bar().encode(
     #  x='risktype', y='riskprobability')
#     c = alt.Chart(dataframe).mark_circle().encode(
#       x='risktype', y='riskowner', size='riskimpact', color='riskimpact', tooltip=['risktype', 'riskowner', 'riskimpact'])

     #st.altair_chart(c, use_container_width=True)
     st.header("Risk Details")
     st.write(dataframe)
     st.json(myrisks)

     submit = st.form_submit_button("Submit")
     if submit:
        st.success("success")
