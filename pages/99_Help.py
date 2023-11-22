import streamlit as st
from PIL import Image
from scripts.thepmutilities import gradiant_header
import os

def file_list_in_directory():
  filelist=[]
  for root, dirs, files in os.walk("files"):
      for file in files:
             filename=os.path.join(root, file)
             filelist.append(filename)
  return(filelist)

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor About Page",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)
st.markdown("""
    <style>
        @media print {
            /* Hide the Streamlit menu and other elements you don't want to print */
            [data-testid="stSidebar"] {
                display: none !important;
            }

            .main {
                max-width: 8in !important;
            }

            span, p, div, textarea, input {
                color: #000 !important;
            }
            
            .stMarkdown, .stCodeBlock, [data-testid="caption"], [data-testid="stMarkdownContainer"], [data-testid="stImage"], [data-baseweb="textarea"] {
                max-width: 8in !important;
                word-break: break-all;
            }

        }
    </style>
""", unsafe_allow_html=True)

gradiant_header ('The PM Monitor Information About this Product')

st.markdown("### About")

st.subheader("Services")
st.write("Janet provides consulting and business process management services. Visit https://bluezoneit.com for a list of services and contact information ") 
st.markdown("#### Buy me a coffee")
st.write("If you would like to support this project with additional features or ideas, please buy me a coffee. Your investment will go to improvements for the community.  https://buymeacoffee.com/thepmmonitor  ") 

st.subheader("Git")
st.write("This project is public and shared, if you have issues, please report on git. ") 

st.subheader("Project management and reporting using Sheets")
st.write("This project was born from my current project management templates and forms using sheets")

st.subheader("Cost Formulas")
st.write("https://www.projectengineer.net/the-earned-value-formulas/")

st.subheader("Trust and Virtual Teams")
st.write("A critical component of project management is establishing trust and communication with the team and stakeholders.  We monitor this using sentiment analysis and engagement scores.  Following is a talk I gave at a customer site. ")
st.write("https://www.flashhub.io/virtuelle-organisationen-live/")

st.subheader("Credits")
st.write(" a lot, get from source, streamlit, the python community")

st.subheader("Theme")
st.write("Using streamlit theme under settings, you can change the colors of the view and reports")

st.subheader("Print")
st.write("Print to PDF using browser or streamlit print.  Collapse the left navigation bar and set browser width to page width before printing.  The media print css code may still need some work. ")

st.subheader("Askme")
st.write("To use AI to complete narriation, ensure the response field is empty and check the checkbox beside the question.  A proposed response will be output to the screen.  Copy the result into the field, edit and save.  Project name must have a value to use the feature.  This feature is a result of the great work at hugging face.  Huggingface is open source tools and models to solve AI problems.  https://towardsdatascience.com/whats-hugging-face-122f4e7eb11a ")

filelist = file_list_in_directory()
st.write(filelist)
