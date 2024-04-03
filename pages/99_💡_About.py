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

st.write("Project management is the process of leading the work of a team to achieve all project goals within the given constraints. This information is described in a plan developed at the start of the project. The primary constraints are scope, time, and budget.  The goal of the project manager is to communicate, plan and mitigate risks, control the budget, manage stakeholder expectations, and ensure there is alignment between the business goals and the project goals.  The Project Manager and The PM monitor application collaborate planning, monitoring and control of projects. The PM monitor focuses on the follwing areas of project management, risk planning and monitoring, communication planning and monitoring, schedule planning and monitoring.")

st.subheader("Basic tasks", anchor="toc")

colt = st.columns(3)
colt[0].write('<a href="#chapterh1">Charter</a>', unsafe_allow_html = True)
colt[0].write('<a href="#chapterh2">Scope and Askme</a>', unsafe_allow_html = True)
colt[0].write('<a href="#chapterbooks">Project Management Resources</a>', unsafe_allow_html = True)
colt[1].write('<a href="#chapterc">Contribute or Report Issues</a>', unsafe_allow_html = True)
colt[1].write('<a href="#chaptert">Theme Update</a>', unsafe_allow_html = True)
colt[1].write('<a href="#chapterp">Print to PDF</a>', unsafe_allow_html = True)
colt[2].write('<a href="#chaptertm">Start a Project using a Template</a>', unsafe_allow_html = True)


st.subheader("Charter", anchor="chapterh1")
st.write('<a href="#toc">Back to Top</a>', unsafe_allow_html = True)
video_file_name = "assets/images/printcharter.webm"
colsd = st.columns(2)
video_file = open(video_file_name, "rb")
video_bytes = video_file.read()
colsd[0].write("The Charter is a document prepared from the planning form. The project manager shares the charter document with the stakeholders, enable discussions to obtain agreement and acceptance.   When the information in the charter is final, close the Project planning phase, and start monitoring and controlling activities. ")
colsd[1].video(video_bytes)

st.subheader("Scope and Askme", anchor="chapterh2")
st.write('<a href="#toc">Back to Top</a>', unsafe_allow_html = True)
video_file_name = "assets/images/askme.webm"
colsd = st.columns(2)
video_file = open(video_file_name, "rb")
video_bytes = video_file.read()
colsd[0].video(video_bytes)
colsd[1].write("The purpose, benefits, scope and related sections have a feature to assist the project manager to prepare a charter by providing the framework and the initial content.  Askme is using HuggingChat assistants.  To use the feature, check that the output box is not filled in, then check the box Askme.  The question will be displayed and the response will be supplied below.  Copy the response to the form and edit as needed. Project name must have a value to use the feature. This feature is a result of the great work at hugging face. Huggingface is open source tools and models to solve AI problems. https://towardsdatascience.com/whats-hugging-face-122f4e7eb11a ")

st.subheader("Contribute", anchor="chapterc")
st.write('<a href="#toc">Back to Top</a>', unsafe_allow_html = True)

st.markdown("#### Git")
st.write("This project is public and shared, if you have issues, please report on git.  https://github.com/jlastwood/pmstreamlit.  If you would like to share information or have a question, please send email to thepmmonitor@gmail.com  ") 

st.markdown("#### Services")
st.write("The author provides consulting and business process management services. Visit https://bluezoneit.com for a list of services and contact information ") 

st.markdown("#### Buy me a coffee")
st.write("Are you interested in supporting this project with additional features or ideas, please buy me a coffee. Your investment will go to improvements for the community.  https://buymeacoffee.com/thepmmonitor  ") 
button(username="thepmmonitor", floating=False)

st.markdown("#### Credits")
st.write(" a lot, get from source, streamlit, the python community")

st.markdown("#### Cheche-pm")
st.write(" Thank you to the developer of the python module to calculate critical path,  https://medium.com/@luisfernandopa1212/efficient-project-scheduling-with-python-the-critical-path-method-19a3f8235f91")


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

st.subheader("Theme", anchor="chaptert")
st.write('<a href="#toc">Back to Top</a>', unsafe_allow_html = True)
st.write("Using streamlit theme under settings, you can change the colors of the view and reports using light, dark, or custom themes.  ")

st.subheader("Print to PDF", anchor="chapterp")
st.write('<a href="#toc">Back to Top</a>', unsafe_allow_html = True)
st.write("Print to PDF of the charter and canvas are using browser print.  Collapse the left navigation bar and set browser width to page width before printing.  If the text is cutoff adjust the browser width.   ")

st.subheader("Start a project with a template", anchor="chaptertm")
imtm = Image.open("assets/images/thepmtemplates.png")
st.write('<a href="#toc">Back to Top</a>', unsafe_allow_html = True)
colsd = st.columns(2)
colsd[0].image(imtm)
colsd[1].write(" Throughout my career I have been asked to create plans and I like to reuse plans, especially when they resulted in successful outcomes.  We have shared some plans here to give you a starting point for your next project.  ")


st.subheader("Resources and Books", anchor="chapterbooks")
st.write('<a href="#toc">Back to Top</a>', unsafe_allow_html = True)
st.write("This project was born from project management templates and forms using sheets https://docs.google.com/spreadsheets/d/1ubIRBmCT3wflP2_MozgJV-Tny7aZfcWBuo1kLx1vVgI/edit?usp=sharing  and the PMBOK list of forms  https://www.wiley.com/en-ca/A+Project+Manager's+Book+of+Forms:+A+Companion+to+the+PMBOK+Guide,+3rd+Edition-p-9781119393986")
st.write("The following are links to resources, books and materials to learn and understand Project Planning, monitoring and control.")
st.link_button("Project Management", "https://en.wikipedia.org/wiki/Project_management")
st.link_button("Wiley Book of Forms", "https://books.wiley.com/titles/9781119393986/")
st.link_button("PMBOK Guide", "https://www.pmi.org/pmbok-guide-standards/foundational/pmbok")
st.link_button("Resource Library", "https://www.pmi.org/learning/library")
st.write("##")
successmsg = f'Thank you for using The PM Monitor. https://thepmmonitor.streamlit.app '
st.success(successmsg)
