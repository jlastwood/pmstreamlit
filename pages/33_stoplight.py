"""Page for nlp of the project report"""
from PIL import Image
import streamlit as st
import datetime
import hydralit_components as hc
import heapq
from pandas import * # bad janet! bad! don't import * 
from scripts.thepmutilities import reporttitle
from deepmultilingualpunctuation import PunctuationModel
#from st_radial import st_radial
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.session_state.update(st.session_state)
im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Stoplight Report",
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

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

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

videopmreport=st.session_state.plpmreport
videoidreport=st.session_state.plpmid
#videoidreport="c4fEms85NQQ"
#videopmreport="https://www.youtube.com/watch?v=qWdyhFiyH0Y&t=10s"
if len(videoidreport) > 10:
 transcript=YouTubeTranscriptApi.get_transcript(videoidreport)
 formatter = TextFormatter()
 text_formatted = formatter.format_transcript(transcript)
 model = PunctuationModel(model="oliverguhr/fullstop-punctuation-multilingual-sonar-base")
 textresult = model.restore_punctuation(text_formatted)
 textcsm = TextBlob(textresult) #sentiment for each sentence

daytoday = datetime.date.today()
cpi = round(st.session_state.thepmcpi,1)
spi = round(st.session_state.thepmspi,1)

bar_theme_2 = {'bgcolor': 'lightgrey','content_color': 'grey','progress_color': 'green'}

reporttitle("Stoplight Report", st.session_state['thepmheader'])

cola, colb, colc, cole = st.columns([1,2,1,4])
with cola:
  st.write("Schedule")
with colb:
  hc.progress_bar(st.session_state['thepmtimecomplete'],'Time',key='paschedule',sentiment='good')
with colc:
  st.write(st.session_state['thepmtimecomplete'], spi)
with cole:
  if spi < 1:
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
  if len(st.session_state['plscopechange']) > 10:
    notec = "<font color='grey'>:warning: " + st.session_state['plpscopecontingency'] + "</font>"
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
    notec = "<font color='grey'>:warning: " + st.session_state['thepminspectionwarning'] + st.session_state['plpscopecontingency'] + "</font>"
  else:
    notec = ""
  st.markdown("{}".format(notec), unsafe_allow_html=True)
cola, colb, colc, cole = st.columns([1,2,1,4])
with cola:
  st.write("Cost")
with colb:
  hc.progress_bar(st.session_state['thepmbudgetcomplete'],'Cost',key='pabudget',sentiment='good')
with colc:
  st.write(st.session_state['thepmbudgetcomplete'], cpi)
with cole:
  if cpi < 1:
    notes = "<font color='grey'>:warning: " + "Over Budget - Contingency:  " + st.session_state['plpbudgetcontingency'] + "</font>"
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

st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Stakeholder Action</p>", unsafe_allow_html=True)
actions = DataFrame({'a': [1,2,3], 'b': [2,3,4]})
st.table(actions)
st.write("write out 3 risks that are high probablity and high impact")

if len(videopmreport) < 10:
  st.warning("PM status report is missing.  Please create report with transcript to get the remaining stoplight report analysis")
else:
 col1, col2, col3, col4, col5 = st.columns(5)
 col1.metric("Polarity", round(textcsm.sentiment.polarity,2), round(1-textcsm.sentiment.polarity,2))
 col2.metric("Objectivity", round(textcsm.sentiment.subjectivity,2), 1-textcsm.sentiment.subjectivity)
 col3.metric("Cost Performance", cpi, cpi-1 )
 col4.metric("Schedule Performance", spi, spi-1 )
 col5.metric("Engagement", "86%", "4%")

 col1, col2 = st.columns(2)
 with col1:
  st.video(videopmreport, format='video/mp4', start_time=0)

 #st.markdown(plcommentsummary)
 #st.write(plcsmcomment) #sentiment for each sentence
 #st.write(textcsm.noun_phrases) #extracting polarity of each sentence
 #st.write(textcsm.np_counts) #extracting polarity of each sentence
 #https://textblob.readthedocs.io/en/dev/classifiers.html#classifying-text
 #st.write("text sentiment", textcsm.sentiment_assessments)
 #st.write(Counter(tags).most_common(5))
 wordtoken = word_tokenize(textresult)
 is_noun = lambda pos: pos[:2] == 'NN'
 nouns = [word for (word, pos) in nltk.pos_tag(wordtoken) if is_noun(pos)] 
 #for word, tag in wordtoken:
 #  if tag == 'NN':
 #    nouns.append(word.lemmatize())
 # st.write(str(dict(Counter(nouns).most_common(5))))
 sentence_list = nltk.sent_tokenize(textresult)
 stopwords = nltk.corpus.stopwords.words('english')
 # st.write(sentence_list)
 word_frequencies = {}
 for word in nltk.word_tokenize(textresult):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1
 maximum_frequncy = max(word_frequencies.values())

 #for word in word_frequencies.keys():
 #   word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    # st.write(word)

 sentence_scores = {}
 for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

 summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

 summary = ' '.join(summary_sentences)

 # https://stackoverflow.com/questions/49566756/creating-wordclouds-with-altair
 # create the WordCloud object
 wordcloud = WordCloud(min_word_length =5,
                      background_color='white', stopwords=stopwords, max_words=10)

 # generate the word cloud
 stopwords = set(STOPWORDS)
 # wordcloud.generate_from_frequencies(word_frequencies)
 wordcloud.generate(text_formatted)

 #plot
 plt.imshow(wordcloud, interpolation='bilinear')
 plt.axis('off')
 plt.show()
 with col2:
  st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Management Report </p>", unsafe_allow_html=True)
  st.pyplot(plt)
  st.write(summary)
st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Deliverables</p>", unsafe_allow_html=True)
st.write(st.session_state.plscopemusthave)
#df[(df['date'] > '2013-01-01') & (df['date'] < '2013-02-01')]
#final_table_columns = ['id', 'name', 'year']
#pandas_df = pandas_df[ pandas_df.columns.intersection(final_table_columns)]
