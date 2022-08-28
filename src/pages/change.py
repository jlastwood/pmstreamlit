"""Page for viewing the awesome Project canvas"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import pandas as pd
from utilities import currencyrisk, evreport, plancomment, get_table_download_link
from st_radial import st_radial

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
    ast.shared.components.title_awesome("Change")
    # with st.spinner("Loading  ..."):

    # initialize session state variables
    if 'plnumber' not in st.session_state:
     st.session_state.plnumber = ""

    with st.form("my_plan"):

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     my_expander0 = st.expander("Managing change is important because in this fast-paced world things can change quickly. This means project managers need to be able to identify, assess impact, and make decisions. Project managers collaborate with stakeholders and the team to assess and provide solutions.  The outcome of the change is recorded in the plan as new goals, scope, budgets, resources or timelines.", expanded=True)
     with my_expander0:
      col6, col7 = st.columns([1, 3])
      with col6:
       plnumber  = st.text_input ("Project ID", value=st.session_state.plnumber, max_chars=10, help="A unique id to identify this project", key="plnumber")

     submit = st.form_submit_button("Save")
     if submit:
        st.info("The information was updated, thank you for using the PM Monitor")
   #  section to download the form for later use
