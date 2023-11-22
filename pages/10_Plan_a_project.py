import streamlit as st
from PIL import Image
from datetime import timedelta, date, datetime
import pandas as pd
from scripts.thepmutilities import evreport, plancomment, get_grade, gradiant_header
import altair as alt
from st_aggrid import AgGrid
from hugchat import hugchat
from hugchat.login import Login

st.session_state.update(st.session_state)


# Log in to huggingface and grant authorization to huggingchat
# Save cookies to the local directory
@st.cache_resource
def signonhugchat():
  hf_email = st.secrets['EMAIL']
  hf_pass = st.secrets['PASS']
  sign = Login(hf_email, hf_pass)
  cookies = sign.login()
  cookie_path_dir = "./cookies_snapshot"
  sign.saveCookiesToDir(cookie_path_dir)
  chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
  return chatbot

#input_container = st.container()
#colored_header(label='', description='', color_name='blue-30')
#response_container = st.container()

# Load cookies when you restart your program:
# sign = login(email, None)
# cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.

#def generate_response(prompt):
#    chatbot = hugchat.ChatBot()
#    response = chatbot.chat(prompt)
#    return response

# Create a ChatBot
# def askme(prompt_input):
    #message = chatbot.query(prompt_input, web_search=True)
    #id = chatbot.new_conversation()
#     return ("none")
#    chatbot.change_conversation(id)
#    message = chatbot.query(prompt_input)
#    info = chatbot.get_conversation_info()
#    st.write(info.id, info.title, info.model, info.system_prompt)
    #st.write(info.id, info.title, info.model, info.system_prompt, info.history)
#    st.write("inaskme")
#    st.write(prompt_input)
    #message = {"role": "assistant", "content": chatbot.query(prompt_input)}
    # st.write(message)
#    st.write(message.text)
    #placeholder.text(message.text)
#    return message.text
    # return chatbot.chat(prompt_input)

def setvalue(var):
    if var.startswith('pllist'):
        if var in st.session_state:
          #st.write("insetvalue", var, st.session_state[var])
          if st.session_state[var] == "":
           return 0
          else:
           return int(st.session_state[var])
        else:
         return 0
    if var.startswith('pld'):
       return st.session_state[var] if var in st.session_state else date.today()
    else:
       if var.startswith('pln'):
          return int(st.session_state[var]) if var in st.session_state else 0
       else:
          return st.session_state[var] if var in st.session_state else "None"

# setup the questions for ask me

#def clear_form():
#  for key in st.session_state.keys():
#    del st.session_state[key]
# @st.cache

im = Image.open("assets/images/BlueZoneIT.ico")

st.set_page_config(
      page_title="The PM Monitor Plan",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

chatbot = signonhugchat()

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

#  get the theme colors
color1t = st._config.get_option('theme.primaryColor')
color1b = st._config.get_option('theme.secondaryBackgroundColor')
color1c = st._config.get_option('theme.backgroundColor')
color1d = st._config.get_option('theme.textColor')

theme_scope = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-check-circle'}
font_fmt = {'font-class':'h4','font-size':'50%'}
mySep = ","

gradiant_header ('The PM Monitor Project Planning Form') 

tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["Start", "Info", "Scope", "Cost", "Schedule", "Roster", "Quality", "Constraints", "ROI", "Chat", "Risk"])
#with st.form(key="pmmonitorplan", clear_on_submit=False):

     ##  Introduction to Planning

with tab0:
      st.subheader("How to Create a Plan")
      st.write("Meet with stakeholders, gather information, identify and document the goal, deliverables, budget and schedule.  Identify resources and constraints. Create an activity list and validate the resources and schedule.   Review the risks and make contingency plans. ")
      st.write("With your plan in Plan phase, Move one tab at a time, fill in the information in the form. Using Askme AI assitance for the narrative text. Fill in all information.  Print the charter and review with stakeholders.  Print the Canvas report and share with the team.  ")

      st.subheader("How to Monitor and Report")

      st.write("Restore your saved plan from backup.  With the project finished tle planning phase, the planning fields will be read only.  Moving through all tabs, update cost information, calculate estimate completion, update engagement and sentiment scores.  Were there scope changes this period?  In schedule, note if milestone delivery dates are changing.  Has the team changed?  What is the active member and engagement score for the period? Was there a quality report.  Create your brief video/audio report and save.  Review the results using the Stoplight report.  ")
      st.subheader("Steps and Pipeline")
      st.write("""
This application provides

- Form to input a charter and plan
- Project reports to share 
- Earned value analysis and reporting of CPI and SPI and ROI
- Analysis of project risks based on the project characteristics
- Sentiment analysis of team and stakeholder communications
- Probability of identified risks based on monitored threasholds
- Engagement analysis based on team and stakeholder communications
- Wordcloud analysis reporting to assess what are the topics of the week
- Analysis of WBS to report most important information

Pipeline

- enter your plan, objectives and charter
- review and save a copy of you plan
- enter your weekly cadence reporting updates to spend and progress
- analysis of your communication channels
- analysis of WBS and team tasks (if you are doing bottom up planning)
- view risks, controls and monitors
- create a project management summary 
- Output charter, canvas and stoplight reports
""")

     ##  The basic intro information 
with tab1:
      st.subheader("Project Information")
      st.write("A project is finite, has a start and and end timeframe and is unique. A project is undertaken to reach a goal, implement change, deliver a new product, service or process.  The Project Plan outlines the timeline and the benefits, scope and contingency plans.  The plan provides the necessary information for the project manager and The PM Monitor to report on the progress of the project, manage risks and identify issues.")
      phaselist = ("None", "Plan", "Design", "Build", "Inspect", "Accept", "Close")
      phaseoptions = list(range(len(phaselist)))
      st.session_state['thepmphasecomplete'] = st.selectbox('Current Phase (planning or monitoring?)', phaseoptions, format_func=lambda x: phaselist[x], key='plnlistphasecomplete', help="The phase of the project will determine which risks are higher or may be closed.  In the early phases of the project you have higher technology and cost risks and in later phases you can have engagement and resource risks. A project has 6 phases, 0 Initiation, 1 plan, 3 design,  4 build, 5 inspect, accept and  6 close")
      disableplan = False
      if st.session_state.thepmphasecomplete > 1:
        disableplan = True
      col4, col5 = st.columns(2)
      with col4:
       st.text_input ("Project Name", help="A short project name, use key words to describe the project. ", max_chars=50, key='plpname', value=setvalue('plpname'), disabled=disableplan)
      with col5:
       st.text_input ("Project ID", max_chars=10, value=setvalue('plpnumber'), help="A unique id to identify this project", key='plpnumber', disabled=disableplan)
      col4, col5 = st.columns(2)
      with col4:
       st.text_input ("Project Manager Identification", max_chars=30, value=setvalue('plpmname'), key='plpmname', disabled=disableplan)
      with col5:
       st.text_input ("Product Owner or Sponsor Identification", max_chars=30, value=setvalue('plspname'), key='plspname', disabled=disableplan)

      col5, col6, col7, col8 = st.columns(4)
      with col5:
       st.date_input ("Report Date", setvalue('pldcharterdate'), key='pldcharterdate', help="Enter the date that this report is updated.")
      with col6:
       st.slider('Cadence', min_value=0, max_value=12, value=setvalue('plncadence'), help="Cadence is the frequency that the project replans and reports on progress.  In a maintenance project you should plan and report quarterly.  In active development projects when investment is higher, you should be planning and reporting weekly", key='plncadence', disabled=disableplan)
      with col7:
       st.session_state['thepmphase'] = st.selectbox('Project Phase Started', phaseoptions, format_func=lambda x: phaselist[x], key='plnlistphase', help="Indicate if you have advanced and are in a later phase")
      classchoice = pd.DataFrame({'Item': ['None', 'Software Build', 'Software Design', 'Brand Marketing', 'Process Automation', 'Scheduled Maintenance', 'Content Migration', 'Decommission', 'Upgrade', 'Training or Documentation'], 'Value': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}) 
      classlist = ('None', 'Software Build', 'Software Design', 'Brand Marketing', 'Process Automation', 'Scheduled Maintenance', 'Content Migration', 'Decommission', 'Upgrade', 'Training or Documentation')
      with col8:
       classoptions = list(range(len(classlist)))
       selected_class = st.selectbox("Project Classification", classoptions, format_func=lambda x: classlist[x], help="The type of project will be used to determine risks, a physical build can be impacted by weather.  Changes to procedures or pipelines require more focus on communication activities", key='pllisttype' )


      cb1 = st.checkbox ("Askme for a purpose of this project", key='cb1', disabled=disableplan)
      st.text_area ("Purpose or Goal?", value=setvalue('plspurpose'), key='plspurpose', disabled=disableplan)
      if cb1 and len(st.session_state.plspurpose) < 10:
         conversation_list = chatbot.get_conversation_list()
         #st.write(conversation_list)
         # Get the available models (not hardcore)
         models = chatbot.get_available_llm_models()
# Switch model to the given index
         #st.write(models)
         #chatbot.switch_llm(3) # Switch to the first model
         # Create a new conversation
         id = chatbot.new_conversation()
         chatbot.change_conversation(id)
         #chatbot.delete_all_conversations()
         query = "What is the purpose of a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb1, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query, web_search=True) 
         st.code(message)
      del st.session_state['cb1']
      cb2 = st.checkbox ("Askme for three benefits.", disabled=disableplan)
      st.text_area ("Benefits", value=setvalue('plsbenefits'), key='plsbenefits', disabled=disableplan)
      if cb2 and len(st.session_state.plsbenefits) < 10:
         query = "What are three benefits of " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query) 
         st.code(message)
      cb3 = st.checkbox("Askme for Benchmarks", disabled=disableplan)
      st.text_area ("Benchmarks", value=setvalue('plsbenchmarks'), key='plsbenchmarks', disabled=disableplan)
      if cb3 and len(st.session_state.plsbenchmarks) < 10:
         query = "Are there comparable benchmarks or services for a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query) 
         st.code(message)
     # set some dates
      week  = timedelta(days = 7)
      daytoday = date.today()
     
      col1, col2, col3 = st.columns(3)
      with col1:
       st.date_input ("Start Date", setvalue('pldstartdate'), key='pldstartdate', help="Enter the project start date", disabled=disableplan)
      with col2:
       st.date_input ("End Date", setvalue('pldenddate'), key='pldenddate', help="Enter the project end date", disabled=disableplan)

     # how much time to end of plan
      daystoend = (st.session_state['pldenddate']-st.session_state['pldstartdate']).days
      daystoday = (daytoday-st.session_state['pldstartdate']).days
      weeksinplan = int(daystoend/7)
      st.session_state['thepmtimecomplete'] = 0
      if daystoend > 0:
        st.session_state['thepmtimecomplete'] = int(daystoday / daystoend * 100)

     ##  output information and create header block
      st.session_state['thepmplannote'] = plancomment(st.session_state['pldstartdate'], st.session_state['pldenddate'], daystoday, daystoend, st.session_state['thepmtimecomplete'], 3, st.session_state['plpnumber'], st.session_state['plpname'], st.session_state['plsbenefits'], st.session_state['plncadence'], phaselist[st.session_state['thepmphase']], st.session_state['plspname'], classlist[selected_class])
 
      st.success(st.session_state['thepmplannote'])
      st.session_state['thepmphasename'] = phaselist[st.session_state['thepmphase']]

      ndays = st.session_state['plncadence']*7
      st.session_state['thepmheader'] = pd.DataFrame({
       "Project": [st.session_state.plpname, st.session_state.plpmname],
       "Sponsor": [st.session_state.plpnumber, st.session_state.plspname],
       "Phase": [phaselist[st.session_state.thepmphase], st.session_state.pldcharterdate]
        })

     #  Scope section 
with tab2:
      st.subheader("Scope")
      st.write("The scope information outlines the features that the product should have. Scope also clarifies what is not planned and what may be negotiable.  When monitoring the project, identify any scope changes.  You can also expand on out of scope items that were not clear.   ")

      scopechange = st.text_area ("What scope has been added or removed after the start of this project? ", value=setvalue('plscopechange'), key='plscopechange')
      col4, col5 = st.columns(2)
      with col4:
       st.slider('Features Planned', min_value=0, max_value=20, value=setvalue('plnfeaturesplanned'), help="How many features are planned for this product. One feature is a collection or group of user stories.  Epics are high level initiatives and contain many features", key='plnfeaturesplanned', disabled=disableplan)
      with col5:
       st.session_state['plnfeaturescompleted'] = st.slider('Features Completed', min_value=0, max_value=20, value=setvalue('plnfeaturescompleted'), help="How many features are completed at this report?")
      st.text_area ("What is out of scope?", value=setvalue('plscopeoutofscope'), key='plscopeoutofscope')

      st.write("The following is a narrative explaining the scope and goal of this project.   If there is flexibility then outline the must have and nice to have features.")

      col4, col5 = st.columns(2)
      cb4 = st.checkbox("Askme for scope ")
      st.text_area ("What are the must have Features?", value=setvalue('plscopemusthave'), key='plscopemusthave' , disabled=disableplan)
      if cb4 and len(st.session_state.plscopemusthave) < 10:
         query = "What are three must have features of a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)

      cb5 = st.checkbox("Askme for scope options")
      st.text_area ("What are some features that are negotiable or nice to have?", value=setvalue('plscopenicetohave'), key='plscopenicetohave', disabled=disableplan)
      if cb5 and len(st.session_state.plsscopenicetohave) < 10:
         query = "What are three nice to have features in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)

      col4, col5 = st.columns(2)
      with col5:
       st.multiselect( label='Select non functional attributes', help='Prese enter to add', options=['Security', 'Availability', 'Usability', 'Maintainability','Documentation', 'Accessibility', 'Compliance', 'Robustness', 'Reliablity', 'Performance', 'Localization', 'Compatiblity', 'Portability', 'Scalability', 'None'], default=setvalue('plmlistscopelist'), key='plmlistscopelist', max_selections = 4, disabled=disableplan)
      with col4:
        st.multiselect( label='Select technical architecture attributes and resources', options=['CMS', 'Web Framework', 'SEO', 'Search', 'Cloud Hosting', 'OnPrem Hosting', 'Automation',  'ERP', 'CDN', 'CI/CD', 'Custom Theme', 'No/Low Code', 'Native Mobile App', 'Process Model', 'Database', 'Testing', 'Decommission', 'Data Migration', 'SAAS', 'None'], default=setvalue('plmlistscopeoption'), key='plmlistscopeoption', max_selections = 4, disabled=disableplan)
      if len(scopechange) > 5:
         scopechange = f'There are scope changes. {scopechange}'
      st.session_state['thepmplanscope'] = f'Options:  \n\n  {st.session_state.plscopenicetohave}  \n\n Required:  \n  {st.session_state.plscopemusthave}  \n\n  Out of Scope:  {st.session_state.plscopeoutofscope} {scopechange}'
      st.success(st.session_state['thepmplanscope'])


##  Schedule
      milestonestatus = {0: "Not started", 1: "In Progress", 2: "On Hold", 3: "Complete"}
with tab4:
      st.subheader("Schedule")
      st.write("The plan is managed and controlled by the defined milestones.  Your project should have no less than 6 milestones however you can define more. Milestones are point in time events that are used to verify if the project is on track.  Completing a phase in the plan is a milestone.  Features can be decomposed into unique stories, stories are SMART,  Specific, Measurable, Achievable, Realistic and completion of a feature can be tracked as a milestone. ")

      st.date_input ("Plan Date", setvalue('pldplandate'), key='pldplandate', help="Enter the target project plan date", disabled=disableplan)
      st.date_input ("Design Date", setvalue('plddesigndate'), key='plddesigndate', help="Enter the target project plan date", disabled=disableplan)
      st.date_input ("Build Date", setvalue('pldbuilddate'), key='pldbuilddate', help="Enter the target project plan date", disabled=disableplan)
      st.date_input ("Inspect Date", setvalue('pldinspectdateplan'), key='pldinspectdateplan', help="Enter the target project plan date", disabled=disableplan)
      st.date_input ("Accept Date", setvalue('pldacceptdate'), key='pldacceptdate', help="Enter the target project plan date", disabled=disableplan)
      sdate = st.session_state['pldstartdate']
      #[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
      reportsinplan = 1
      if st.session_state['plncadence'] > 0:
       reportsinplan = int(weeksinplan/st.session_state['plncadence'])
      #  we must report at least close of each phase
      if reportsinplan < 6:
       reportsinplan = 6 
      st.session_state['thepmreportsinplan'] = reportsinplan

      st.write("Status Reports", reportsinplan)
      series = pd.DataFrame(pd.date_range(start=st.session_state.pldstartdate, end=st.session_state.pldenddate, periods=st.session_state.thepmreportsinplan, normalize=True))
      seriesb = pd.DataFrame(pd.date_range(start=st.session_state.pldstartdate, end=st.session_state.pldenddate, periods=st.session_state.thepmreportsinplan))
      jseries = pd.merge(series, seriesb, left_index=True, right_index=True)
      jseries = jseries.rename(columns={"0_x": "reportdate", "0_y": "plandate"})
      jseries['Milestone'] = "Baseline"
     
      #  append not supported
      #  collect in list and then convert to df  https://stackoverflow.com/questions/75956209/dataframe-object-has-no-attribute-append

      series = pd.DataFrame(pd.date_range(start=st.session_state.pldinspectdateplan, end=st.session_state.pldacceptdate, periods=2))
      #series = pd.DataFrame(pd.date_range(start=(st.session_state.pldacceptdate - timedelta(days=7)), end=st.session_state.pldacceptdate, periods=2))
      series.rename(columns={series.columns[0]: "reportdate"}, inplace=True)
      series['Milestone'] = "5-Accept"
      series['plandate'] = datetime.combine(st.session_state.pldacceptdate, datetime.min.time())
      kseries = pd.concat([jseries, series])

      series = pd.DataFrame(pd.date_range(start=st.session_state.pldbuilddate, end=st.session_state.pldinspectdateplan, periods=2))
      series.rename(columns={series.columns[0]: "reportdate"}, inplace=True)
      series['Milestone'] = "4-Inspect"
      series['plandate'] = datetime.combine(st.session_state.pldinspectdateplan, datetime.min.time())
      lseries = pd.concat([kseries, series])

      series = pd.DataFrame(pd.date_range(start=st.session_state.plddesigndate, end=st.session_state.pldbuilddate, periods=2))
      series.rename(columns={series.columns[0]: "reportdate"}, inplace=True)
      series['Milestone'] = "3-Build"
      series['plandate'] = datetime.combine(st.session_state.pldbuilddate, datetime.min.time())
      mseries = pd.concat([lseries, series])

      series = pd.DataFrame(pd.date_range(start=st.session_state.pldplandate, end=st.session_state.plddesigndate, periods=2))
      series.rename(columns={series.columns[0]: "reportdate"}, inplace=True)
      series['Milestone'] = "2-Design"
      series['plandate'] = datetime.combine(st.session_state.plddesigndate, datetime.min.time())
      nseries = pd.concat([mseries, series])

      series = pd.DataFrame(pd.date_range(start=(st.session_state.pldplandate - timedelta(days=7)), end=st.session_state.pldplandate, periods=2))
      series.rename(columns={series.columns[0]: "reportdate"}, inplace=True)
      series['Milestone'] = "1-Plan"
      series['plandate'] = datetime.combine(st.session_state.pldplandate, datetime.min.time())
      pseries = pd.concat([nseries, series])

      # st.write(oseries)

      series = pd.DataFrame(pd.date_range(start=(st.session_state.pldplandate), end=st.session_state.pldenddate, periods=2))

      series.rename(columns={series.columns[0]: "plandate"}, inplace=True)
      series['reportdate'] = datetime.now()
      series['Milestone'] = "Today"
      oseries = pd.concat([pseries, series])

      #dfm = dfm.rename(columns={0: "Milestone", 1: "reportdate", 2: "plandate", 3: "Status"})
      #dfresponse = AgGrid(dfm, height=200, theme='streamlit', editable=True, fit_columns_on_grid_load=True)

      chart = alt.Chart(oseries).mark_line(point = True).encode(
          alt.X('yearmonthdate(reportdate):O', title='Report Date'),
          alt.Y('yearmonthdate(plandate):O', title='Plan Date', scale=alt.Scale(reverse=True)),
          color="Milestone", text="Milestone")
      st.altair_chart(chart, use_container_width=True)
      st.session_state['thepmmilestones'] = oseries

      # st.write(oseries)

with tab5:
      st.subheader("Roster")
      st.write("Projects are executed and implemented by people, the team, the stakeholders and are implemented to provide benefit to users or customers.  The communication plan outlines the needs of the stakeholders, team and users. The complexity maintaining good communication and establishing trust between the team and the stakeholders is a factor of the size of the team, and how long they have been working together.  Trust is earned, not given, and as trust increases, performance will improve and quality will follow.  Typically engagement and team sentiment is high at the beginning of the project and decreases over time, and engagement of the stakeholders follows the opposite pattern  ")
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.slider ("Number of Stakeholders", value=setvalue('plnstakeholder'), format="%i", min_value=0, max_value=10, step=1, key='plnstakeholder', disabled=disableplan )
      with col2:
       st.slider ("Number of Core Team Members", value=setvalue('plnteam'), format="%i", min_value=0, max_value=15, step=1, key='plnteam', disabled=disableplan)
      with col3:
       st.slider ("Number of Users", value=setvalue('plnusers'), format="%i", min_value=0, max_value=100000, step=10000, key='plnusers', disabled=disableplan)
      with col4:
       st.slider ("Number of Actors", value=setvalue('plnactors'), format="%i", min_value=0, max_value=10, step=1, key='plnactors', disabled=disableplan)
      st.write("---")
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.slider ("Weeks with Full Team", value=setvalue('plnteamweeks'), format="%i", min_value=0, max_value=12, step=1, key='plnteamweeks' )
      with col2:
       st.slider ("Number of Open Roles", value=setvalue('plnopenroles'), format="%i", min_value=0, max_value=15, step=1, key='plnopenroles')
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       # SAM = (Active Channel Members/ Total Channel Members)
       st.slider ("Active Team Score (Engagement)", value=setvalue('plnactivesam'), format="%i", min_value=0, max_value=100, step=5, key='plnactivesam' )
      with col2:
        #SES = ((Unique Commenters + Unique Reactors) / 2) / (Active Channel Members)
        #SES Simplified = (Average Active Members) / (Active Channel Members)
       st.slider ("Active Team Score (Sentiment)", value=setvalue('plnactiveses'), format="%i", min_value=0, max_value=100, step=5, key='plnactiveses' )
      with col3:
       st.slider ("Active User Score (Engagement)", value=setvalue('plnactivesamuser'), format="%i", min_value=0, max_value=100, step=5, key='plnactivesamuser' )
      with col4:
       st.slider ("Active User Score (Sentiment)", value=setvalue('plnactivesesuser'), format="%i", min_value=0, max_value=100, step=5, key='plnactivesesuser' )
      st.write("Enter the location of the team WBS and their communication channel")
      col3, col4, col5 = st.columns(3)
      with col3:
       st.text_input ("Activity Source Link (URL)", value=setvalue('plpactivitylink'), key='plpactivitylink' )
      with col4:
       st.text_input ("Team Standup Async Link (URL)" , value=setvalue('plpstanduplink'), key='plpstanduplink')
      with col5:
       st.text_input ("User Async Link (URL)" , value=setvalue('plpstanduplinkusers'), key='plpstanduplinkusers')
      st.write("---")
      st.write("Enter the contact information of the team leads, architect and account manager")
      col1, col2, col3, col4, col5 = st.columns(5)
      with col1:
       st.text_input ("Solution Architect Name", max_chars=30, value=setvalue('plpsolutionname'), key='plpsolutionname', disabled=disableplan)
       st.text_input ("Controller Finance ", max_chars=30, value=setvalue('plpfinancename'), key='plpfinancename', disabled=disableplan)
      with col2:
       st.text_input ("Operations Lead Name", max_chars=30, value=setvalue('plpoperationname'), key='plpoperationname', disabled=disableplan)
      with col3:
       st.text_input ("Inspection Lead Name", max_chars=30, value=setvalue('plpinspectorname'), key='plpinspectorname', disabled=disableplan)
      with col4:
       st.text_input ("Account Manager Name", max_chars=30, value=setvalue('plpaccountname'), key='plpaccountname', disabled=disableplan)
      with col5:
       st.text_input ("Customer Project Manager Name", max_chars=30, value=setvalue('plpmcustname'), key='plpmcustname', disabled=disableplan)
      planchannels = (int(st.session_state['plnstakeholder']) + int(st.session_state['plnteam'])) * (int(st.session_state['plnstakeholder']) + int(st.session_state['plnteam']) - 1)
      st.write("---")
      st.write("The project manager supplies a video report with the reports")
      col3, col4 = st.columns(2)
      with col3:
       st.text_input ("PM report (youtube)", value=setvalue('plpmreport'), key='plpmreport')
      with col4:
       st.text_input ("PM report ID", value=setvalue('plpmid'), key='plpmid')
      plancommunication = f' There are {planchannels:.0f} communication channels. The team has a message forum at {st.session_state.plpstanduplink} and a task activity board at {st.session_state.plpactivitylink}'
      st.markdown('##') 
      st.success(plancommunication)

with tab6:
      st.subheader("Quality and Grade")
      st.write("Enter the Quality inspection types, attributes and dates.  When the inspector starts to inspect, enter the results of the quality inspection.  The PM monitor will determine a pass/fail score based on the results against the plan. ")
      cb6 = st.checkbox("askme for a quality goal")
      st.text_area ("Describe Quality Goal? (askme) ", value=setvalue('plsqualitygoal'), key='plsqualitygoal', disabled=disableplan)
      if cb6 and len(st.session_state.plsqualitygoal) < 10:
         query = "What would make customers happey in terms of the outcome of t " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)

      st.text_area ("Quality Report", value=setvalue('plsqualityreport'), key='plsqualityreport')
      col1, col2, col3 = st.columns(3)
      with col1:
       st.slider ("Number of Tests", value=setvalue('plntests'), format="%i", min_value=0, max_value=100, step=1, key="plntests" )
      with col2:
       st.slider ("Number of Tests Run", value=setvalue('plntestsrun'), format="%i", min_value=0, max_value=100, step=1, key='plntestsrun' )
      with col3:
       st.slider ("Number of Tests Failed", value=setvalue('plntestsfailed'), format="%i", min_value=0, max_value=100, step=1, key='plntestsfailed' )
      with col1:
       st.slider ("Number of Defects Allowed", value=setvalue('plntestsfailallow'), format="%i", min_value=0, max_value=100, step=1, key='plntestsfailallow' )
      with col2:
       st.session_state['plntestscritical']  = st.slider ("Number Critical Failed", value=setvalue('plntestscritical'), format="%i", min_value=0, max_value=100, step=1 )
      with col3:
       st.date_input ("Inspection Report Date", setvalue('pldinspectdate'), key='pldinspectdate')

      st.write("Enter details to calculate a grade, number of features planned, completed and inspected.  The quality of the product reports if the product is working, the grade is about product scope, how many features does the product have.  A product regardless of its service must be high-quality, however a product does not have to be high-grade, it can have minimal features and meet the goals of the sponsor.  Normally higher grade products, with more features have more risks and most cost.")
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.slider ("Number of Features", value=setvalue('plnscopenumber'), format="%i", min_value=0, max_value=100, step=1, key="plnscopenumber" , disabled=disableplan)
      with col2:
       st.slider ("Number of Features nice to have", value=setvalue('plnscopenumberwish'), format="%i", min_value=0, max_value=100, step=1, key="plnscopenumberwish" , disabled=disableplan)
      with col3:
       st.slider ("Number of Features Complete and Pass", value=setvalue('plnscopenumbersuccess'), format="%i", min_value=0, max_value=100, step=1, key="plnscopenumbersuccess" )
      with col4:
       st.slider ("Number of Features Comparable", value=setvalue('plnscopenumbercomp'), format="%i", min_value=0, max_value=100, step=1, key="plnscopenumbercomp", help="Describe the number of features in comparable products" , disabled=disableplan)
      st.multiselect(
         label='Select types of quality inspection attributes',
         options=['Component or by Piece Testing', 'Pre Production Testing(PPI)', 'Pre Shipment/Final Inspection(PSI)', 'Security Test', 'Regulatory/Compliance Testing', 'Code Scanner', 'None'],
         default=setvalue('plmlistqualitytypes'), key='plmlistqualitytypes', max_selections = 5)
     #  test results, test not done, test run less than tolerance of 70% test failed more than 20 or critical test failed is positive
      st.session_state['thepminspectionwarning'] = "Inspection planned or passed." 
      st.session_state['thepminspectionflag'] = 0 
      if st.session_state.plntests == 0 or st.session_state.plntestscritical > 0 or (st.session_state.plntestsrun == 0 and st.session_state.pldinspectdate < daytoday ):
        st.session_state['thepminspectionwarning'] = "Inspection plan missing or failed." 
        st.session_state['thepminspectionflag'] = 1 
      planquality = f'There are {st.session_state.plntests:.0f}  tests planned. '
      passfail = 0
      passcoverage = 0
      if int(st.session_state.plntests) > 0:
        passfail = int(st.session_state.plntestsfailed / st.session_state.plntests * 100) 
        passcoverage = int(st.session_state.plntestsrun / st.session_state.plntests * 100) 
      st.session_state['thepmquality'] = f'{planquality} The inspector is {st.session_state.plpinspectorname}.  The inspection report is planned on {st.session_state.pldinspectdate.strftime("%Y-%m-%d")}  Pass to fail rate is {passfail:.0f}%. Test coverage is {passcoverage}%.  {st.session_state.plsqualityreport} . ' 
      st.markdown('##') 
      st.success(st.session_state['thepmquality'])
      st.success(st.session_state['thepminspectionwarning'])
      #  Grade
      grade = (get_grade(st.session_state.plnscopenumbercomp, st.session_state.plnscopenumber)) 
      gradedelivered = (get_grade(st.session_state.plnscopenumbersuccess, st.session_state.plnscopenumber)) 
      nonfunctlist = ' '.join(st.session_state.plmlistscopelist)
      st.session_state['thepmgrade'] = f'A product with {st.session_state.plnscopenumber} features has a grade of {grade}.  The current grade is {gradedelivered} which measures the number of features delivered and passed inspection. The number of actors or personas is {st.session_state.plnactors} increasing actors will increase cost however will improve grade.  Delivery of nice to have features or high quality non-functional attributes will also improve the grade.  The non-functional attributes are {nonfunctlist}' 
      st.success(st.session_state.thepmgrade) 
with tab3:
      st.subheader("Cost")
      st.write("Changes incur costs, and these costs are monitored to ensure that the investment is in line with the value of the change to the business.  Using feature completion, and timelines we calculate cost performance index (CPI) and schedule performance index (SPI) which are indicators if the project is in control. During conception and planning, earned value will be 0, when you start execution your earned value will be realized as features are inspected and accepted")
      currchoice = pd.DataFrame({'Item': ['None', 'USD', 'CDN', 'EUR'], 'Value': [0, 1, 2, 3]})
      col4, col5 = st.columns(2)
      with col4:
       selected_cur1 = st.selectbox("Income Currency", currchoice.Item, index=setvalue('pllistincomecurrency')) 
       st.session_state['pllistincomecurrency'] = currchoice.loc[currchoice.Item == selected_cur1]["Value"].iloc[0]
      with col5:
       selected_cur2 = st.selectbox("Expense Currency", currchoice.Item, index=setvalue('pllistexpensecurrency')) 
       st.session_state['pllistexpensecurrency'] = currchoice.loc[currchoice.Item == selected_cur2]["Value"].iloc[0]
      st.slider('Budget', min_value=0, max_value=200000, value=setvalue('plnbudget'), step=5000, key='plnbudget', disabled=disableplan)
      st.slider('Spend to Date', min_value=0, max_value=250000, value=setvalue('plnspend'), step=500, key='plnspend')
      col1, col2, col3, col4, col5 = st.columns(5)
      with col1:
       st.slider('Estimated Work Hours', min_value=0, max_value=2000, value=setvalue('plnhours'), step=10, key='plnhours', disabled=disableplan)
      with col2:
       st.slider('Average Rate', min_value=0, max_value=200, value=setvalue('plnavgrate'), step=5, key='plnavgrate')
      with col3:
       st.slider('Work Hours Performed', min_value=0, max_value=2000, value=setvalue('plnhoursused'), step=10, key='plnhoursused')
      with col4:
       st.slider('Estimate Confidence', min_value=0, max_value=100, value=setvalue('plnhoursconfidence'), step=5, key='plnhoursconficence', disabled=disableplan)
      with col5:
       st.slider('Estimate Complete', min_value=0, max_value=100, value=setvalue('plnestimatecomplete'), step=5, key='plnestimatecomplete', help="Enter the value for earned value estimate")
      plbudget = st.session_state['plnbudget']
      plspend = st.session_state['plnspend']
      mcomplete = st.session_state.plnestimatecomplete
      mplanned = 100
      st.session_state['thepmdelivery'] = int (mcomplete / mplanned * 100)
      (evsummary, st.session_state['thepmcpi'], st.session_state['thepmspi'], etc, st.session_state['thepmevm'])  = evreport((plbudget + (plbudget *.3)), plbudget, st.session_state['plnhours'], st.session_state['plnavgrate'], "EUR" , st.session_state['pldstartdate'], st.session_state['pldenddate'], plspend, mplanned, mcomplete, daystoend, daystoday, st.session_state['thepmtimecomplete'])
      st.session_state['thepmbudgetcomplete'] = 0
      if plbudget > 0:
        st.session_state['thepmbudgetcomplete'] = int(plspend / plbudget * 100)
      st.markdown("{}".format(evsummary), unsafe_allow_html=True)
      st.session_state['thepmevsummary'] = evsummary
      st.table(st.session_state.thepmevm)
      #st.table(st.session_state.thepmevm, hide_index=True, use_container_width=True)

with tab8:
      st.subheader("Return on Investment")
     #https://www.investopedia.com/articles/basics/10/guide-to-calculating-roi.asp
     #[200~https://www.coface.com/news-economy-and-insights/business-risk-dashboard/country-risk-files/canada
      st.write("Measure the benefits or return on the investment over time based on the benefits, either savings or increased income after release.  Provide the date when new benefits are expected to start, and the number of periods to allocate the investment.  A benefit date before end of project is a sign of agile delivery or iterative delivery to give value in increments, or a maintanance project.  The ROI is a number that is used to measure the value of the investment in this project against other projects in your portfolio.")
      st.write("input country , gdp, inflation, unemployment, growth,  Business climate, country risk")

# https://www.focus-economics.com/countries/spain/
# https://santandertrade.com/en/portal/analyse-markets/spain/economic-political-outline#
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.session_state['plnincreaseincome']  = st.slider ("Benefit Income", value=setvalue('plnincreaseincome'), format="%i", min_value=-100000, max_value=1000000, step=5000 )
      with col2:
       st.session_state['plnincreaseexpense']  = st.slider ("New Expenses against Benefits", value=setvalue('plnincreaseexpense'), format="%i", min_value=-100000, max_value=1000000, step=5000 )
      with col3:
       st.session_state['plnbenefitperiod']  = st.slider ("Benefit Period", value=setvalue('plnbenefitperiod'), format="%i", min_value=1, max_value=36, step=1,  help="Enter the number of months you want to spread out this investment" )
      with col4:
       st.session_state['pldbenefitdate']  = st.date_input ("Benefit Start Date", value=setvalue('pldbenefitdate'))
      cb12 = st.checkbox("Askme for ROI Information")
      st.session_state['plproigoal'] = st.text_area("ROI Goal", value=setvalue('plproigoal'))
      if cb12 and len(st.session_state.plproigoal) < 10:
         query = "What is the ROI goal for a   " + st.session_state.plpname + " project with an investment of " + format(st.session_state.plnbudget,'.0f')
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)

      benefitdelta = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'])
      roi = 0
      rateofreturn = 0
      benefitdate = st.session_state['pldbenefitdate']
      if plbudget > 0:
        roi = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'] - plbudget) / (plbudget + etc) * 100
        rateofreturn = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'] - (plbudget + etc)) / (plbudget + etc)
     # annualroi = (1 + rateofreturn) ^ (1 / st.session_state['plnbenefitdate']) - 1
     # st.write(annualroi)
      st.session_state['thepmroisummary'] = f'The roi is {roi:.3f} with an investment of {plbudget:.0f} and a benefit of {benefitdelta:.0f} to begin {benefitdate :%B %d, %Y} '
      st.write(st.session_state.thepmroisummary)

with tab7:
      st.subheader("Environment and Constraints")
      st.write("What constraints impact time, scope, quality or cost. Little to no flexibility in time, cost or scope is normally a risk but can be a constraint when the probability of risks are almost certain.  Environmental issues are risks that are expected to occur in a project such as weather events, or limits of people and resources, when plans are not clear or finalized they become a constraint.")
      st.write("Describe the approach to limit impact of issues with Scope, Time, Budget or Resources. Choose a range on the slider related to the impact with 5 highest impact.  Example, if scope changes will the project be severely impacted (5 - High) or will scope changes be tolerated and have low impact because you have planned and communicated how to change scope in this project (1 - Low).  ")
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnscoperange']  = st.slider ("Scope Risk", value=setvalue('plnscoperange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       cb7 = st.checkbox("Askme for scope mitigation strategies")
       st.session_state['plpscopecontingency']  = st.text_area ("What are three ways to mitigate the impact of scope changes in a project? (askme)", value=setvalue('plpscopecontingency'))
       if cb7 and len(st.session_state.plpscopecontingency) < 10:
         query = "What are three strategies to reduce the impact of scope changes in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)

      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnschedulerange']  = st.slider ("Schedule Risk", value=setvalue('plnschedulerange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       cb8 = st.checkbox("Askme for schedule mitigation strategies")
       st.session_state['plptimecontingency']  = st.text_area ("Schedule Contingency? (askme)", value=setvalue('plptimecontingency'))
       if cb8 and len(st.session_state.plptimecontingency) < 10:
         query = "What are three strategies to reduce the impact of schedule issues in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnbudgetrange']  = st.slider ("Budget Risk", value=setvalue('plnbudgetrange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       cb9 = st.checkbox("Askme for budget mitigation strategies")
       st.session_state['plpbudgetcontingency']  = st.text_area ("Budget Contingency", value=setvalue('plpbudgetcontingency'))
       if cb9 and len(st.session_state.plpbudgetcontingency) < 10:
         query = "What are three strategies to reduce the impact of cost overruns in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnteamrange']  = st.slider ("Team Risk", value=setvalue('plnteamrange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       cb10 = st.checkbox("Askme for team mitigation strategies")
       st.session_state['plpteamcontingency']  = st.text_area ("Team Contingency", value=setvalue('plpteamcontingency'))
       if cb10 and len(st.session_state.plpteamcontingency) < 10:
         query = "What are three strategies to reduce the impact of low performing teams in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnresourcerange']  = st.slider ("Resource Risk", value=setvalue('plnresourcerange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       cb11 = st.checkbox("Askme for resource or technology mitigation strategies")
       st.session_state['plpresourcecontingency']  = st.text_area ("Resource Contingency", value=setvalue('plpresourcecontingency'))
       if cb11 and len(st.session_state.plpresourcecontingency) < 10:
         query = "What are three strategies to reduce the impact of resource or technology challenges in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query)
         message = chatbot.query(query)
         st.code(message)
      thepmcontingencysummary = "The project contingency plans include Scope: " + st.session_state['plpscopecontingency']+ " Schedule: " + st.session_state['plptimecontingency'] + " Budget:  " + st.session_state['plpbudgetcontingency'] + " and Resource:  " + st.session_state['plpresourcecontingency']
      st.markdown("{}".format(thepmcontingencysummary), unsafe_allow_html=True)

      st.session_state['thepmteam'] = f'The team is composed of {st.session_state.plnteam:.0f}  members and have collaborated together for {st.session_state.plnteamweeks:.0f} weeks.  \n\n   The solution architect is {st.session_state.plpsolutionname}. The Operations Lead is {st.session_state.plpoperationname}. The inspector is {st.session_state.plpinspectorname}.  There are currently {st.session_state.plnopenroles:.0f} open roles. '

with tab9:
    placeholder = st.empty()
    textquestion = st.text_input ("Ask AI for general help, enter a question")
    #st.button('askmeforhelp', key='askmeforhelp')  
    #chatbot.change_conversation(id)
    if  len(textquestion) > 10:
      message = chatbot.query(textquestion)
      st.write(textquestion)
      textquestion = ""
      st.code(message)

with tab10:
     st.write("Risk trigger default values")
     risktriggers = {'Inflation': 10, 'Changes': 1, 'Earned Value': 0, 'Sentiment': 70, 'Engagement': 80, 
        'CPI': 0,
        'SPI': 0, 'Inspection': 3, 'ROI': 120, 'Late Start': 3, 'Climate': 1, 'Unemployment': 8, 'Business Climate': 'B',
        'Country Risk': 'B' }
     st.data_editor(risktriggers)
