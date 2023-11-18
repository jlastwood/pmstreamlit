"""Home page shown when the user enters the application"""
import streamlit as st
from PIL import Image
import pandas as pd
from scripts.thepmutilities import reporttitle, gradiant_header
import re

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
#    <style>
#        header {visibility: hidden;}
#    </style>
#'''
#st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.markdown("""
    <style>
        @media print {
            @page {size: A4 landscape; margin: 27mm 16mm 27mm 16mm; }
            body { margin: 0; padding: 0; }
            header {display: none !important;}
            /* Hide the Streamlit menu and other elements you don't want to print */
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            [data-testid="stDecoration"] { display: none !important; }
            [data-testid="stToolbar"] { display: none !important; }
            .css-1iyw2u1 { display: none; }
            .css-15yd9pf { display: none; }
            .css-fblp2m { display: none; }
            .main {
                max-width: 100% !important;
            }
            .stHeadingContainer {
              page-break-before: always;
            }
            span, p, div, textarea, input {
                color: #textcolor !important;
            }

            .stMarkdown, .stCodeBlock, [data-testid="caption"], [data-testid="stMarkdownContainer"], [data-testid="stImage"], [data-baseweb="textarea"] {
                max-width: 100% !important;
                word-break: break-all;
                break-inside: avoid;
            }
            #MainMenu{visibility: hidden;} footer{visibility: hidden;} header {visibility: hidden;}
            #root>div:nth-child(1)>div>div>div>div>section>div{padding-top: .2rem;
        }
    </style>
""", unsafe_allow_html=True)

if 'thepmheader' not in st.session_state:
 st.warning("Plan is missing.  Please enter or import a plan")
 st.stop()

#reporttitle("Final Report", st.session_state['thepmheader'])

with st.spinner("Loading Home ..."):

    gradiant_header ('The PM Monitor Project Charter')
    st.markdown("<br><br><p style='text-align: center; vertical-align: bottom; font-size: 200%;'>" + st.session_state.plpname + "</p><br><br>",  unsafe_allow_html=True)
    st.markdown("<br><br><p style='text-align: center; vertical-align: bottom; font-size: 200%;'>" + st.session_state.plpmname + "</p><br><br>",  unsafe_allow_html=True)
    st.markdown("<br><br><p style='text-align: center; vertical-align: bottom; font-size: 200%;'>" + st.session_state.pldplandate.strftime('%d-%m-%Y') + "</p><br><br>",  unsafe_allow_html=True)

    st.header(":classical_building: Project Information", anchor=False, help="overview", divider="rainbow")
    st.write(
            """
The PM Monitor charter describes the project plan, goals, objectives and status at key phases of the project, initiation, issue identification and closure.     
    """
        )
    st.write("##### Overview")
    st.write(st.session_state.thepmplannote)

    st.write("##### Objectives")
    st.write(st.session_state.plspurpose)

    st.write("##### Benefits")
    st.write(st.session_state.plsbenefits)
    st.write("##### Return on Investment")
    st.write(st.session_state.thepmroisummary)
    st.write(st.session_state.plproigoal)

    st.header(":classical_building: Scope", anchor=False, help="overview", divider="rainbow")
    st.write("#### Product Scope")
    st.write("##### Must have Scope")
    st.write(st.session_state.plscopemusthave)
    st.write("##### Optional or Nice to have Scope")
    st.write(st.session_state.plscopenicetohave)
    st.write("##### Out of Scope")
    st.write(st.session_state.plscopeoutofscope)
    st.write("#### Environment")
    st.write("Non functional deliverables - ",', '.join(st.session_state.plmlistscopelist))
    st.write("Technology deliverables - ",', '.join(st.session_state.plmlistscopeoption))
    st.write("Quality reports - ",', '.join(st.session_state.plmlistqualitytypes))
    st.write("#### Benchmarks")
    st.write(st.session_state.plsbenchmarks)
    st.write("#### Changes")
    st.write(st.session_state.plscopechange)

    st.header(":classical_building: Quality and Grade", anchor=False, help="overview", divider="rainbow")
    st.write("**Goal**")
    st.write(st.session_state.plsqualitygoal)
    st.write("**Quality**")
    st.write(st.session_state.thepmquality)
    st.write("**Grade**")
    st.write(st.session_state.thepmgrade)

    st.header(":classical_building: Stakeholders and Approvers", anchor=False, help="overview", divider="rainbow")
    col1, col2 = st.columns(2)
    with col1:
     v=f"**Sponsor:** {st.session_state.plspname}"
     st.markdown(v)
     v=f"**Account Manager:** {st.session_state.plpaccountname}"
     st.markdown(v)
     v=f"**Quality Inspector:** {st.session_state.plpinspectorname}"
     st.markdown(v)
     v=f"**Business Project Manager:** {st.session_state.plpmcustname}"
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

    st.header(":classical_building: Financials", anchor=False, help="overview", divider="rainbow")
    st.write("The planned investment in Product Design and Delivery is ", st.session_state.plnbudget)
    st.write("**Earned Value**")
    st.write(st.session_state.thepmevsummary)
    st.table(st.session_state.thepmevm)
    #st.dataframe(st.session_state.thepmevm, hide_index=True, use_container_width=True)
    st.header(":classical_building: Resources and Risks", anchor=False, help="overview", divider="rainbow")

    impactlist = ['High','Very Low', 'Low', 'Moderate', 'High', 'Very High']
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
 
