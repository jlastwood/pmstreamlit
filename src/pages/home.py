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

The PM Monitor helps Project Managers monitor risks in projects. The PM Monitor presents the most common risks and uses sentiment analyis to discover when you should consider the response strategy.

This application provides

- A project canvas input and report 
- Earned value analysis and reporting
- A set of typical project risks based on your project canvas
- Sentiment analysis of your team and stakeholder communications

    """
        )
