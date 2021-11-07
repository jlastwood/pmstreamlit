"""Main module for the streamlit app"""
import streamlit as st

import awesome_streamlit as ast
import src.pages.about
import src.pages.gallery.index
import src.pages.home
import src.pages.resources
import src.pages.vision
import src.pages.plan
import src.pages.risks
import src.pages.canvas
import src.pages.messages

ast.core.services.other.set_logging_format()

PAGES = {
    "Home": src.pages.home,
    "Plan": src.pages.plan,
    "Risks": src.pages.risks,
    "Canvas": src.pages.canvas,
    "Messaging": src.pages.messages,
    "Resources": src.pages.resources,
    "Gallery": src.pages.gallery.index,
    "Vision": src.pages.vision,
    "About": src.pages.about,
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("Contribute")
    st.sidebar.write(
        "This an open source project, "
        "submit comments, questions, as  "
        "[issues](https://github.com/jlastwood/pmstreamlit/issues) "
    )
    st.sidebar.title("About")
    st.sidebar.write(
        """
        This app is maintained by Janet Astwood. You can learn more about me at
        [bluezoneit.com](https://bluezoneit.com).
"""
    )

if __name__ == "__main__":
    main()
