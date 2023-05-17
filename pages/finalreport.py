"""Home page shown when the user enters the application"""
import streamlit as st
import awesome_streamlit as ast
from utilities import reporttitle
from PIL import Image

st.session_state.update(st.session_state)

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Final Report",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

if 'thepmheader' not in st.session_state:
 st.warning("Sorry, plan is missing.  Please enter or import a plan")
 st.stop()

# pylint: disable=line-too-long
reporttitle("Final Report", st.session_state['thepmheader'])

with st.spinner("Loading Home ..."):
    st.write(
            """

The PM Monitor is an aid for Project Managers to monitor and control risks in projects and report to the sponsor and team.   The PM Monitor assess and presents risks, uses earned value and sentiment analysis to adjust risk probability and predict issues and recommend a response strategy.  

The project manager is a communication facilator, they communicate expectations, monitor outcomes, listen and assess risks in order to address negative impacts to project scope, time, cost or quality early.   

The ability to assess, detect and predict issues is based on information obtained through engagement, sentiment, and subjectivity of written or spoken information.  This is combined with factual reports such as task completion status reports, time and cost reports. Using these inputs a  model can be developed to recommend changes to the project. 

Risk monitoring and control is an ongoing process for the life of the project.  Risks change as the project matures, new risks develop and anticipated risks disappear.  Risk monitoring provides processes to make effective decisions in advance of the risk occuring. 

    """
        )

    st.subheader("Project Objectives")

    st.subheader("Project Achievements")

    st.subheader("Scope Changes")

    st.subheader("Top 3 Risks/Issues")

    st.subheader("ROI and Cost Summary")
 
