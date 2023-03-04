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
    st.image('assets/images/The PM Monitor Plan.png', caption='The PM Monitor Planner and Risk Management')

    st.markdown("---")
    columns = st.columns((2,1,2))
    url1 = "/plan"
    with columns[1]:
     st.markdown(f'''
<a href={url1} target = "_self"><button style="background-color:#F4A261;text-align: center;">  Start Planning  </button></a>
''',
unsafe_allow_html=True)
    #url2 = "/identify"
    #st.write("Review Risks [link](%s)" % url2)

    st.sidebar.title("Contribute")
    st.sidebar.write(
        "This an open source project, submit comments, questions, as  "
        "[issues](https://github.com/jlastwood/pmstreamlit/issues) "
    )
    st.sidebar.title("About")
    st.sidebar.write(
        """
        Idea, Design and Development by Janet Astwood. More about Janet at
        [bluezoneit.com](https://bluezoneit.com).
"""
    )

if __name__ == "__main__":
    main()
