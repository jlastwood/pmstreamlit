"""Home page shown when the user enters the application"""
import streamlit as st

import awesome_streamlit as ast


# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""

    with st.spinner("Loading Home ..."):
        ast.shared.components.title_awesome("")
        st.write(
            """

The PM Monitor is an aid for Project Managers to monitor and control risks in projects. The PM Monitor presents the most common risks, uses earned value and sentiment analysis to predict issues and recommend a response strategy.  The project manager is a communication facilator, they communicate expectations,  and monitor outcomes, communications and risks in order to address negative impacts to project scope, time, cost or quality early.   The ability to assess, detect and predict issues is based on engagement, sentiment, and subjectivity of written or spoken information.  Combined with factual reports such as task completion status reports, time and cost reports, a model can be developed to recommend changes to the project teams. 

Risk monitoring and control is an ongoing process for the life of the project.  Risks change as the project matures, new risks develop and anticipated risks disappear.  Risk monitoring provides processes to make effective decisions in advance of the risk occuring. 

This application provides

- Form to input a charter and plan
- A project report or canvas including scope and benefits
- Earned value analysis and reporting of CPI and SPI
- Selection of project risks based on the project characteristics
- Sentiment analysis of team and stakeholder communications
- Probability of identified risks based on monitored threasholds
- Engagement analysis based on team and stakeholder communications 
- Wordcloud analysis reporting, what are the team talking about

Pipeline

- enter and save a copy of your charter
- submit cadence project updates to spend and progress
- connect your communications channels
- view risks, controls and monitors
- analysis, report and communicate
    """
        )
