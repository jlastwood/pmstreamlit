import streamlit as st
from PIL import Image
from datetime import datetime 
from datetime import date
import pandas as pd
from scripts.thepmutilities import reporttitle, gradiant_header
from streamlit_extras.switch_page_button import switch_page
import os
from os import walk
from pathlib import Path

st.session_state.update(st.session_state)
pm = Image.open("assets/images/MonitorImage.png")

#  we have to do this as a separate file to force the refresh page
#  this saves as json file
#  https://github.com/Valires/streamlit-survey/blob/main/streamlit_survey/streamlit_survey.py

# todo add windows nt path
def getfiles(folder_path):
 selected_filename = "None"
 files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
 if files:
  selected_filename = st.selectbox('Select a project from local', files)
 return os.path.join(folder_path, selected_filename)

# 3. Apply Settings
def upload_saved_settings(saved_settings):
        #st.write(saved_settings)
        #st.write(len(saved_settings))
        """Set session state values to what specified in the saved_settings."""
        saved_settings.fillna('None', inplace = True)
        for i in range(len(saved_settings)):
            #st.write(saved_settings.iloc[i, 2])
            #if isinstance(saved_settings.iloc[i, 2],type(str)):
            #  st.write(saved_settings.iloc[i,1], saved_settings.iloc[i,2])
            if saved_settings.iloc[i, 2] == 'None':
              st.session_state[saved_settings.iloc[i, 1]] = 'None'
            if saved_settings.iloc[i, 2] == ' ':
              st.session_state[saved_settings.iloc[i, 1]] = 'None'
            if saved_settings.iloc[i, 1].startswith('plp'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
            if saved_settings.iloc[i, 1].startswith('pls'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
            if saved_settings.iloc[i, 1].startswith('pln'):
              st.session_state[saved_settings.iloc[i, 1]] = int(saved_settings.iloc[i, 2])
            if saved_settings.iloc[i, 1].startswith('pll'):
              st.session_state[saved_settings.iloc[i, 1]] = int(saved_settings.iloc[i, 2])
            #if saved_settings.iloc[i, 1].startswith('plm'):
            #  st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
              #  st.session_state[saved_settings.iloc[i, 1]] = 1
            #if saved_settings.iloc[i, 1].startswith('plmlist'):
            #  st.session_state[saved_settings.iloc[i, 1]] = list(saved_settings.iloc[i, 2])
            if 'status' in saved_settings.iloc[i, 1]:
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
            if saved_settings.iloc[i, 1].startswith('plmlist'):
              string_without_brackets = saved_settings.iloc[i, 2].strip("[]")
              string_without_brackets = string_without_brackets.replace("'", "")
              string_list = string_without_brackets.split(", ")
              for x in string_list:
               st.write(x)
               if x != "":
                 if x not in st.session_state[saved_settings.iloc[i, 1]]:  # prevent duplicates
                    st.session_state[saved_settings.iloc[i, 1]].append(x)
            if saved_settings.iloc[i, 1].startswith('pld') and len(saved_settings.iloc[i, 2]) > 6:
              datetime1 = saved_settings.iloc[i, 2]
              if len(datetime1) > 9:
               datetime2 = datetime.strptime(datetime1, '%Y-%m-%d').date()
              else:
               datetime2 = datetime.strptime(datetime1, '%m/%d/%y').date()
              st.session_state[saved_settings.iloc[i, 1]] = datetime2
        return


def clear_form():
  for key in st.session_state.keys():
    del st.session_state[key]
#@st.cache

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Save or Load Plan",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

gradiant_header ('The PM Monitor Projects')

#   st.info("The information was updated, thank you for using the PM Monitor.  Use Save Plan to save a copy of your plan offline.  Go to Canvas or Stoplight reports")

# 2. Select Settings to be uploaded
uploaded_file = st.file_uploader(label="Select a Plan to be uploaded",
                                     help="Select the Plan File (Downloaded in a previous run) that you want"
                                          " to be uploaded and then applied (by clicking 'Apply Plan' above)")
if uploaded_file is not None:
        uploaded_settings = pd.read_csv(uploaded_file)
        upload_saved_settings(uploaded_settings)
        st.warning("**WARNING**: Plan uploaded")
#        switch_page("Plan")
#else:

st.markdown("""---""")
st.write("Click clear to reset all plan information to None")
clear = st.button("Clear Plan")
if clear:
   st.info("The information was cleared, thank you for using the PM Monitor.  Go to Plan to initiate a new project plan.")
   clear_form()

# 1. Download Settings Button convert dataframe to list there is a pandas problem with data serialization set to legacy
dataitems = st.session_state.items()
datalist = list(dataitems)
df = pd.DataFrame(datalist)
df = df.astype(str)
csv = df.to_csv().encode('utf-8')
settings_to_download = {k: v for k, v in datalist if "button" not in k and "file_uploader" not in k}
uploaded_settings = settings_to_download
st.markdown("""---""")
st.write("Using the Save Plan button read the form data and save a copy offline")
pmid="CS1"
today = date.today()
reportdate = today.strftime("%b-%d-%Y")
pmfile_name = "thepmmonitorplan_" + pmid + "_" + reportdate + ".csv"
button_download = st.download_button(label="Save Plan",
                                           data=csv,
                                           file_name=pmfile_name,
                                           help="Click to Download Current Settings")

st.markdown("""---""")
dir = str(os.path.join(Path.home(), "Downloads"))
files = getfiles(dir)
st.write(files)

st.markdown("""---""")
st.write("Template or Sample projects")

wprelaunch = st.button("Wordpress Relaunch Plan")
if wprelaunch:
   uploaded_settings = pd.read_csv('files/wprelaunch.csv', sep=',')
   upload_saved_settings(uploaded_settings)
   st.warning("**WARNING**: Plan uploaded")
   st.info("The information was cleared, thank you for using the PM Monitor.  Go to Plan to initiate a new project plan.")

st.markdown("""---""")
st.write("The following is a copy of the plan details sheet saved as ")
st.dataframe(df, use_container_width=True)

# with open("milestones.csv", "rb") as file:
#         milestonebtn = st.download_button(
#         label="Download Milestone as CSV",
#         data=file,
#         file_name='miletstones.csv',
#         mime='text/csv',
#      )
