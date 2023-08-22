import streamlit as st
from PIL import Image

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
st.markdown("### About")

st.subheader("Services")

st.subheader("Trust and Virtual Teams")

st.write("https://www.flashhub.io/virtuelle-organisationen-live/")
st.session_state.plpname = st.session_state.plpname
st.subheader("Credits")
st.write(" a lot, get from source, streamlit, the python community")
