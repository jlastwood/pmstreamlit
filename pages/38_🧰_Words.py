"""Page for viewing the awesome Project slackmessages"""
from PIL import Image
import streamlit as st
import pandas as pd
#from slack_message import slack_messages_pm
from textblob import TextBlob
import nltk
import heapq
from nltk.tokenize import sent_tokenize
from scripts.thepmutilities import reporttitle, gradiant_header
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from wordcloud import WordCloud, STOPWORDS
from deepmultilingualpunctuation import PunctuationModel
import matplotlib.pyplot as plt

st.session_state.update(st.session_state)

# https://ruarfff.com/slack-sentiment/


im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Communications Analysis",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

gradiant_header ('The PM Monitor Communication Analysis')

if 'thepmheader' not in st.session_state:
     st.error('Please create a plan')
     st.stop()
reporttitle("The PM Monitor Word Analysis", st.session_state['thepmheader'])

st.write("Analysis of the written team channels, or spoken word provides insight to engagement, sentiment and context.  Using your team communication channel messages, and your video report, analysis of the sentiment, word density to see what they are talking about, and get engagement score. There are two input files, a message channel logfile and a video.    The format of the input is DateTime, Channel, User, and Message. ") 

uploaded_file = st.file_uploader("Message history", type=['csv'])
st.write("---")
st.write("The project manager supplies a video report with the reports")
col3, col4 = st.columns(2) 
with col3:
       st.text_input ("PM report (youtube)", key='plpmreport')
with col4: 
       videoidreport = st.text_input ("PM report ID",  key='plpmid')

if uploaded_file is not None:
    messages=pd.read_csv(uploaded_file, quotechar='"',  delimiter=',', skipinitialspace=True)
    messages['Date'] = pd.to_datetime(messages.DateTime, format='%Y-%m-%d')
    messages['Week'] = messages['Date'].dt.strftime('%y%U')
    #Tasks['DateTime'] = Tasks['Start'].astype('datetime64')
    #Tasks['Finish'] = Tasks['Finish'].astype('datetime64')
    #Tasks['duration'] = Tasks['duration'].astype('int')
    #Tasks['duration'] = Tasks['duration'].fillna(0)
    st.dataframe(messages)
    st.success("success")
    allmessages = ". ".join(map(str, messages['text']))
    #st.write(allmessages)

    output = messages.groupby('User')['DateTime'].describe()
    st.write(output)
    output2 = messages.groupby('Week')['User'].describe()
    st.write(output2)

    sents = sent_tokenize(allmessages) #tokenizing the text data into a list of sentences
    entireText = TextBlob(allmessages) #storing the entire text in one string
    sentScores = [] #storing sentences in a list to plot
    for sent in sents:
         text = TextBlob(sent) #sentiment for each sentence
         score = text.sentiment[0] #extracting polarity of each sentence
         sentScores.append(score) 
    st.write(allmessages)
    #Plotting sentiment scores per sentencein line graph
    st.write("output engagement score, sentiment, top 5 words, top 3 people")
    st.line_chart(sentScores) #using line_chart st call to plot polarity for each 
    #(commentdata, clientmessage) = slack_messages_pm(slacktoken, slackchannel)
    sentimentTotal = entireText.sentiment
    st.write("The sentiment of the overall text below.")
    st.write(sentimentTotal)
    #wordtoken = word_tokenize(sents)
    stopwords = nltk.corpus.stopwords.words('english')
    wordcloud = WordCloud().generate(allmessages)
    wordcloud = WordCloud(min_word_length = 5,
                      background_color='white', stopwords=stopwords, max_words=10)

    # generate the word cloud
 # wordcloud.generate_from_frequencies(word_frequencies)
    plotwc = wordcloud.generate(allmessages)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

#  processing of the video

if len(videoidreport) > 10: 
 transcript=YouTubeTranscriptApi.get_transcript(videoidreport)
 formatter = TextFormatter()
 text_formatted = formatter.format_transcript(transcript)
 model = PunctuationModel(model="oliverguhr/fullstop-punctuation-multilingual-sonar-base")
 textresult = model.restore_punctuation(text_formatted)
 st.session_state['textcsm'] = TextBlob(textresult) #sentiment for each sentence

 wordtoken = word_tokenize(textresult)
 is_noun = lambda pos: pos[:2] == 'NN'
 nouns = [word for (word, pos) in nltk.pos_tag(wordtoken) if is_noun(pos)]
 #for word, tag in wordtoken:
 #  if tag == 'NN':
 #    nouns.append(word.lemmatize())
 # st.write(str(dict(Counter(nouns).most_common(5))))
 sentence_list = nltk.sent_tokenize(textresult)
 stopwords = nltk.corpus.stopwords.words('english')
 newStopWords = ['um','ok']
 for i in newStopWords:
    stopwords.append(i)
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
 summary = summary.replace('um', '')

 # https://stackoverflow.com/questions/49566756/creating-wordclouds-with-altair
 # create the WordCloud object
 wordcloud = WordCloud(min_word_length = 5,
                      background_color='white', stopwords=stopwords, max_words=10)

 # generate the word cloud
 stopwords = set(STOPWORDS)
 # wordcloud.generate_from_frequencies(word_frequencies)
 wordcloud.generate(text_formatted)
 st.text_area("Write a report", key='pmvidmysummary')
 st.code(summary)
 if len(st.session_state.pmvidmysummary) > 20:
   st.session_state['pmpvidsummary'] = st.session_state.pmvidmysummary
 else:
   st.session_state['pmpvidsummary'] = summary
 st.session_state['pmpvidwordcloud'] = wordcloud
