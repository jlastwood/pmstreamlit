"""Home page shown when the user enters the application"""
import streamlit as st
from PIL import Image
import pandas as pd
from scripts.thepmutilities import reporttitle, gradiant_header
import re
from scripts.riskgenerate import calculate_risks_json
from scripts.cssscripts import page_media_print
import altair as alt

# get a list of the bullet points 
def split(s):
    thislist = []
    start = 0
    for i in [1,2,3,4,5,6,7,8]:
      txt = str(i) + '.'
      fins = s.find(txt, start)
      if fins > 0:
        end = s.find(":", fins)
        if end < 0:
          end = find + 15
        getstring = s[fins:end]
        thislist.append(getstring)
        start = fins + 3
    return thislist

st.session_state.update(st.session_state)

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Charter Report",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

#  get the theme colors
#  https://blog.streamlit.io/accessible-color-themes-for-streamlit-apps/

#hide_decoration_bar_style = '''
#   <style>
#       header {visibility: hidden;}
#   </style>
#'''
#st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

#  create media print
page_media_print()

if 'thepmheader' not in st.session_state:
 st.warning("Plan is missing.  Please enter or import a plan")
 st.stop()

with st.spinner("Preparing Charter Report ..."):

#    gradiant_header ('The PM Monitor Project Charter')

    st.markdown("<br><br><p style='text-align: center; vertical-align: bottom; font-size: 200%;'>" + st.session_state.plpname + "</p><br><br>",  unsafe_allow_html=True)
    st.markdown("<br><br><p style='text-align: center; vertical-align: bottom; font-size: 200%;'>Project Manager: " + st.session_state.plpmname + "</p><br><br>",  unsafe_allow_html=True)
    st.markdown("<br><br><p style='text-align: center; vertical-align: bottom; font-size: 200%;'>Sponsor: " + st.session_state.plspname + "</p><br><br>",  unsafe_allow_html=True)
    st.markdown("<br><br><p style='text-align: center; vertical-align: bottom; font-size: 200%;'>Report Date:  " + st.session_state.pldplandate.strftime('%d-%m-%Y') + "</p><br><br>",  unsafe_allow_html=True)


    st.header("Table of Contents", anchor='toc', help="overview", divider="rainbow")
    st.write('<a href="#chapter1">Project Overview</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter2">Scope</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter3">Definitions and Terms</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter4">Requirements</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter5">Change Management</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter6">Quality and Grade</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter7">Stakeholders</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter8">Milestones</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter9">Communication Plan</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter10">Financial Information</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter11">Team and WBS</a>', unsafe_allow_html = True)
    st.write('<a href="#chapter12">Risk and Contingency Plans</a>', unsafe_allow_html = True)

    st.header("Overview and Benefits", anchor='chapter1', help="overview", divider="rainbow")
    st.write(
            """
The PM Monitor charter describes the plan, goals, objectives of the project.     
    """
        )
    st.write("##### Overview")
    st.write(st.session_state.thepmplannote)

    st.write("##### Objectives")
    st.write(st.session_state.plspurpose)
    st.markdown("<h6></h6>", unsafe_allow_html=True)

    st.write("##### Benefits")
    st.write(st.session_state.plsbenefits)

    st.markdown("<h6></h6>", unsafe_allow_html=True)
    st.write("##### Return on Investment")
    st.write(st.session_state.thepmroisummary)
    st.write(st.session_state.plproigoal)

    st.header("Scope", anchor='chapter2', help="overview", divider="rainbow")
    st.write("#### Product Scope")
    st.write("##### Must have Scope")
    st.write(st.session_state.plscopemusthave)
    if len(st.session_state.plscopemusthave) > 1000:
      st.markdown("<h6></h6>", unsafe_allow_html=True)
    st.write("##### Optional or Nice to have Scope")
    st.write(st.session_state.plscopenicetohave)
    st.write("##### Out of Scope")
    st.write(st.session_state.plscopeoutofscope)
    st.write("#### Environment")
    st.write("Non functional deliverables - ",', '.join(st.session_state.plmlistscopelist))
    st.write("Technology deliverables - ",', '.join(st.session_state.plmlistscopeoption))
    st.write("#### Benchmarks")
    st.write(st.session_state.plsbenchmarks)

    st.header("Definitions and Terms", anchor='chapter3', help="overview", divider="rainbow")
    st.write(st.session_state.plscopeterms)
    
    st.header("Requirements", anchor='chapter4', help="overview", divider="rainbow")
    st.write("#### Use Case or Process Steps")
    st.write(st.session_state.plsusecase)

    st.header("Change Management Plan", anchor='chapter5', help="overview", divider="rainbow")
    st.write("#### Change Management Plan")
    st.write(st.session_state.plschangeplan)
    st.write("The following changes have occurred.  A change is usually recorded to correct, mitigate or avoid a risk or issue.")
    st.write(st.session_state.plscopechange)
    st.write(st.session_state.plsotherchange)
    st.write("Approval and Justification:")
    st.write(st.session_state.plsapprovalchange)

    st.header("Quality and Grade", anchor='chapter6', help="overview", divider="rainbow")
    st.write("**Goal**")
    st.write(st.session_state.plsqualitygoal)
    st.write("**Quality**")
    st.write(st.session_state.thepmquality)
    st.write("**Grade**")
    st.write(st.session_state.thepmgrade)
    st.write("**Quality Reports**")
    st.write(', '.join(st.session_state.plmlistqualitytypes))
    st.write(st.session_state.plsqualityreport)

    st.header("Stakeholders", anchor='chapter7', help="overview", divider="rainbow")
    st.write("The following people are contributors, interested parties and collaborators.")
    col1, col2 = st.columns(2)
    with col1:
     v=f"**Sponsor:** {st.session_state.plspname}"
     st.markdown(v)
     v=f"**Account Manager:** {st.session_state.plpaccountname}"
     st.markdown(v)
     v=f"**Quality Inspector:** {st.session_state.plpinspectorname}"
     st.markdown(v)
     v=f"**Product Owner:** {st.session_state.plpmcustname}"
     st.markdown(v)
     v=f"**Process Owner:** {st.session_state.plpprocowner}"
     st.markdown(v)
     v=f"**Staffing Manager::** {st.session_state.plpmhrname}"
     st.markdown(v)
    with col2:
     v=f"**Project Manager:** {st.session_state.plpmname}"
     st.markdown(v)
     v=f"**Operations Manager:** {st.session_state.plpoperationname}"
     st.markdown(v)
     v=f"**Solution Architect:** {st.session_state.plpsolutionname}"
     st.markdown(v)
     v=f"**Controller Finance:** {st.session_state.plpfinancename}"
     st.markdown(v)
     v=f"**Purchasing Manager::** {st.session_state.plppurchasingname}"
     st.markdown(v)

    st.header("Milestones", anchor='chapter8', help="overview", divider="rainbow")
    st.write("The following chart shows the project status reports and the product milestones.  The project manager reports activity to the stakeholders at regular intervals and at milestones using the Stoplight report")
    chart = alt.Chart(st.session_state.thepmmilestones).mark_line(point = True).encode(
          alt.X('yearmonthdate(reportdate):O', title='Report Date'),
          alt.Y('yearmonthdate(plandate):O', title='Plan Date', scale=alt.Scale(reverse=True)),
          color="Milestone", text="Milestone")
    st.altair_chart(chart, use_container_width=True)
    st.header("Communication Plan and Media links", anchor='chapter9', help="overview", divider="rainbow")
    st.write("The project manager will report project status using the Stoplight report at regular intervals.  Information about the project, artefacts and the calendar are available at the following locations.")
    col1, col2 = st.columns(2)
    with col1:
     v=f"**Live Site:** {st.session_state.plplivesitelink}"
     st.markdown(v)
     v=f"**Design Board:** {st.session_state.plpproductownerdesignlink}"
     st.markdown(v)
     v=f"**Documents:** {st.session_state.plpdocumentslink}"
     st.markdown(v)
     v=f"**Documents (private):** {st.session_state.plpdocumentsprivatelink}"
     st.markdown(v)
     v=f"**Chat/message Users:** {st.session_state.plpstanduplinkusers}"
     st.markdown(v)
    with col2:
     v=f"**Stage Site:** {st.session_state.plpstagesitelink}"
     st.markdown(v)
     v=f"**Team Task Board:** {st.session_state.plpactivitylink}"
     st.markdown(v)
     v=f"**Source Code:** {st.session_state.plpgithublink}"
     st.markdown(v)
     v=f"**Chat/message team:** {st.session_state.plpstanduplink}"
     st.markdown(v)
     v=f"**Calendar team:** {st.session_state.plpteamcalendar}"
     st.markdown(v)

    st.header("Financials", anchor='chapter10', help="overview", divider="rainbow")
    st.write("The planned investment in Product Design and Delivery is ", st.session_state.plnbudget)
    st.write("Cost Summary: ", st.session_state.plscostgoal)

    st.write("**Earned Value**")
    st.write(st.session_state.thepmevsummary)
    st.table(st.session_state.thepmevm)
    #st.dataframe(st.session_state.thepmevm, hide_index=True, use_container_width=True)
    st.header("Team", anchor='chapter11', help="overview", divider="rainbow")
    st.write("***Team Information***")
    st.write(st.session_state.thepmteam, " The team consists of the following roles: ", ' '.join(st.session_state.plmlistroles))
    st.write("***Tasks***")
    st.markdown(st.session_state.plswbs, unsafe_allow_html=True)
    st.write("***Team Contingency Plans***")
    st.write(st.session_state.plpteamcontingency)

    impactlist = ['High','Very Low', 'Low', 'Moderate', 'High', 'Very High']
    st.header("Risks and Contingency Plans", anchor='chapter12', help="overview", divider="rainbow")
    st.write("The risk register is pre-popluated with the PM monitor risks.  The team has set the impact of risks by area as follows, and identified mitigation strategies.  The risk owners are asked to review risks and issues each reporting period and to alert the Project Manager when risks become issues")
    v=f"**Scope Impact** {st.session_state.plnscoperange}-{impactlist[st.session_state.plnscoperange]}"
    st.write(v)
    st.write(st.session_state.plpscopecontingency)
    v=f"**Schedule Impact** {st.session_state.plnschedulerange}-{impactlist[st.session_state.plnschedulerange]}"
    st.write(v)
    st.write(st.session_state.plptimecontingency)
    v=f"**Cost Impact** {st.session_state.plnbudgetrange}-{impactlist[st.session_state.plnbudgetrange]}"
    st.write(v)
    st.write(st.session_state.plpbudgetcontingency)
    v=f"**Team Impact** {st.session_state.plnteamrange}-{impactlist[st.session_state.plnteamrange]}"
    st.write(v)
    st.write(st.session_state.plpteamcontingency)
    v=f"**Resource Impact** {st.session_state.plnresourcerange}-{impactlist[st.session_state.plnresourcerange]}"
    st.write(v)
    st.write(st.session_state.plpresourcecontingency)
    st.markdown('##')

    #phasenumber = st.session_state.thepmphase
    #CPI = st.session_state.thepmcpi
    #SPI = st.session_state.thepmspi
    #engagementscoreteam = st.session_state.plnactivesam
    #sentimentscoreteam = st.session_state.plnactiveses
    #retention = st.session_state.plnopenroles
    #scopechange = len(st.session_state.plscopechange.split(".")) 
    #if len(st.session_state.plscopechange) < 6:
    #   scopechange = 0
    #earnedvalue = st.session_state.plnactiveses
    #roi = st.session_state.thepmannualroi
    #latestart = st.session_state.plnactiveses
    #inspectfail = st.session_state.plntestsfailed

    st.write("Risks are identified as issues when the risk is trigged during project monitoring.  Risks triggered are reported on the stoplight report with owner and recommended action.") 
    (myrisks, issues, risks, totalrisks, risksummary)  = calculate_risks_json() 

    st.subheader("Risks by Owner and Classification")
    heatmap = alt.Chart(myrisks.dropna()).mark_rect().encode(
       alt.X('riskowner', title="Owner", scale=alt.Scale(reverse=True)),
       alt.Y('riskclassification', title="Classification"),
       alt.Color('count()', scale=alt.Scale(scheme='lightgreyred'))
             )

    points = alt.Chart(myrisks).mark_circle(
       color='black',
       size=5,
     ).encode(
       x='riskowner',
       y='riskclassification',
     )
      
    f = heatmap + points
    st.altair_chart(f, use_container_width=True)

st.write("##")
st.markdown("### Blank Page", unsafe_allow_html=True)
st.markdown("<footer> my footer </footer>", unsafe_allow_html=True)
#st.markdown(str(foot), unsafe_allow_html=True)
#successmsg = f'The PM Monitor project charter presented by {st.session_state.plpmname} on {st.session_state.pldcharterdate}.  Thank you for using The PM Monitor '
#st.success(successmsg)
