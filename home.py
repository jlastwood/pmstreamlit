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
#import src.pages.messages

# ast.core.services.other.set_logging_format()

#PAGES = {
#    "Connect": src.pages.messages,
#}

def main():
    """Main function of the App"""

    st.image('assets/images/The PM Monitor Plan.png', caption='The PM Monitor Risk')

    st.markdown("---")
    url1 = "/plan"
    st.markdown(f'''
<a href={url1}><button style="background-color:#F4A261;text-align: center;">  Start Planning  </button></a>
''',
unsafe_allow_html=True)
    #url2 = "/identify"
    #st.write("Review Risks [link](%s)" % url2)

#    st.sidebar.title("Navigation")
#    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

#    page = PAGES[selection]
#    with st.spinner(f"Loading {selection} ..."):
#        ast.shared.components.write_page(page)

    st.sidebar.title("Contribute")
    st.sidebar.write(
        "This an open source project, submit comments, questions, as  "
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
