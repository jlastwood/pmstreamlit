"""Main module for the streamlit app"""
import streamlit as st
from PIL import Image

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

import awesome_streamlit as ast
import src.pages.vision
import src.pages.about
import src.pages.gallery.index
import src.pages.resources
import src.pages.report
import src.pages.change
import src.pages.canvas
import src.pages.messages

# ast.core.services.other.set_logging_format()

PAGES = {
    "Vision": src.pages.vision,
    "Report": src.pages.report,
    "Change": src.pages.change,
    "Canvas": src.pages.canvas,
    "Connect": src.pages.messages,
    "Resources": src.pages.resources,
    "Gallery": src.pages.gallery.index,
    "About": src.pages.about,
}

def main():
    """Main function of the App"""

    st.image('assets/images/The PM Monitor Plan.png', caption='The PM Monitor Risk')

    st.write("getting started with The PM Monitor")
#    st.sidebar.title("Navigation")
#    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

#    page = PAGES[selection]
#    with st.spinner(f"Loading {selection} ..."):
#        ast.shared.components.write_page(page)
    st.sidebar.title("Contribute")
    st.sidebar.write(
        "This an open source project, "
        "submit comments, questions, as  "
        "[issues](https://github.com/jlastwood/pmstreamlit/issues) "
    )
    st.sidebar.title("About")
    st.sidebar.write(
        """
        Idea, Design and Development by Janet Astwood. More about me at
        [bluezoneit.com](https://bluezoneit.com).
"""
    )

if __name__ == "__main__":
    main()
