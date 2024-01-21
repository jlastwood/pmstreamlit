#Page for nlp of the project report
from PIL import Image
import streamlit as st
from datetime import date, datetime
import hydralit_components as hc
import pandas as pd # bad janet! bad! don't import * 
from scripts.thepmutilities import reporttitle, gradiant_header
#from st_radial import st_radial
import matplotlib.pyplot as plt
from scripts.riskgenerate import calculate_risks_json
import logging

def color_survived(val):
    #RAG (dashboard)
    color = 'white'
    if val == 'G' or val == 'Green':
      color = 'green' 
    if val == 'A' or val == 'Amber':
      color = '#FFBF00' 
    if val == 'R' or val == 'Red':
      color = '#D12F2E'
    if val == 'N' or val == 'None':
      color = 'white'
    return f'background-color: {color}'
def dashboard_rag(val):
    #  value displayed based on ratio or value 
    if val >= 6:
       st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: #D12F2E; font-size: 100%;'>  R  </p>", unsafe_allow_html=True)      
    elif val >= 3:
       st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: #FFBF00; font-size: 100%;'>  A  </p>", unsafe_allow_html=True)      
    elif val >= 1.0:
       st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 100%;'>  G  </p>", unsafe_allow_html=True)      
    elif val < 0.8:
       st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: #D12F2E; font-size: 100%;'>  R  </p>", unsafe_allow_html=True)      
    else:
       st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: #FFBF00; font-size: 100%;'>  A  </p>", unsafe_allow_html=True)      
# get a list of the bullet points
def split(s):
    thislist = []
    start = 0
    for i in [1,2,3,4,5,6,7,8]:
      txt = str(i) + '.'
      fins = s.find(txt, start)
      if fins > 0:
        end = s.find(":", fins)
        if end < 0:
          end = find + 15
        getstring = s[fins:end]
        thislist.append(getstring)
        start = fins + 3
    return thislist

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

gradiant_header ('The PM Monitor Stoplight Report')

if 'thepmheader' not in st.session_state:
 st.warning("Sorry, plan is missing.  Please enter or import a plan")
 st.stop()

if 'plcsmcomment' not in st.session_state:
 st.session_state.plcsmcomment = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "collapsed"
    st.session_state.disabled = False

if "plpmreport" not in st.session_state:
  st.session_state.plpmreport = ""
  st.session_state.plpmid = ""
videopmreport=st.session_state.plpmreport
videoidreport=st.session_state.plpmid

#videoidreport="c4fEms85NQQ"
#videopmreport="https://www.youtube.com/watch?v=qWdyhFiyH0Y&t=10s"

daytoday = date.today()
cpi = round(st.session_state.thepmcpi,1)
spi = round(st.session_state.thepmspi,1)
if st.session_state.plncadence == 0:
 freqn = "1W"
else:
 freqn = str(st.session_state.plncadence) + 'W'
#series = pd.date_range(start=st.session_state.pldstartdate, end=st.session_state.pldenddate, periods=st.session_state.thepmreportsinplan, freq='B')
series = pd.date_range(start=st.session_state.pldstartdate, end=st.session_state.pldenddate, freq=freqn)
seriesdate = [datetime.strftime(d, '%Y/%m/%d') for d in series]
serieslist = pd.DataFrame(seriesdate).astype(str)
statuslist = []
#  todo figure out a way to generate dashboard
for i in range (0, len(serieslist)):
      seriesvalue = st.session_state.plmplanstatus
      y = 0
      if st.session_state.pldacceptdate.strftime('%Y/%m/%d') > seriesdate[i] > st.session_state.pldinspectdate.strftime('%Y/%m/%d'):
        seriesvalue = st.session_state.plmacceptstatus
        y = 1        
      elif st.session_state.pldinspectdate.strftime('%Y/%m/%d') > seriesdate[i] > st.session_state.pldbuilddate.strftime('%Y/%m/%d'):
          seriesvalue = st.session_state.plminspectstatus
          y =  2       
      elif st.session_state.pldbuilddate.strftime('%Y/%m/%d') > seriesdate[i] > st.session_state.plddesigndate.strftime('%Y/%m/%d'):
          seriesvalue = st.session_state.plmbuildstatus
          y =  3       
      elif st.session_state.plddesigndate.strftime('%Y/%m/%d') > seriesdate[i] > st.session_state.pldplandate.strftime('%Y/%m/%d'):
          seriesvalue = st.session_state.plmdesignstatus
          y =  4       
      if seriesdate[i] > datetime.today().strftime('%Y/%m/%d'):
        seriesvalue = 'None'
      statuslist.append(seriesvalue)
      # st.write(i, y, seriesvalue, seriesdate[i], st.session_state.plddesigndate.strftime('%Y/%m/%d'))
  #if seriesdate[i] < datetime.today().strftime('%Y/%m/%d'):
  # statuslist.append('G')
serieslist['Status'] = statuslist
bar_theme_2 = {'bgcolor': 'lightgrey','content_color': 'grey','progress_color': 'green'}

reporttitle("Stoplight Report", st.session_state['thepmheader'])

st.markdown("---")
seriestrans = serieslist.T
seriestrans = seriestrans.astype(str)
st.table(seriestrans.style.applymap(color_survived))

st.markdown("---")
cola, colb, colc, cold, cole = st.columns([1,2,1,1,4])
with cola:
  st.write("Schedule")
with colb:
  hc.progress_bar(st.session_state['thepmtimecomplete'],'Time',key='thepaschedule',sentiment='good')
with colc:
  st.write(st.session_state['thepmtimecomplete'], spi)
with cold:
  dashboard_rag(spi)
with cole:
  if spi < 1:
    notes = "<font color='grey'>:warning:" + " Behind schedule - Contingency: " + st.session_state['plptimecontingency'] + "</font>"
  else:
    notes = "<font color='grey'>" + "On or ahead of schedule" + "</font>"
  st.markdown("{}".format(notes), unsafe_allow_html=True)
cola, colb, colc, cold, cole = st.columns([1,2,1,1,4])
with cola:
  st.write("Scope")
with colb:
  scopebar =  st.session_state['thepmdelivery']
  hc.progress_bar(scopebar,'Features',key='thepascope',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.write(scopebar)
with cold:
  dashboard_rag(len(st.session_state.plscopechange)/10)
with cole:
  if len(st.session_state['plscopechange']) > 10:
    notec = "<font color='grey'>:warning: " + st.session_state['plpscopecontingency'] + "</font>"
  else:
    notec = ""
  st.markdown("{}".format(notec), unsafe_allow_html=True)
cola, colb, colc, cold, cole = st.columns([1,2,1,1,4])
with cola:
  st.write("Quality")
with colb:
  qualbar = qualratio = 0
  if int(st.session_state['plntests']) > 0:
   qualbar = int(st.session_state['plntestsfailed'] / st.session_state['plntests'] * 100)
   qualration = float(st.session_state['plntestsfailed'] / st.session_state['plntests'])
  hc.progress_bar(qualbar,'Quality',key='thepaqual',sentiment='good',override_theme=bar_theme_2)
with colc:
  st.write(qualbar, qualratio, st.session_state.plntestsfailed)
with cold:
  dashboard_rag(st.session_state.plntestsfailed)
with cole:
  if int(st.session_state['thepminspectionflag']) == 1:
    notec = "<font color='grey'>:warning: " + st.session_state['thepminspectionwarning'] + st.session_state['plpscopecontingency'] + "</font>"
  else:
    notec = ""
  st.markdown("{}".format(notec), unsafe_allow_html=True)
cola, colb, colc, cold, cole = st.columns([1,2,1,1,4])
with cola:
  st.write("Cost")
with colb:
  hc.progress_bar(st.session_state['thepmbudgetcomplete'],'Cost',key='thepmpabudget',sentiment='good')
with colc:
  st.write(st.session_state['thepmbudgetcomplete'], cpi)
with cold:
  dashboard_rag(cpi)
with cole:
  if cpi < 1:
    notes = "<font color='grey'>:warning: " + "Over Budget - Contingency:  " + st.session_state['plpbudgetcontingency'] + "</font>"
  else:
    notes = "<font color='grey'>" + "On or ahead of budget" + "</font>"
  st.markdown("{}".format(notes), unsafe_allow_html=True)
cola, colb, colc, cold = st.columns([2,2,2,2])
with cola:
  st.write("Planned Completion")
with colb:
  st.write(st.session_state['pldenddate'])
with colc:
  st.write("Planned Features")
with cold:
  st.write(st.session_state['plnscopenumber'])
with cola:
  st.write("Estimate to Complete")
with colb:
  st.write(st.session_state['thepmtimecomplete'])
#with colc:
#  st.write("Features Completed")
#with cold:
#  st.write(st.session_state['plnscopenumbersuccess'])
st.markdown("---")

st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: red; font-size: 120%;'>Management Alert</p>", unsafe_allow_html=True)

st.write("The following issues have been triggered, the risk owner should consider taking action to recover.")

phasenumber = st.session_state.thepmphase
CPI = st.session_state.thepmcpi
SPI = st.session_state.thepmspi
engagementscoreteam = st.session_state.plnactivesam
sentimentscoreteam = st.session_state.plnactiveses
retention = st.session_state.plnopenroles
scopechange = len(st.session_state.plscopechange.split("."))
if len(st.session_state.plscopechange) < 6:
   scopechange = 0
earnedvalue = st.session_state.plnactiveses
roi = st.session_state.plnactiveses
latestart = st.session_state.plnactiveses
inspectfail = st.session_state.plnactiveses

(myrisks, issues, risks, totalrisks, risksummary)  = calculate_risks_json(phasenumber, SPI, CPI, engagementscoreteam, sentimentscoreteam, retention, scopechange, earnedvalue, roi, latestart, inspectfail)

cols = ['risktype', 'riskowner', 'riskscore', 'riskdescription']
myissues = (myrisks[myrisks['riskselect'] == 'I'])
subissues = myissues[cols]

st.table(subissues)

st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: red; font-size: 120%;'>Project Manager Report</p>", unsafe_allow_html=True)
if len(videopmreport) < 10:
  st.warning("PM report is missing no stoplight report engagement analysis")
else:
 textcsm = st.session_state.textcsm
 col1, col2, col3, col4, col5 = st.columns(5)
 col1.metric("Polarity", round(textcsm.sentiment.polarity,2), round(1-textcsm.sentiment.polarity,2))
 col2.metric("Objectivity", round(textcsm.sentiment.subjectivity,2), 1-textcsm.sentiment.subjectivity)
 col3.metric("Cost Performance", cpi, cpi-1 )
 col4.metric("Schedule Performance", spi, spi-1 )
 col5.metric("Engagement", "86%", "4%")

 col1, col2 = st.columns(2)
 with col1:
  st.video(videopmreport, format='video/mp4', start_time=0)

 #plot
 plt.imshow(st.session_state.pmpvidwordcloud, interpolation='bilinear')
 plt.axis('off')
 plt.show()
 with col2:
  st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Management Report </p>", unsafe_allow_html=True)
  st.pyplot(plt)
  st.write(st.session_state.pmpvidsummary)

st.markdown("<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>Deliverables</p>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
 st.write("Requirements")
 st.write('.  \n'.join(split(st.session_state.plscopemusthave)))
 st.write("Nice to Have")
 st.write('.  \n'.join(split(st.session_state.plscopenicetohave)))
with col2:
 st.write("Environment and Non-Functional")
 st.write('.  \n'.join(st.session_state.plmlistscopelist))
 st.write('.  \n'.join(st.session_state.plmlistscopeoption))
 st.write("Quality Reports")
 st.write('.  \n'.join(st.session_state.plmlistqualitytypes))
#df[(df['date'] > '2013-01-01') & (df['date'] < '2013-02-01')]
#final_table_columns = ['id', 'name', 'year']
#pandas_df = pandas_df[ pandas_df.columns.intersection(final_table_columns)]
