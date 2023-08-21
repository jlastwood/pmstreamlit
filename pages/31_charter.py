"""Home page shown when the user enters the application"""
import streamlit as st
from PIL import Image
from scripts.thepmutilities import reporttitle

st.session_state.update(st.session_state)

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Final Report",
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
if 'thepmheader' not in st.session_state:
 st.warning("Sorry, plan is missing.  Please enter or import a plan")
 st.stop()

# pylint: disable=line-too-long
reporttitle("Final Report", st.session_state['thepmheader'])

with st.spinner("Loading Home ..."):
    st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Planning</p>", unsafe_allow_html=True)
    st.write(
            """

The PM Monitor final report describes the project plan, goals, objectives and status at the time a project is paused or closed.   It is a written narrative that is delivered to the stakeholders.  

    """
        )

    st.subheader("Project Overview")
    st.write(st.session_state.thepmplannote)

    st.subheader("Project Objectives")
    st.write(st.session_state.plspurpose)

    st.subheader("Product Scope")
    st.write(st.session_state.plscopemusthave)

    st.subheader("Project Benefits")
    st.write(st.session_state.plsbenefits)

    st.subheader("Project Achievements")

    st.subheader("Scope Changes")
    st.write(st.session_state.plscopechange)

    st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Quality and Grade</p>", unsafe_allow_html=True)
    st.subheader("Quality and Grade")

    st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Resources</p>", unsafe_allow_html=True)

    st.subheader("Stakeholders and Approvers")
    v=f"**Sponsor:** {st.session_state.plspname}"
    st.markdown(v)
    st.subheader("Environment")

    st.subheader("Top 3 Risks/Issues")

    st.subheader("ROI and Cost Summary")
    st.markdown('##')
 
