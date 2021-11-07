"""Page for viewing the awesome Project canvas"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import pandas as pd

@st.cache
def get_canvas_markdown() -> str:
    """Enter the plan and return CPI and SPI
    """
    url = pathlib.Path(__file__).parent.parent.parent / "AWESOME-STREAMLIT.md"
    with open(url, mode="r") as file:
        readme_md_contents = "".join(file.readlines())
    return readme_md_contents.split("\n", 3)[-1]

def write():
     """Method used to write the page in the app.py file"""
     ast.shared.components.title_awesome("Canvas")
    # with st.spinner("Loading  ..."):

    # initialize session state variables
     if 'plnumber' not in st.session_state:
      st.session_state.plnumber = ""
      st.error('Please enter a plan')
      return()

     st.write("Project Number: ", st.session_state.plnumber)
#    with st.form("my_canvas"):
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     st.markdown("<h4 style='text-align: center; color: white; background: green;'>Goal Setting</h4>", unsafe_allow_html=True)
     col6, col7, col8 = st.columns([3, 1, 1])
     with col6:
      st.info("Scope :thought_balloon:")
     with col7:
      st.info("Users :thought_balloon:")
     with col8:
      st.info("Benefits :thought_balloon:")
     col4, col5 = st.columns(2)
     with col4:
      st.info("Stakeholders :thought_balloon:")
     with col5:
      st.success("Risks chart :grinning:")
     col4, col5 = st.columns(2)
     with col4:
      st.info("Team :thought_balloon:")
     with col5:
      st.success("Resources :grinning:")
     col4, col5 = st.columns(2)
     with col4:
      st.info("Budget :thought_balloon:")
     with col5:
      st.success("Actions :grinning:")
     st.write("Planning :grinning:")
     color1 = '#1aa3ff'
     color2 = '#00ff00'
     color3 = '#ffffff'
     content = 'sample'
     st.markdown(f'<p style="text-align:center;background-image: linear-gradient(to right,{color1}, {color2});color:{color3};font-size:14px;border-radius:5px;">{content}</p>', unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: blue'>Timeframe</h4>", unsafe_allow_html=True)
     st.write(":red_circle: :yellow_circle: :green_circle:", unsafe_allow_html=True)
     st.markdown("<h4 style='text-align: center; color: white; background: yellow'>Team</h4>", unsafe_allow_html=True)
     st.markdown("<h4 style='text-align: center; color: white; background: pink;'>Environment</h4>", unsafe_allow_html=True)
     #download = st.form_submit_button("Download Analysis")
     #df = pd.DataFrame({'numbers': [1, 2, 3], 'colors': ['red', 'white', 'blue']})
     # d = {'Budget': [plbudget], 'Hours': [plhours]} 
     # st.markdown(get_table_download_link(df), unsafe_allow_html=True)
     #if download:
     #   open('df.csv', 'w').write(df.to_csv())
     # st.success("The download is presented in another tab,  thank you for using the PM monitor")
     # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/



