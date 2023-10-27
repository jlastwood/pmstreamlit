"""Home page shown when the user enters the application"""
import streamlit as st
from PIL import Image
from scripts.thepmutilities import reporttitle, gradiant_header

st.session_state.update(st.session_state)

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Charter Report",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

#  get the theme colors
color1t = st._config.get_option('theme.primaryColor')
color1b = st._config.get_option('theme.secondaryBackgroundColor')
color1c = st._config.get_option('theme.backgroundColor')
color1d = st._config.get_option('theme.textColor')

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
                max-width: 15in !important;
            }

            span, p, div, textarea, input {
                color: #textcolor !important;
            }

            .stMarkdown, .stCodeBlock, [data-testid="caption"], [data-testid="stMarkdownContainer"], [data-testid="stImage"], [data-baseweb="textarea"] {
                max-width: 15in !important;
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

# pylint: disable=line-too-long
#reporttitle("Final Report", st.session_state['thepmheader'])

with st.spinner("Loading Home ..."):

    gradiant_header (color1t, color1b, color1c, 'The PM Monitor Project Charter')
    #st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Planning</p>",  unsafe_allow_html=True)
    st.write(
            """

The PM Monitor charter describes the project plan, goals, objectives and status at key phases of the project, initiation, issue identification and closure.   It is a written narrative that is delivered to the stakeholders.  

    """
        )

    st.header(":classical_building: Project Information", anchor=False, help="overview", divider="rainbow")
    st.write(st.session_state.thepmplannote)

    st.subheader("Objectives")
    st.write(st.session_state.plspurpose)

    st.subheader("Benefits")
    st.write(st.session_state.plsbenefits)

    st.subheader("Project Achievements")

    st.header(":classical_building: Scope", anchor=False, help="overview", divider="rainbow")
    st.subheader("Product Scope")
    st.write(st.session_state.plscopemusthave)
    st.subheader("Scope Changes")
    st.write(st.session_state.plscopechange)

    st.header(":classical_building: Quality and Grade", anchor=False, help="overview", divider="rainbow")


    st.header(":classical_building: Stakeholders and Approvers", anchor=False, help="overview", divider="rainbow")
    v=f"**Sponsor:** {st.session_state.plspname}"
    st.markdown(v)
    st.subheader("Environment")

    st.header(":classical_building: Resources and Risks", anchor=False, help="overview", divider="rainbow")

    st.subheader("ROI and Cost Summary")
    st.markdown('##')
 
