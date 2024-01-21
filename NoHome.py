"""Main module for the streamlit app"""
import streamlit as st
from PIL import Image

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
    page_title="The PM Monitor",
    page_icon=im,
    layout="wide",
)    
st.session_state.update(st.session_state)
ip = Image.open("assets/images/HomeImage.jpg")

st.markdown("""
    <style>
        @media print {
            /* Hide the Streamlit menu and other elements you don't want to print */
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            [data-testid="stDecoration"] { display: none !important; }
            [data-testid="stToolbar"] { display: none !important; }
            .css-1iyw2u1 { display: none; }
            .css-15yd9pf { display: none; }
            .css-fblp2m { display: none; }
            .main {
                max-width: 12in !important;
                margin: 25mm 25mm 25mm 25mm;
            }

            span, p, div, textarea, input {
                color: #textcolor !important;
            }

            .stMarkdown, .stCodeBlock, [data-testid="caption"], [data-testid="stMarkdownContainer"], [data-testid="stImage"], [data-baseweb="textarea"] {
                max-width: 12in !important;
                word-break: break-all;
            }
            #MainMenu{visibility: hidden;} footer{visibility: hidden;}
            #root>div:nth-child(1)>div>div>div>div>section>div{padding-top: .2rem;
        }
    </style>
""", unsafe_allow_html=True)


st.header("6 Steps to Project Planning and Controlling")
st.markdown("---")
st.write("A project management tool provides assistance with managing chaos in a project, enabling the project manager to consume and analyse information from multiple sources, assess risks and plan actions. The PM Monitor walks the Project manager through creating a comprehensive Project plan with 6 phases, plan, design, build, inspect, accept and close. The PM generates reports and uses built in tools to analyse risks, task progress and communications.")
st.write("Create a comprehensive project plan with AI (askme) assistance, use built in analysis for sentiment and engagement analysis of communication channels , use target activity plan analysis report for analysis of tasks and activities and finally using a comprehensive list of possible risks classified by phase and probability enables fact based issue identification.")
st.markdown("---")
video_file = open('streamlit-Home-2023-11-19-09-11-67.webm', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)


st.markdown("---")
colr = st.columns(2)
with colr[0]:
    st.write(
        """
        Initiation and Planning \n 
         - Identify goals
         - Create a plan
         - Define resources and activities
         - Define milestones 
         - Review the goals and charter
         - Share canvas and schedule team kickoff 
         - Review risks, challenges and opportunities 
         - Create task list with team
        """)
with colr[1]:
    st.image(ip, caption="Step 1 - The PM Monitor Initiation, Planning, Set Goals and Objectives")
st.markdown("---")
coll = st.columns(2)
with coll[1]:
    st.write(
        """
        Execute, Monitor and Control \n
         - Update metrics,  milestones completed and costs incurred, change phase
         - Monitor activity changes and updates
         - Monitor communication channels, meetings and meeting outcomes
         - Monitor risks and issues and initiate controls
         - Create a report summary
         - Share stoplight report on your communication channel. 
        """)
with coll[0]:
    st.image(ip, caption='Step 2 - The PM Monitor Execution Monitoring, Controlling and Reporting')
st.markdown("---")
colr = st.columns(2)
with colr[0]:
    st.write(
        """
        Closure \n
         - Gather feedback
         - Create a report summary
         - Update plan and charter and publish
         - Generate final stoplight report
         - Thank the team and release
        """)
with colr[1]:
    st.image(ip, caption='Step 3 - The PM Monitor Closing')
st.markdown("---")
