import streamlit as st
from PIL import Image
from scripts.thepmutilities import gradiant_header
import os
from streamlit_extras.buy_me_a_coffee import button

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

st.session_state.update(st.session_state)

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

gradiant_header ('The PM Monitor Project Management Information')

st.write("In this section you can find starting points and information about how to use the product, contribute, or report an error") 
st.markdown("### Project Management Goal")

st.write("The goal and objective of a project manager is to communicate, mitigate risks, control the budget, manage stakeholder expectations, and ensure there is alignment between the business goals and the project goals.  The Project Manager and The PM monitor application collaborate planning, monitoring and control of projects. ")

st.write("Basic tasks")

colt = st.columns(3)
colt[0].write('<a href="#chapterh1">Print a Charter</a>', unsafe_allow_html = True)
colt[0].write('<a href="#chapter2">Scope</a>', unsafe_allow_html = True)
colt[0].write('<a href="#chapter3">Definitions and Terms</a>', unsafe_allow_html = True)

st.markdown("### Project Management Areas")

st.write("The PM monitor focuses on the follwing areas of project management, risk planning and monitoring, communication planning and monitoring, schedule planning and monitoring.")

st.subheader("Print a Charter", anchor="chapterh1")
video_file_name = "assets/images/printcharter.webm"
colsd = st.columns(2)
video_file = open(video_file_name, "rb")
video_bytes = video_file.read()
colsd[0].write("** Print Charter ** uses the link Charter, view the report then choose browser print.  If the text is cutoff, then adjust the width of the browser to 1024.")
colsd[1].video(video_bytes)
#st.video("localhost:8501/assets/videohelp/printcharter.webm", format="video/webm")
st.markdown("### About the App and Developer")

st.markdown("#### Git")
st.write("This project is public and shared, if you have issues, please report on git.  https://github.com/jlastwood/pmstreamlit ") 

st.markdown("#### Services")
st.write("The developer provides consulting and business process management services. Visit https://bluezoneit.com for a list of services and contact information ") 

st.markdown("#### Buy me a coffee")
st.write("Are you interested in supporting this project with additional features or ideas, please buy me a coffee. Your investment will go to improvements for the community.  https://buymeacoffee.com/thepmmonitor  ") 
button(username="thepmmonitor", floating=False)

st.markdown("#### Credits")
st.write(" a lot, get from source, streamlit, the python community")

st.markdown("#### Cheche-pm")
st.write(" Thank you to the developer of the python module to calculate critical path,  https://medium.com/@luisfernandopa1212/efficient-project-scheduling-with-python-the-critical-path-method-19a3f8235f91")

st.markdown("##### PMBOK Design")
st.write("This project was born from project management templates and forms using sheets https://docs.google.com/spreadsheets/d/1ubIRBmCT3wflP2_MozgJV-Tny7aZfcWBuo1kLx1vVgI/edit?usp=sharing  and the PMBOK list of forms  https://www.wiley.com/en-ca/A+Project+Manager's+Book+of+Forms:+A+Companion+to+the+PMBOK+Guide,+3rd+Edition-p-9781119393986")

st.subheader("Project Life Cycle and Product Life Cycle")
st.write("The project is organized into 4 phases Initiation,   Planning,  Execution/Control and Closing.  The product is organized into 6 phases,  Plan, Design, Build, Inspect, Accept and Closure.") 

st.subheader("Cost Management and Cost Control - Earned Value")
st.write("Monitoring risks are performed using earned value over time and spend and use the cost performance index and schedule performance index to raise issues")
st.write("https://www.projectengineer.net/the-earned-value-formulas/")

st.subheader("Engagement and Sentiment - Words")
st.write("A critical component of project management is establishing trust and communication with the team and stakeholders, listening to their feedback and taking an action when engagement or sentiment is low.   Sentiment analysis and engagement scores are used to monitor team and stakeholder sentiment and engagement.  ")
st.write("https://www.flashhub.io/virtuelle-organisationen-live/")

st.subheader("Risk Management - Risks")
st.write("The PM Monitor contains a risk register with 130 possible risks spanning 9 different categories.  Risks are flagged as possible issues using triggers, such as late start of tasks, scope changes, or low engagement scores.  The risks are reported in the management actions of the stoplight report")

st.subheader("Schedule Management - Tasks")
st.write("The PM Monitor contains a set of reports that provide analysis of the tasks or WBS.  The PM monitor monitors tasks started late, these are important to address early, and monitors tasks on the critical path that are finished late.  Most task assignment tools do not present the critical path or the late start information.  ") 

st.subheader("Theme")
st.write("Using streamlit theme under settings, you can change the colors of the view and reports")

st.subheader("Print")
st.write("Print to PDF using browser or streamlit print.  Collapse the left navigation bar and set browser width to page width before printing.  Please open an issue on git if there are issues with PDF printing formats. ")

st.subheader("Askme")
st.write("To use AI to complete narriation, ensure the response field is empty and check the checkbox beside the question.  A proposed response will be output to the screen.  Copy the result into the field, edit and save.  Project name must have a value to use the feature.  This feature is a result of the great work at hugging face.  Huggingface is open source tools and models to solve AI problems.  https://towardsdatascience.com/whats-hugging-face-122f4e7eb11a ")

#st.write("On git you can find samples of plans and reports")
#filelist = file_list_in_directory()
#st.write(filelist)

st.write("##")
successmsg = f'Thank you for using The PM Monitor. https://thepmmonitor.streamlit.app '
st.success(successmsg)
