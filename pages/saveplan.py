import streamlit as st
from PIL import Image
import pathlib
from math import log
from datetime import datetime 
from datetime import timedelta, date
import pandas as pd
from st_aggrid import AgGrid
import io
import base64

st.session_state.update(st.session_state)

# 3. Apply Settings
def upload_saved_settings(saved_settings):
        #st.write(saved_settings)
        #st.write(len(saved_settings))
        """Set session state values to what specified in the saved_settings."""
        for i in range(len(saved_settings)):
          #st.write(saved_settings.iloc[i, 2])
          #if isinstance(saved_settings.iloc[i, 2],type(str)):
            if saved_settings.iloc[i, 1].startswith('plp'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
            if saved_settings.iloc[i, 1].startswith('pls'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
            if saved_settings.iloc[i, 1].startswith('pln'):
              st.session_state[saved_settings.iloc[i, 1]] = int(saved_settings.iloc[i, 2])
            if saved_settings.iloc[i, 1].startswith('plrlist'):
              st.session_state[saved_settings.iloc[i, 1]] = int(saved_settings.iloc[i, 2])
            if saved_settings.iloc[i, 1].startswith('pllist'):
              st.session_state[saved_settings.iloc[i, 1]] = int(saved_settings.iloc[i, 2])
            #if saved_settings.iloc[i, 1].startswith('plmlist'):
            #  string_without_brackets = saved_settings.iloc[i, 2].strip("[]")
            #  string_without_brackets = string_without_brackets.replace("'", "")
            #  string_list = string_without_brackets.split(", ")
            #  for x in string_list:
            #   if x != "":
            #     if x not in st.session_state[saved_settings.iloc[i, 1]]:  # prevent duplicates
            #        st.session_state[saved_settings.iloc[i, 1]].append(x)
            if saved_settings.iloc[i, 1].startswith('pld') and len(saved_settings.iloc[i, 2]) > 6:
              datetime1 = saved_settings.iloc[i, 2]
              datetime2 = datetime.strptime(datetime1, '%Y-%m-%d').date()
              st.session_state[saved_settings.iloc[i, 1]] = datetime2
        return

def setvalue(var):

    if (st.session_state.clear == True and var.startswith('plm')):
       return "None"

    if var.startswith('pllist'):
        if var in st.session_state:
          if st.session_state[var] == "":
           return 0
          else:
           return int(st.session_state[var])
        else:
         return 0
    if var.startswith('pld'):
       return st.session_state[var] if var in st.session_state else date.today()
    else:
       if var.startswith('pln'):
          return int(st.session_state[var]) if var in st.session_state else 0
       else:
          return st.session_state[var] if var in st.session_state else "None"


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

st.markdown("<h3 style='text-align: center; color: white; background: grey;'>The PM Monitor</h3>", unsafe_allow_html=True)


     #   st.info("The information was updated, thank you for using the PM Monitor.  Use Save Plan to save a copy of your plan offline.  Go to Canvas or Stoplight reports")

clear = st.button("Clear Plan")
if clear:
   st.info("The information was cleared, thank you for using the PM Monitor.  Use Save Plan to save a copy of your plan offline")
   clear_form()

# 1. Download Settings Button convert dataframe to list
#  there is a pandas problem with data serialization set to legacy
dataitems = st.session_state.items()
datalist = list(dataitems)
df = pd.DataFrame(datalist)

csv = df.to_csv().encode('utf-8')
col1, col2, col3, col4 = st.columns([1, 1, 3, 3])
#settings_to_download = {k: v for k, v in st.session_state.items()
settings_to_download = {k: v for k, v in datalist if "button" not in k and "file_uploader" not in k}

    # 2. Select Settings to be uploaded
with col3:
  uploaded_file = st.file_uploader(label="Select a Plan to be uploaded",
                                     help="Select the Plan File (Downloaded in a previous run) that you want"
                                          " to be uploaded and then applied (by clicking 'Apply Plan' above)")
with col4:
  if uploaded_file is not None:
         uploaded_settings = pd.read_csv(uploaded_file)
  else:
        #uploaded_settings = settings_to_download
        uploaded_settings = settings_to_download
        st.warning("**WARNING**: Select the Plan File to be uploaded")

button_apply_settings = col2.button(label="Apply Plan",
                                        on_click=upload_saved_settings,
                                        args=(uploaded_settings,),
                                        help="Click to Apply the Plan of the Uploaded file.\\\n"
                                             "Please start by uploading a Plan File below")
pmid="CS1"
reportdate="12-01-2022"
pmfile_name = "pmmonitorsettings_" + pmid + "_" + reportdate + ".csv"
button_download = col1.download_button(label="Save Plan",
                                           data=csv,
                                           file_name=pmfile_name,
                                           help="Click to Download Current Settings")
st.dataframe(df, use_container_width=True)
# with open("milestones.csv", "rb") as file:
#         milestonebtn = st.download_button(
#         label="Download Milestone as CSV",
#         data=file,
#         file_name='miletstones.csv',
#         mime='text/csv',
#      )
