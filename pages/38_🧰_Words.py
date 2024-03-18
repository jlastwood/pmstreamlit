"""Page for viewing the awesome Project slackmessages"""
from PIL import Image
import streamlit as st
import re
import pandas as pd
from textblob import TextBlob
from scipy import stats
import altair as alt
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
#  run this "/Applications/Python 3.8/Install Certificates.command"
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

st.write("Analysis of the written team channels, or spoken word provides insight to engagement, sentiment and context.  Using your team communication channel messages, and your video report, analysis of the sentiment, word density to see what they are talking about, and get engagement score. There are two input files, a message channel logfile and a video.    The format of the input is DateTime, User, and text ") 

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
    #messages['Date'] = pd.to_datetime(messages.DateTime, format='%Y-%m-%d')
    messages['Date'] = pd.to_datetime(messages.DateTime, format='mixed')
    messages['Week'] = messages['Date'].dt.strftime('%y%U')
    #messages['mentions'] = re.findall("(^|[^@\w])@(\w{1,15})", messages['text'])
    #messages['text'] = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", messages['text'])
    #st.dataframe(messages)
    st.success("success")

    allmessages = ". ".join(map(str, messages['text']))
    # get mentions from text
    # text = '@username1: some tweet here, http://www.url.com, aaaaa @username2'
    # processed_text = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", allmessages)
    # processed_text = " ".join(processed_text.split())
    # get emotions from text

    st.write(allmessages)

    output = messages.groupby('User')['Week'].describe()
    #st.write(output)
    #st.line_chart(output, x='top', y='count') #using line_chart st call to plot polarity for each 
    output2 = messages.groupby('Week')['User'].describe()
    output2['week'] = output2.index
    output2['week'] = output2['week'].astype('int')
    output2['count'] = output2['count'].astype('int')
    #st.write(output2)
    slope, intercept, r_value, p_value, std_err = stats.linregress(output2['count'], output2['week'])
    if slope < .9:
       st.write(slope, std_err, " is negative indicating that engagement is declining " )
    else: 
       st.write(slope, std_err, " is positive indicating that engagement is increasing " )
    st.bar_chart(output2, x='top') #using line_chart st call to plot polarity for each 

    chart = alt.Chart(output2).mark_line().encode(
        x='week:O',
        y='median(count)',
        color='top'
    )
    st.altair_chart(chart, theme="streamlit", use_container_width=True)

    sents = sent_tokenize(allmessages) #tokenizing the text data into a list of sentences
    entireText = TextBlob(allmessages) #storing the entire text in one string
    sentScores = [] #storing sentences in a list to plot
    for sent in sents:
         text = TextBlob(sent) #sentiment for each sentence
         score = text.sentiment[0] #extracting polarity of each sentence
         sentScores.append(score) 
    # st.write(allmessages)
    #Plotting sentiment scores per sentencein line graph
    st.write("Sentiment and Topics")
    st.line_chart(sentScores) #using line_chart st call to plot polarity for each 
    #(commentdata, clientmessage) = slack_messages_pm(slacktoken, slackchannel)
    sentimentTotal = entireText.sentiment
    st.write("The sentiment of the overall text shown in the graph above.  Graph below 0 is negative sentiment and above the line is positive. ")
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

st.write("##")
successmsg = f'The PM Monitor project charter presented by {st.session_state.plpmname} on {st.session_state.pldcharterdate}.  Thank you for using The PM Monitor https://thepmmonitor.streamlit.app '
st.success(successmsg)
