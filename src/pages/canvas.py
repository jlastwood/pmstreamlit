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

    with st.form("my_canvas"):
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     st.markdown("<h4 style='text-align: center; color: white; background: green;'>Goal Setting</h4>", unsafe_allow_html=True)
     col6, col7 = st.beta_columns([3, 1])
     with col6:
      st.info("this is info :thought_balloon:")
     with col7:
      st.info("this is info :thought_balloon:")
     col4, col5 = st.beta_columns(2)
     with col4:
      st.info("this is info :thought_baloon:")
     with col5:
       st.success("this is success :grinning:")
     color1 = '#1aa3ff'
     color2 = '#00ff00'
     color3 = '#ffffff'
     content = 'sample'
     st.markdown(f'<p style="text-align:center;background-image: linear-gradient(to right,{color1}, {color2});color:{color3};font-size:14px;border-radius:5px;">{content}</p>', unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: blue'>Timeframe</h4>", unsafe_allow_html=True)
     st.write(":red_circle: :yellow_circle: :green_circle:", unsafe_allow_html=True)
     st.markdown("<h4 style='text-align: center; color: white; background: yellow'>Team</h4>", unsafe_allow_html=True)
     st.markdown("<h4 style='text-align: center; color: white; background: pink;'>Environment</h4>", unsafe_allow_html=True)
     submit = st.form_submit_button("Save")
     if submit:
        st.info("The information was updated, thank you for using the PM Monitor")
     #download = st.form_submit_button("Download Analysis")
     #df = pd.DataFrame({'numbers': [1, 2, 3], 'colors': ['red', 'white', 'blue']})
     # d = {'Budget': [plbudget], 'Hours': [plhours]} 
     # st.markdown(get_table_download_link(df), unsafe_allow_html=True)
     #if download:
     #   open('df.csv', 'w').write(df.to_csv())
     # st.success("The download is presented in another tab,  thank you for using the PM monitor")
      # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/



