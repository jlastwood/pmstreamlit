import streamlit as st
from PIL import Image

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor About Page",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

st.markdown("### About")

st.subheader("Services")

st.subheader("Trust and Virtual Teams")

st.write("https://www.flashhub.io/virtuelle-organisationen-live/")
st.session_state.plpname = st.session_state.plpname
st.subheader("Credits")
st.write(" a lot, get from source, streamlit, the python community")
