"""Page for nlp of the project report"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import pandas as pd
import hydralit_components as hc
from collections import Counter
from utilities import currencyrisk, evreport, plancomment, get_table_download_link
#from st_radial import st_radial
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
 
#@st.cache
#with st.spinner("Loading  ..."):
    # initialize session state variables
if 'plnumber' not in st.session_state:
 st.session_state.plnumber = ""
if 'plcsmcomment' not in st.session_state:
 st.session_state.plcsmcomment = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "collapsed"
    st.session_state.disabled = False

videopmreport="https://www.youtube.com/watch?v=c4fEms85NQQ"
videoidreport="c4fEms85NQQ"
    #videopmreport="https://www.youtube.com/watch?v=qWdyhFiyH0Y&t=10s"
st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Stoplight Report</h4><br>", unsafe_allow_html=True)
transcript=YouTubeTranscriptApi.get_transcript(videoidreport)
formatter = TextFormatter()
text_formatted = formatter.format_transcript(transcript)
textcsm = TextBlob(text_formatted) #sentiment for each sentence
daytoday = datetime.date.today()
cpi = int(st.session_state.thepmcpi)
spi = int(st.session_state.thepmspi)
bar_theme_2 = {'bgcolor': 'grey','content_color': 'black','progress_color': 'green'}

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

## output the header
st.table(st.session_state.thepmheader)

st.markdown("---")

cola, colb, colc = st.columns([2,1,4])
with cola:
  st.write("Schedule")
with colb:
  hc.progress_bar(st.session_state['thepmtimecomplete'],'Percent complete',key='paschedule',sentiment='good')
with colc:
  st.markdown("<font color='grey'>:warning: THIS TEXT WILL CHANGE COLOR</font>", unsafe_allow_html=True)
cola, colb, colc = st.columns([2,1,4])
with cola:
  st.write("Scope")
with colb:
  hc.progress_bar(35,'Something something - 2a',key='pascope',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.markdown("<font color='red'>THIS TEXT WILL CHANGE COLOR</font>", unsafe_allow_html=True)
cola, colb, colc = st.columns([2,1,4])
with cola:
  st.write("Cost")
with colb:
  hc.progress_bar(35,'Something something - 2a',key='pacost',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.markdown("<font color='red'>THIS TEXT WILL CHANGE COLOR</font>", unsafe_allow_html=True)
cola, colb, colc = st.columns([2,1,4])
with cola:
  st.write("Risk")
with colb:
  hc.progress_bar(35,'Something something - 2a',key='parisk',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.markdown("<font color='red'>There are 6 high risk probable risks</font>", unsafe_allow_html=True)
cola, colb, colc = st.columns([2,1,4])
with cola:
  st.write("Issues")
with colb:
  hc.progress_bar(35,'Something something - 2a',key='paissues',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.markdown("<font color='red'>There are 2 issues related to risk or contingency activities in force</font>", unsafe_allow_html=True)
st.markdown("---")
cola, colb, colc = st.columns([2,1,4])
with cola:
  st.write("Planned Completion")
with colb:
  hc.progress_bar(35,'Something something - 2a',key='paplanned',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.markdown("<font color='red'>THIS TEXT WILL CHANGE COLOR</font>", unsafe_allow_html=True)
with cola:
  st.write("Estimated Completion")
with colb:
  hc.progress_bar(35,'Something something - 2a',key='paestimate',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.markdown("<font color='red'>Estimate to complete is</font>", unsafe_allow_html=True)
st.markdown("---")
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
 #st.write("text sentiment", textcsm.sentiment_assessments)
 #st.write(Counter(tags).most_common(5))
 nouns = list()
 for word, tag in textcsm.tags:
   if tag == 'NN':
     nouns.append(word.lemmatize())
 st.write ("This report theme is ...")
 st.write(str(dict(Counter(nouns).most_common(5))))
 #for item in nouns:
   #word = Word(item)
 #  st.write (item)
