"""Page for viewing the awesome Project slackmessages"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
from risklist import getrisks
import pandas as pd
import altair as alt
from slack_message import slack_messages_pm
from textblob import TextBlob
from nltk.tokenize import sent_tokenize

@st.cache
def get_plan_markdown() -> str:
    """Enter the plan and return CPI and SPI
    """
    url = pathlib.Path(__file__).parent.parent.parent / "AWESOME-STREAMLIT.md"
    with open(url, mode="r") as file:
        readme_md_contents = "".join(file.readlines())
    return readme_md_contents.split("\n", 3)[-1]


def write():
    """Method used to write the page in the app.py file"""
    ast.shared.components.title_awesome("Messages")
    # with st.spinner("Loading  ..."):
    if 'plnumber' not in st.session_state:
     #st.session_state.plnumber = ""
     st.error('Please create a plan')
     return()
    st.write("Project Number: ", st.session_state.plnumber)
    with st.form("my_messages"):
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Project Information</h4>", unsafe_allow_html=True)

     st.header("Slack Connection Details")
     slacktoken  = st.text_input ("Token", help="A slack token", key="slacktoken")
     slackchannel  = st.text_input ("Channel", help="A slack token", key="slackchannel")
     slackdata   = st.text_input ("Enter data", help="A slack string", key="slackdata")
     submit = st.form_submit_button("Submit")
     if submit:
        st.success("success")
        sents = sent_tokenize(slackdata) #tokenizing the text data into a list of sentences
        entireText = TextBlob(slackdata) #storing the entire text in one string
        sentScores = [] #storing sentences in a list to plot
        for sent in sents:
         text = TextBlob(sent) #sentiment for each sentence
         score = text.sentiment[0] #extracting polarity of each sentence
         sentScores.append(score) 

    #Plotting sentiment scores per sentencein line graph
        st.line_chart(sentScores) #using line_chart st call to plot polarity for each 
        (commentdata, clientmessage) = slack_messages_pm(slacktoken, slackchannel)
        st.write(commentdata)
        sentimentTotal = entireText.sentiment
        st.write("The sentiment of the overall text below.")
        st.write(sentimentTotal)
