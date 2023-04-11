"""Main module for the streamlit app"""
import streamlit as st
from PIL import Image

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

import awesome_streamlit as ast

def main():
    """Main function of the App"""
    st.session_state.update(st.session_state)
    st.header("6 Steps to Better Project Planning and Controlling")
    st.markdown("---")
    st.write("Fill in the project plan, and use Askme and OpenAI technology assistance to create the plan, use NLP for sentiment and engagement analysis of communication channels and reports, use target activity plan analysis report for analysis of tasks and activities and finally a comprehensive list of possible risks classified by phase speeds up issue identification.")
    st.markdown("---")
    colr = st.columns((1,3))
    with colr[0]:
     st.write(
"""
##Initiation and Planning##
	•	Identify goals
	•	Create a plan
	•	Define resources and activities
	•	Define milestones 
	•	Review the goals and plan in the canvas report with stakeholders and team kickoff
	•	Know the risks, challenges and opportunities and plan mitigation 
""")
    with colr[1]:
     st.image('assets/images/Homeimage.jpg', caption='Step 1 - The PM Monitor Initiation, Planning, Set Goals and Objectives')
    st.markdown("---")
    coll = st.columns((3,1))
    with coll[1]:
     st.write(
"""
Monitoring and Control
	•	   Update metrics,  milestones completed and costs incurred, change phase
	•	   Monitor activity changes and updates
	•	   Monitor communication channels, meetings and meeting outcomes
	•	   Monitor risks and issues and initiate controls
	•	   Create a report summary
	•	   Share stoplight report on your communication channel. 

""")
    with coll[0]:
     st.image('assets/images/Homeimage.jpg', caption='Step 2 - The PM Monitor Execution Monitoring, Controlling and Reporting')
    st.markdown("---")
    colr = st.columns((1,3))
    with colr[0]:
     st.write("Closure.  gather feedback in a survey,  update metrics,  generate final stoplight report, financials and close")
    with colr[1]:
     st.image('assets/images/Homeimage.jpg', caption='Step 3 - The PM Monitor Closing')
    st.markdown("---")
    columns = st.columns((2,1,2))
    url1 = "/plan"
    with columns[1]:
     st.markdown(f'''
<a href={url1} target = "_self"><button style="background-color:#F4A261;text-align: center;">  Start Planning  </button></a>
''',
unsafe_allow_html=True)

    st.sidebar.write("***About and Contribute***")
    st.sidebar.write(
        """
        This an open source project built using Streamlit, submit comments, questions, as 
        [issues](https://github.com/jlastwood/pmstreamlit/issues)
        Idea, Design and Development by Janet. More information at
        [bluezoneit.com](https://bluezoneit.com).
"""
    )

if __name__ == "__main__":
    main()
