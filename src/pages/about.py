"""Home page shown when the user enters the application"""
import streamlit as st

import awesome_streamlit as ast


# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading About ..."):
        ast.shared.components.title_awesome(" - About")
        st.markdown(
            """## Contributions

This an open source project and you are very welcome to **contribute** your awesome
comments, questions, resources and apps as
[issues](https://github.com/jlastwood/project/issues) or
[pull requests](https://github.com/jlastwood/project/pulls)
to the [source code](https://github.com/jlastwood/project).

## The Developer
For more details about the author Janet Astwood see [Author](https://bluezoneit.com).

## Credits
This project is in part a result of the contributions to awesome streamlit by Marc Skov Madsen.  
[datamodelsanalytics.com](https://datamodelsanalytics.com).
""",
            unsafe_allow_html=True,
        )
