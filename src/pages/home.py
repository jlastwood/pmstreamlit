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

The PM Monitor helps Project Managers monitor risks in projects. The PM Monitor presents the most common risks and uses earned value and sentiment analysis to discover when you should consider the response strategy.  Project managers should monitor project risks often in order to address negative impacts to project scope, time, cost or quality early.  

This application provides

- Form to input your plans
- A project canvas report 
- Earned value analysis and reporting for CPI and SPI
- Selection of project risks based on your project characteristics
- Sentiment analysis of your team and stakeholder communications
- Probability setting of identified risks based on monitors 

    """
        )
