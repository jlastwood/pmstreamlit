"""Page for nlp of the project report"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import pandas as pd
from collections import Counter
from utilities import currencyrisk, evreport, plancomment, get_table_download_link
from st_radial import st_radial
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
 
@st.cache
def get_report_markdown() -> str:
    """Enter the plan and return CPI and SPI
    """
    url = pathlib.Path(__file__).parent.parent.parent / "AWESOME-STREAMLIT.md"
    with open(url, mode="r") as file:
        readme_md_contents = "".join(file.readlines())
    return readme_md_contents.split("\n", 3)[-1]

def write():
    """Method used to write the page in the app.py file"""
    ast.shared.components.title_awesome("Report")
    # with st.spinner("Loading  ..."):

    # initialize session state variables
    if 'plnumber' not in st.session_state:
     st.session_state.plnumber = ""
    if 'plcsmcomment' not in st.session_state:
     st.session_state.plcsmcomment = ""

    videopmreport="https://www.youtube.com/watch?v=c4fEms85NQQ"
    videoidreport="c4fEms85NQQ"
    #videopmreport="https://www.youtube.com/watch?v=qWdyhFiyH0Y&t=10s"
    st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Analysis</h4>", unsafe_allow_html=True)
    transcript=YouTubeTranscriptApi.get_transcript(videoidreport)
    formatter = TextFormatter()
    text_formatted = formatter.format_transcript(transcript)
    textcsm = TextBlob(text_formatted) #sentiment for each sentence
    daytoday = datetime.date.today()
    cpi = int(st.session_state.cpi)
    spi = int(st.session_state.spi)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Polarity", textcsm.sentiment.polarity, round(.5-textcsm.sentiment.polarity,2))
    col2.metric("Objectivity", textcsm.sentiment.subjectivity, "")
    col3.metric("Cost Performance", cpi, round(cpi-1,1) )
    col4.metric("Schedule Performance", spi, round(spi-1,1) )
    col5.metric("Engagement", "86%", "4%")
    col1, col2 = st.columns(2)
    with col1:
     st.video(videopmreport, format='video/mp4', start_time=0)
    with col2:
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Management Report</h4>", unsafe_allow_html=True)
     #plcommentsummary = "#### Product Owner says:\n" + plcsmcomment + "\n#### Project Manager says:\n" + plpmcomment + "\n#### Stakeholder action items:\n" + plmgmtactions + "\n\nReport date:" + daytoday.strftime("%Y %m %d")
     #st.markdown(plcommentsummary)
     #st.write(plcsmcomment) #sentiment for each sentence
     #st.write(textcsm.noun_phrases) #extracting polarity of each sentence
     #st.write(textcsm.np_counts) #extracting polarity of each sentence
     #https://textblob.readthedocs.io/en/dev/classifiers.html#classifying-text
     tags = textcsm.tags
     st.write("text sentiment", textcsm.sentiment_assessments)
     #st.write(Counter(tags).most_common(5))
     nouns = list()
     for word, tag in textcsm.tags:
       if tag == 'NN':
         nouns.append(word.lemmatize())
     st.write ("This text is about...")
     st.write(Counter(nouns).most_common(5))
     #for item in nouns:
       #word = Word(item)
     #  st.write (item)
