"""Main module for the streamlit app"""
import streamlit as st
from PIL import Image
#from st_pages import Page, Section, show_pages, add_page_title

primaryColor="#264653"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F4A261"
textColor="#2A9D8F"

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

#import awesome_streamlit as ast

#show_pages(
#    [
#        Page("home.py", "Home", "🏠"),
#        Page("pages/plan.py", "Plan", ":spiral_note_pad:"),
#        Page("pages/saveplan.py", "Save", ":left_speech_bubble:"),
#        Section(name="Reports", icon=":books:"),
#        Page("pages/stoplight.py", "StopLight", ":books:"),
#        Page("pages/canvas.py", "Canvas", ":books:"),
#        Page("pages/finalreport.py", "  Final", ":information_source:"),
#        Section(name="Analysis", icon=":books:"),
#        Page("pages/risk.py", "Risk", ":books:"),
#        Page("pages/wbs.py", "WBS", ":books:"),
#        Page("pages/communication.py", "  Comms", ":left_speech_bubble:"),
#        Page("pages/about.py", "About", ":books:", in_section=False),
#    ]
#)

def main():
    """Main function of the App"""
    ip = Image.open("assets/images/HomeImage.jpg")
    st.session_state.update(st.session_state)
    st.header("6 Steps to Better Project Planning and Controlling")
    st.markdown("---")
    st.write("Fill in the project plan with Askme assistance, use NLP for sentiment and engagement analysis of communication channels and reports, use target activity plan analysis report for analysis of tasks and activities and finally a comprehensive list of possible risks classified by phase and probability set by triggers will speed up issue identification.")
    st.markdown("---")
    colr = st.columns(2)
    with colr[0]:
     st.write(
"""
Initiation and Planning \n 
	• Identify goals
	• Create a plan
	• Define resources and activities
	• Define milestones 
	• Review the goals and plan in the canvas report with stakeholders and team kickoff
	• Know the risks, challenges and opportunities and plan mitigation 
""")
    with colr[1]:
     st.image(ip, caption="Step 1 - The PM Monitor Initiation, Planning, Set Goals and Objectives")
    st.markdown("---")
    coll = st.columns(2)
    with coll[1]:
     st.write(
"""
Execute, Monitor and Control \n
	• Update metrics,  milestones completed and costs incurred, change phase
	• Monitor activity changes and updates
	• Monitor communication channels, meetings and meeting outcomes
	• Monitor risks and issues and initiate controls
	• Create a report summary
	• Share stoplight report on your communication channel. 

""")
    with coll[0]:
     st.image(ip, caption='Step 2 - The PM Monitor Execution Monitoring, Controlling and Reporting')
    st.markdown("---")
    colr = st.columns(2)
    with colr[0]:
     st.write(
"""
Closure \n
	• Gather feedback
	• Update plan 
	• Generate final stoplight report
""")
    with colr[1]:
     st.image(ip, caption='Step 3 - The PM Monitor Closing')
    st.markdown("---")
    columns = st.columns((2,1,2))
    url1 = "/plan"
#    with columns[1]:
#     st.markdown(f'''
#<a href={url1} target = "_self"><button style="background-color:#F4A261;text-align: center;">  Start Planning  </button></a>
#''',
#unsafe_allow_html=True)

#    st.sidebar.write("***About and Contribute***")
#    st.sidebar.write(
#        """
#        This an open source project built using Streamlit, submit comments, questions, as 
#        [issues](https://github.com/jlastwood/pmstreamlit/issues)
#        Idea, Design and Development by Janet. More information at
#        [bluezoneit.com](https://bluezoneit.com).  Feel free to buy me a coffee to support The PM monitor.  [bmc.link](https://bmc.link/thepmmonitor)
#"""
#    )

if __name__ == "__main__":
    main()
