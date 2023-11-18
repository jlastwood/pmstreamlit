"""Page for viewing the awesome Project slackmessages"""
from PIL import Image
import streamlit as st
import pandas as pd
#from slack_message import slack_messages_pm
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from scripts.thepmutilities import reporttitle, gradiant_header

st.session_state.update(st.session_state)

# https://ruarfff.com/slack-sentiment/


im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Communications Analysis",
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

gradiant_header ('The PM Monitor Communication Analysis')

if 'thepmheader' not in st.session_state:
     st.error('Please create a plan')
     st.stop()
reporttitle("Team Communication Analysis", st.session_state['thepmheader'])

st.write("Using your team communication channel messages, analysis of the sentiment, word density to see what they are talking about, and engagement score") 

uploaded_file = st.file_uploader("Message history", type=['csv'])

if uploaded_file is not None:
    messages=pd.read_csv(uploaded_file, quotechar='"', delimiter=',', skipinitialspace=True)
    #Tasks['Start'] = Tasks['Start'].astype('datetime64')
    #Tasks['Finish'] = Tasks['Finish'].astype('datetime64')
    #Tasks['duration'] = Tasks['duration'].astype('int')
    #Tasks['duration'] = Tasks['duration'].fillna(0)
    #st.write(messages)
    st.success("success")
    allmessages = ". ".join(map(str, messages['text']))
    #st.write(allmessages)
    sents = sent_tokenize(allmessages) #tokenizing the text data into a list of sentences
    entireText = TextBlob(allmessages) #storing the entire text in one string
    sentScores = [] #storing sentences in a list to plot
    for sent in sents:
         text = TextBlob(sent) #sentiment for each sentence
         score = text.sentiment[0] #extracting polarity of each sentence
         sentScores.append(score) 

    #Plotting sentiment scores per sentencein line graph
    st.write("output engagement score, sentiment, top 5 words, top 3 people")
    st.line_chart(sentScores) #using line_chart st call to plot polarity for each 
    #(commentdata, clientmessage) = slack_messages_pm(slacktoken, slackchannel)
    sentimentTotal = entireText.sentiment
    st.write("The sentiment of the overall text below.")
    st.write(sentimentTotal)
