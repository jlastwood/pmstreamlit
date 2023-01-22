"""Page for nlp of the project report"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import pandas as pd
import hydralit_components as hc
from collections import Counter
from utilities import currencyrisk, evreport, plancomment, get_table_download_link, reporttitle
#from st_radial import st_radial
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
 
#@st.cache
#with st.spinner("Loading  ..."):
    # initialize session state variables
if 'thepmheader' not in st.session_state:
 st.warning("Sorry, plan is missing.  Please enter or import a plan")
 st.stop()

if 'plcsmcomment' not in st.session_state:
 st.session_state.plcsmcomment = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "collapsed"
    st.session_state.disabled = False

videopmreport="https://www.youtube.com/watch?v=c4fEms85NQQ"
videoidreport="c4fEms85NQQ"
    #videopmreport="https://www.youtube.com/watch?v=qWdyhFiyH0Y&t=10s"
transcript=YouTubeTranscriptApi.get_transcript(videoidreport)
formatter = TextFormatter()
text_formatted = formatter.format_transcript(transcript)
textcsm = TextBlob(text_formatted) #sentiment for each sentence
daytoday = datetime.date.today()
cpi = int(st.session_state.thepmcpi)
spi = int(st.session_state.thepmspi)
bar_theme_2 = {'bgcolor': 'lightgrey','content_color': 'grey','progress_color': 'green'}

reporttitle("Stoplight Report", st.session_state['thepmheader'])

cola, colb, colc, cole = st.columns([1,2,1,4])
with cola:
  st.write("Schedule")
with colb:
  hc.progress_bar(st.session_state['thepmtimecomplete'],'Time',key='paschedule',sentiment='good')
with colc:
  st.write(int(st.session_state['thepmspi']*100), st.session_state['thepmtimecomplete'])
with cole:
  if st.session_state['thepmspi'] < 1:
    notes = "<font color='grey'>:warning:" + " Behind schedule - Contingency: " + st.session_state['plptimecontingency'] + "</font>"
  else:
    notes = "<font color='grey'>" + "On or ahead of schedule" + "</font>"
  st.markdown("{}".format(notes), unsafe_allow_html=True)
cola, colb, colc, cole = st.columns([1,2,1,4])
with cola:
  st.write("Scope")
with colb:
  scopebar =  st.session_state['thepmdelivery']
  hc.progress_bar(scopebar,'Features',key='pascope',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.write(scopebar)
with cole:
  if st.session_state['plscopechangeadd'] != "None":
    notec = "<font color='grey'>:warning:" + st.session_state['plpscopecontingency'] + "</font>"
  else:
    notec = ""
  st.markdown("{}".format(notec), unsafe_allow_html=True)
cola, colb, colc, cole = st.columns([1,2,1,4])
with cola:
  st.write("Quality")
with colb:
  qualbar = 0
  if int(st.session_state['plntests']) > 0:
   qualbar = int(st.session_state['plntestsfailed'] / st.session_state['plntests'] * 100)
  hc.progress_bar(qualbar,'Quality',key='paqual',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.write(qualbar)
with cole:
  if int(st.session_state['thepminspectionflag']) == 1:
    notec = "<font color='grey'>:warning:" + st.session_state['thepminspectionwarning'] + st.session_state['plpscopecontingency'] + "</font>"
  else:
    notec = ""
  st.markdown("{}".format(notec), unsafe_allow_html=True)
cola, colb, colc, cole = st.columns([1,2,1,4])
with cola:
  st.write("Cost")
with colb:
  hc.progress_bar(st.session_state['thepmbudgetcomplete'],'Cost',key='pabudget',sentiment='good')
with colc:
  st.write(st.session_state['thepmbudgetcomplete'], st.session_state['thepmcpi'])
with cole:
  if st.session_state['thepmcpi'] < 1:
    notes = "<font color='grey'>:warning:" + "Over Budget - Contingency:  " + st.session_state['plpbudgetcontingency'] + "</font>"
  else:
    notes = "<font color='grey'>" + "On or ahead of budget" + "</font>"
  st.markdown("{}".format(notes), unsafe_allow_html=True)
cola, colb, colc, cole = st.columns([1,2,1,4])
with cola:
  st.write("Risk")
with colb:
  riskbar = 15
  hc.progress_bar(riskbar,'Risk',key='parisk',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.write(riskbar)
with cole:
  # if there are open risks, and probability is 100 and impact is high
  st.markdown("<font color='grey'>Risks have become issues and require management action</font>", unsafe_allow_html=True)
st.markdown("---")
cola, colb, colc = st.columns([2,2,4])
with cola:
  st.write("Planned Completion")
with colb:
  st.write(st.session_state['pldenddate'])
with colc:
  st.markdown("<font color='red'></font>", unsafe_allow_html=True)
with cola:
  st.write("Estimate to Complete")
with colb:
  st.session_state['thepmtimecomplete']
with colc:
  st.markdown("<font color='red'><font>", unsafe_allow_html=True)
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
