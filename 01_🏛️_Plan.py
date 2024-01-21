import streamlit as st
from PIL import Image
from datetime import timedelta, date, datetime
import pandas as pd
from scripts.thepmutilities import evreport, plancomment, get_grade, gradiant_header
import altair as alt
from hugchat import hugchat
from hugchat.login import Login
from streamlit_extras.app_logo import add_logo
from streamlit_extras.switch_page_button import switch_page
import extra_streamlit_components as stx

st.session_state.update(st.session_state)
ip = Image.open("assets/images/PlanImage.png")
il = Image.open("assets/images/MonitorImage.png")

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

def clearaskme():
    #st.session_state.something = st.session_state.widget
    st.session_state.askmeaquestion = ''

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
         if var.startswith('plm'):
            return st.session_state[var] if var in st.session_state else "None"
         else:
            return st.session_state[var] if var in st.session_state else var

im = Image.open("assets/images/BlueZoneIT.ico")
imurl = "assets/images/BlueZoneIT.ico"

st.set_page_config(
      page_title="The PM Monitor Plan",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

chatbot = signonhugchat()

#  get the theme colors
color1t = st._config.get_option('theme.primaryColor')
color1b = st._config.get_option('theme.secondaryBackgroundColor')
color1c = st._config.get_option('theme.backgroundColor')
color1d = st._config.get_option('theme.textColor')

with st.sidebar:

  #cyclelist = ["None", "Planning", "Execution/Control", "Close"]
  #cycleoptions = list(range(len(cyclelist)))
  #val = stx.stepper_bar(steps=cyclelist)
  #st.info(f"Phase #{val}")
  #st.session_state['thepmcycle'] = val
  #thepmcycle = st.selectbox('Project Phase (planning or monitoring?)', cycleoptions, format_func=lambda x: cyclelist[x], key='thepmcycle', help="The phase of the project will determine which risks are higher or may be closed.  In the early phases of the project you have higher technology and cost risks and in later phases you can have engagement and resource risks. A project has 4 phases, Initiation, Planning, Execution and Control and Closure.  A product has 6 phases.   0 Initiation, 1 plan, 2 design, 3 build, 4 inspect, 5 accept and  6 close")

  want_plan = st.toggle("Planning or Control")
  if want_plan:
        val = 2 
  else:
        val = 1 
  st.session_state['thepmcycle'] = val

  st.date_input ("Report Date", setvalue('pldcharterdate'), key='pldcharterdate', help="Enter the date that this report is updated.")
  want_help = st.toggle("Inline Help")
  if want_help:
        labelvis="visible"
  else:
        labelvis="collapsed"

  want_to_contribute = st.button("Help")
  if want_to_contribute:
        switch_page("Help")

theme_scope = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-check-circle'}
font_fmt = {'font-class':'h4','font-size':'50%'}
mySep = ","

if st.session_state.thepmcycle > 1:
  gradiant_header ('The PM Monitor Project Monitoring') 
else:
  gradiant_header ('The PM Monitor Project Planning') 

##  Introduction to Planning

with st.container():
  with st.expander("Playbook Information"):
     if st.session_state.thepmcycle > 1:
      st.image(il)
     else:
      st.image(ip)

     if st.session_state.thepmcycle < 2:
      st.write("1.  The assigned project manager meets with stakeholders, gather information, identify and document the goal, deliverables, budget and schedule.  Identify resources and constraints.  Review the risks and define project manager authority and contingency plans. ")
      st.write("2.  Fill in the project plan using the form.   Move one tab at a time, fill in the information in the form. Using Askme AI assistance for the narrative text. Fill in all information.    ")
      st.write("3.  Print the charter and review with stakeholders.  Confirm there is acceptance on the plan, goals and deliverables  ")
      st.write("4.  Assemble the team, have team kickoff using the canvas poster. Setup team tools. ")
      st.write("5.  Book your calendar to monitor project progress and generate status updates and stoplight report.    ")

     ##  The basic intro information 
with st.container():
      with st.expander("Project Information"):
        st.write("A project is finite, has a start and and end timeframe and is unique. A project is undertaken to reach a goal, implement change, deliver a new product, service or process.  The Project Plan outlines the timeline and the benefits, scope and contingency plans.  The plan provides the necessary information for the project manager and The PM Monitor to report on the progress of the project, manage risks and identify issues.")
      plancontainer = st.empty()
      disableplan = False
      if st.session_state.thepmcycle > 1:
        disableplan = True
      st.text_input ("Project Name", help="A short project name, use key words to describe the project. ", max_chars=50, key='plpname', value=setvalue('plpname'), disabled=disableplan, label_visibility=labelvis)
      st.text_input ("Project ID", max_chars=10, value=setvalue('plpnumber'), help="A unique id to identify this project", key='plpnumber', label_visibility=labelvis,disabled=disableplan)
      st.text_input ("Project Manager Identification", max_chars=30, value=setvalue('plpmname'), key='plpmname',label_visibility=labelvis, disabled=disableplan)
      st.text_input ("Product Owner or Sponsor Identification", max_chars=30, value=setvalue('plspname'), key='plspname',label_visibility=labelvis, disabled=disableplan)

      phaselist = ("None", "Plan", "Design", "Build", "Inspect", "Accept", "Close")
      phaseoptions = list(range(len(phaselist)))
      col5, col6 = st.columns([1,4])
      with col5:
       st.write('Cadence')
      with col6:
       st.slider('Cadence', min_value=0, max_value=12, value=setvalue('plncadence'), help="Cadence is the frequency that the project replans and reports on progress.  In a maintenance project you should plan and report quarterly.  In active development projects when investment is higher, you should be planning and reporting weekly", key='plncadence', disabled=disableplan, label_visibility=labelvis)
      classchoice = pd.DataFrame({'Item': ['None', 'Software Build', 'Software Design', 'Brand Marketing', 'Process Automation', 'Scheduled Maintenance', 'Content Migration', 'Decommission', 'Upgrade', 'Training or Documentation'], 'Value': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}) 
      classlist = ('None', 'Software Build', 'Software Design', 'Brand Marketing', 'Process Automation', 'Scheduled Maintenance', 'Content Migration', 'Decommission', 'Upgrade', 'Training or Documentation')

      col1, col2, col3, col4 = st.columns([1,2,1,2])
      with col1:
       st.write("Start")
      with col2:
       st.date_input ("Start Date", setvalue('pldstartdate'), key='pldstartdate', help="Enter the project start date",label_visibility=labelvis, disabled=disableplan)
      with col3:
       st.write("End")
      with col4:
       st.date_input ("End Date", setvalue('pldenddate'), key='pldenddate', help="Enter the project end date", label_visibility=labelvis, disabled=disableplan)
      col1, col2 = st.columns([1,5])
      with col1:
       st.write("Classify")
      with col2:
       classoptions = list(range(len(classlist)))
       selected_class = st.selectbox("Project Classification", classoptions, format_func=lambda x: classlist[x], help="The type of project will be used to determine risks, a physical build can be impacted by weather.  Changes to procedures or pipelines require more focus on communication activities", key='pllisttype', label_visibility=labelvis, disabled=disableplan )

    
      cb1 = st.checkbox ("Askme for a purpose.", key='cb1', disabled=disableplan)
      st.text_area ("Purpose or Goal?", value=setvalue('plspurpose'), key='plspurpose', label_visibility=labelvis,disabled=disableplan)
      if cb1 and len(st.session_state.plspurpose) < 12:
         conversation_list = chatbot.get_conversation_list()
         models = chatbot.get_available_llm_models()
# Switch model to the given index
         # Create a new conversation
         id = chatbot.new_conversation()
         chatbot.change_conversation(id)
         #chatbot.delete_all_conversations()
         query = "What is the purpose of a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb1, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query) 
         st.code(message)
      del st.session_state['cb1']
      cb2 = st.checkbox ("Askme for three benefits.", disabled=disableplan)
      st.text_area ("Benefits", value=setvalue('plsbenefits'), key='plsbenefits',label_visibility=labelvis, disabled=disableplan)
      if cb2 and len(st.session_state.plsbenefits) < 12:
         query = "What are three benefits of " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query) 
         st.code(message)
      cb3 = st.checkbox("Askme for benchmarks.", disabled=disableplan)
      st.text_area ("Benchmarks", value=setvalue('plsbenchmarks'), key='plsbenchmarks',label_visibility=labelvis, disabled=disableplan)
      if cb3 and len(st.session_state.plsbenchmarks) < 10:
         query = "Are there comparable benchmarks or services for a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query) 
         st.code(message)
     # set some dates
      week  = timedelta(days = 7)
      daytoday = date.today()
     
     # how much time to end of plan
      daystoend = (st.session_state['pldenddate']-st.session_state['pldstartdate']).days
      daystoday = (daytoday-st.session_state['pldstartdate']).days
      weeksinplan = int(daystoend/7)
      st.session_state['thepmtimecomplete'] = 0
      if daystoend > 0:
        st.session_state['thepmtimecomplete'] = int(daystoday / daystoend * 100)

     ##  output information and create header block
 
    #  a header block for reports
      ndays = st.session_state['plncadence']*7
     #  Scope section 

with st.container():
       st.subheader("Change")
       with st.expander("Change information"):
          st.write("Change information is collected during control and monitoring.  Capture changes to the scope, schedule, cost or quality goals and make a note of who reviewed and approved the change.")
       scopechange = st.text_area ("What scope has been added or removed after the start of this project? ", value=setvalue('plscopechange'), key='plscopechange')
       otherchange = st.text_area ("What other changes have been made to this project? schedule, cost, quality ", value=setvalue('plsotherchange'), key='plsotherchange')
       approvalchange = st.text_area ("Describe the change, who presented the change, why, when and who approved. ", value=setvalue('plsapprovalchange'), key='plsapprovalchange')

with st.container():
       st.subheader("Scope")
       with st.expander("Scope Information"):
         st.write("The scope information outlines the features that the product should have. Scope also clarifies what is not planned and what may be negotiable.  When monitoring the project, identify any scope changes.  It is important to track out of scope items.  ")

         st.write("The following is a narrative explaining the scope and goal of this project.   If there is flexibility then separate the must have and nice to have scope.")

       col4, col5 = st.columns(2)
       cb4 = st.checkbox("Askme for must have scope.", disabled=disableplan)
       st.text_area ("What is the must have scope?", value=setvalue('plscopemusthave'), key='plscopemusthave' ,label_visibility=labelvis, disabled=disableplan)
       if cb4 and len(st.session_state.plscopemusthave) < 10:
         query = "What are three must have features of a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)

       cb5 = st.checkbox("Askme for scope options.", disabled=disableplan)
       st.text_area ("What are some features that are negotiable or nice to have?", value=setvalue('plscopenicetohave'), key='plscopenicetohave',label_visibility=labelvis, disabled=disableplan)
       if cb5 and len(st.session_state.plscopenicetohave) < 10:
         query = "What are three nice to have features in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)

       st.text_area ("Dictionary.  Define any terms used in this product or design", value=setvalue('plscopeterms'), key='plscopeterms' , label_visibility=labelvis, disabled=disableplan)

       st.text_area ("What is out of scope?", value=setvalue('plscopeoutofscope'), key='plscopeoutofscope', label_visibility=labelvis, disabled=disableplan)
       col4, col5 = st.columns(2)
       with col5:
        st.multiselect( label='Select non functional attributes', help='Press enter to add', options=['Security', 'Availability', 'Usability', 'Maintainability','Documentation', 'Accessibility', 'Compliance', 'Robustness', 'Reliablity', 'Performance', 'Localization', 'Compatiblity', 'Portability', 'Scalability', 'None'], default=setvalue('plmlistscopelist'), key='plmlistscopelist', max_selections = 4,label_visibility=labelvis, disabled=disableplan)
       with col4:
         st.multiselect( label='Select technical architecture attributes and resources in the scope', options=['CMS', 'Web Framework', 'SEO', 'Search', 'Cloud Hosting', 'OnPrem Hosting', 'Automation',  'ERP', 'CDN', 'CI/CD', 'Custom Theme', 'No/Low Code', 'Native Mobile App', 'Process Model', 'Database', 'Testing', 'Decommission', 'Data Migration', 'SAAS', 'None'], default=setvalue('plmlistscopeoption'), key='plmlistscopeoption', max_selections = 4,label_visibility=labelvis, disabled=disableplan)
       if len(scopechange) > 15:
          scopechange = f'There are scope changes. {scopechange}'
       st.session_state['thepmplanscope'] = f'Required:  \n  {st.session_state.plscopemusthave} \n\n  Options:  \n\n  {st.session_state.plscopenicetohave}  \n\n \n\n  Out of Scope:  {st.session_state.plscopeoutofscope} \n\n Change:  {scopechange}'
       st.success(st.session_state['thepmplanscope'])


##  Schedule
with st.container():
      milestonestatus = {0: "Not started", 1: "In Progress", 2: "On Hold", 3: "Complete"}
      st.subheader("Life Cycle")
      with st.expander("Schedule and Status Product delivery"):
        st.write("The life cycle of a product defines the phases of the product.   A project must complete the product planning phase, and can be executing more than one phase concurrently.  Phases have activities defined in the WBS. ")
        st.write("When monitoring, choose a status value RAG (Green - Phase is on track,  Amber - Phase has missed some targets but overall end date and budget is not at risk,  Red - Product development is likely to deliver over budget or late.  There will be management action items in the stoplight report. ")

      statusoptions = (['None', 'Red', 'Amber', 'Green'])
      cola, colb, cold = st.columns([1,3,3])
      cola.write("Plan")
      colb.date_input ("Plan Date", setvalue('pldplandate'), key='pldplandate', help="Enter the target product plan date",label_visibility=labelvis, disabled=disableplan, min_value=st.session_state.pldstartdate, max_value=st.session_state.pldenddate)
      cold.select_slider('Status Reporting', options=statusoptions, key='plmplanstatus', label_visibility=labelvis)
      cola, colb, cold = st.columns([1,3,3])
      cola.write("Design")
      colb.date_input ("Design Date", setvalue('plddesigndate'), key='plddesigndate', help="Enter the target product design date", label_visibility=labelvis,disabled=disableplan, min_value=st.session_state.pldstartdate, max_value=st.session_state.pldenddate)
      cold.select_slider('Status Reporting', options=statusoptions, key='plmdesignstatus', label_visibility=labelvis)
      cola, colb, cold = st.columns([1,3,3])
      cola.write("Build")
      colb.date_input ("Build Date", setvalue('pldbuilddate'), key='pldbuilddate', help="Enter the target product build date", label_visibility=labelvis,disabled=disableplan, min_value=st.session_state.pldstartdate, max_value=st.session_state.pldenddate)
      cold.select_slider('Status Reporting', options=statusoptions, key='plmbuildstatus', label_visibility=labelvis)
      cola, colb, cold = st.columns([1,3,3])
      cola.write("Inspect")
      colb.date_input ("Inspect Date", setvalue('pldinspectdateplan'), key='pldinspectdateplan', help="Enter the target product inspect date", label_visibility=labelvis,disabled=disableplan, min_value=st.session_state.pldstartdate, max_value=st.session_state.pldenddate)
      cold.select_slider('Status Reporting', options=statusoptions, key='plminspectstatus', label_visibility=labelvis)
      cola, colb, cold = st.columns([1,3,3])
      cola.write("Accept")
      colb.date_input ("Accept Date", setvalue('pldacceptdate'), key='pldacceptdate', help="Enter the target product accept date", label_visibility=labelvis,disabled=disableplan, min_value=st.session_state.pldstartdate, max_value=st.session_state.pldenddate)
      cold.select_slider('Status Reporting', options=statusoptions, key='plmacceptstatus', label_visibility=labelvis)
      sdate = st.session_state['pldstartdate']
      #[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
      x = 1 
      if st.session_state.pldacceptdate > date.today():
        x = 5     
      if st.session_state.pldinspectdateplan > date.today():
        x = 4     
      if st.session_state.pldbuilddate > date.today():
        x = 3     
      if st.session_state.plddesigndate > date.today():
        x = 2     
      st.session_state['thepmphase'] = x
      st.write('The current phase is ', phaselist[x], x, date.today())
      reportsinplan = 1
      if st.session_state['plncadence'] > 0:
       reportsinplan = int(weeksinplan/st.session_state['plncadence'])
      #  we must report at least close of each phase
      if reportsinplan < 6:
       reportsinplan = 6 
      st.session_state['thepmreportsinplan'] = reportsinplan

      st.session_state['thepmheader'] = pd.DataFrame({
       "Project": [st.session_state.plpname, st.session_state.plpmname],
       "Sponsor": [st.session_state.plpnumber, st.session_state.plspname],
       "Phase": [phaselist[x], st.session_state.pldcharterdate]
        })
      st.session_state['thepmphasename'] = phaselist[x]
      st.session_state['thepmplannote'] = plancomment(st.session_state['pldstartdate'], st.session_state['pldenddate'], daystoday, daystoend, st.session_state['thepmtimecomplete'], 3, st.session_state['plpnumber'], st.session_state['plpname'], st.session_state['plsbenefits'], st.session_state['plncadence'], phaselist[st.session_state['thepmphase']], st.session_state['plspname'], classlist[selected_class])
      st.write("There will be ", reportsinplan, " Status Reports")
      plancontainer.success(st.session_state.thepmplannote) 
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

      st.session_state['thepmmilestones'] = oseries
      chart = alt.Chart(oseries).mark_line(point = True).encode(
          alt.X('yearmonthdate(reportdate):O', title='Report Date'),
          alt.Y('yearmonthdate(plandate):O', title='Plan Date', scale=alt.Scale(reverse=True)),
          color="Milestone", text="Milestone")
      st.altair_chart(chart, use_container_width=True)

      # st.write(oseries)

with st.container():
   with st.container():
      st.subheader("Team Information")
      with st.expander("Describe the team"):
        st.write("Projects are executed and implemented by people, the team, the stakeholders and are implemented to provide benefit to users or customers.  The complexity communication, controlling  and establishing trust between the team and the stakeholders is a factor of the size of the team, and how long they have been working together.  Trust is earned, not given, and as trust increases, performance will improve and quality will follow.  Typically engagement and team sentiment is high at the beginning of the project and decreases over time, and engagement of the stakeholders follows the opposite pattern  ")
        st.write("Describe the size of the team, number of users, actors and stakeholders")
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.slider ("Number of Stakeholders", value=setvalue('plnstakeholder'), format="%i", min_value=0, max_value=10, step=1, key='plnstakeholder', disabled=disableplan )
      with col2:
       st.slider ("Number of Core Team Members", value=setvalue('plnteam'), format="%i", min_value=0, max_value=15, step=1, key='plnteam', disabled=disableplan)
      with col3:
       st.slider ("Number of Users", value=setvalue('plnusers'), format="%i", min_value=0, max_value=100000, step=10000, key='plnusers', disabled=disableplan)
      with col4:
       st.slider ("Number of Actors", value=setvalue('plnactors'), format="%i", min_value=0, max_value=10, step=1, key='plnactors', disabled=disableplan)
with st.container():
      st.subheader("Team Monitoring")
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
with st.container():
      st.subheader("Tools and Links")
      st.write("Location of the cloud tools, the team WBS and their communication channel")
      col3, col4, col5 = st.columns(3)
      with col3:
       st.text_input ("Task Activity Source Link (URL)", value=setvalue('plpactivitylink'), key='plpactivitylink', disabled=disableplan )
       st.text_input ("Documentation Folder (URL)", value=setvalue('plpdocumentslink'), key='plpdocumentslink', disabled=disableplan )
      with col4:
       st.text_input ("Team Standup Channel Link (URL)" , value=setvalue('plpstanduplink'), key='plpstanduplink', disabled=disableplan)
       st.text_input ("Team Source Code Git Link (URL)" , value=setvalue('plpgithublink'), key='plpgithublink', disabled=disableplan)
      with col5:
       st.text_input ("Product Owner Design Link (URL)" , value=setvalue('plpproductownerdesignlink'), key='plpproductownerdesignlink', disabled=disableplan)
       st.text_input ("User Chat Channel Link (URL)" , value=setvalue('plpstanduplinkusers'), key='plpstanduplinkusers', disabled=disableplan)
      st.write("---")
with st.container():
      st.subheader("Key Decision makers and contacts")
      st.write("Contact information of the team leads, architect and account manager, and key stakeholders")
      col1, col2, col3 = st.columns(3)
      with col1:
       st.text_input ("Solution Architect Name", max_chars=30, value=setvalue('plpsolutionname'), key='plpsolutionname', disabled=disableplan)
       st.text_input ("Controller Finance ", max_chars=30, value=setvalue('plpfinancename'), key='plpfinancename', disabled=disableplan)
      with col2:
       st.text_input ("Operations Lead Name", max_chars=30, value=setvalue('plpoperationname'), key='plpoperationname', disabled=disableplan)
       st.text_input ("Inspection Lead Name", max_chars=30, value=setvalue('plpinspectorname'), key='plpinspectorname', disabled=disableplan)
      with col3:
       st.text_input ("Account Manager Name", max_chars=30, value=setvalue('plpaccountname'), key='plpaccountname', disabled=disableplan)
       st.text_input ("Product Owner Name", max_chars=30, value=setvalue('plpmcustname'), key='plpmcustname', disabled=disableplan)
      planchannels = (int(st.session_state['plnstakeholder']) + int(st.session_state['plnteam'])) * (int(st.session_state['plnstakeholder']) + int(st.session_state['plnteam']) - 1)
      plancommunication = f' There are {planchannels:.0f} communication channels. The team has a message forum at {st.session_state.plpstanduplink} and a task activity board at {st.session_state.plpactivitylink}.  Artefacts and documents are found {st.session_state.plpdocumentslink} and code is found {st.session_state.plpgithublink}.  The design artefacts are found at {st.session_state.plpproductownerdesignlink}'
      st.markdown('##') 
      st.success(plancommunication)

with st.container():
   with st.container():
      st.subheader("Quality Planning")
      st.write("Enter the Quality inspection types, attributes and dates.  When the inspector starts results will be available in the quality inspection report.  The PM monitor will determine a pass/fail score based on the results against the plan. ")
      cb6 = st.checkbox("Askme for a quality goal")
      st.text_area ("Describe Quality Goal ", value=setvalue('plsqualitygoal'), key='plsqualitygoal', disabled=disableplan)
      if cb6 and len(st.session_state.plsqualitygoal) < 10:
         query = "What would make customers happey in terms of the outcome of t " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)
      st.multiselect(
         label='Select types of quality inspection attributes',
         options=['Component or by Piece Testing', 'Pre Production Testing(PPI)', 'Pre Shipment/Final Inspection(PSI)', 'Security Test', 'Regulatory/Compliance Testing', 'Code Scanner', 'None'],
         default=setvalue('plmlistqualitytypes'), key='plmlistqualitytypes', max_selections = 5, disabled=disableplan)

      st.subheader("Quality Monitoring")
      st.text_area ("Quality Report", value=setvalue('plsqualityreport'), key='plsqualityreport')
      col1, col2, col3 = st.columns(3)
      with col1:
       st.slider ("Number of Tests", value=setvalue('plntests'), format="%i", min_value=0, max_value=100, step=1, key="plntests" )
      with col2:
       st.slider ("Number of Tests Run", value=setvalue('plntestsrun'), format="%i", min_value=-1, max_value=st.session_state.plntests, step=1, key='plntestsrun' )
      with col3:
       st.slider ("Number of Tests Failed", value=setvalue('plntestsfailed'), format="%i", min_value=-1, max_value=st.session_state.plntestsrun, step=1, key='plntestsfailed' )
      with col1:
       st.slider ("Number of Defects Allowed", value=setvalue('plntestsfailallow'), format="%i", min_value=-1, max_value=st.session_state.plntests, step=1, key='plntestsfailallow' )
      with col2:
       st.session_state['plntestscritical']  = st.slider ("Number Critical Failed", value=setvalue('plntestscritical'), format="%i", min_value=-1, max_value=st.session_state.plntestsrun, step=1 )
      with col3:
       st.date_input ("Inspection Report Date", setvalue('pldinspectdate'), key='pldinspectdate', min_value=st.session_state.pldstartdate, max_value=st.session_state.pldenddate)

     #  test results, test not done, test run less than tolerance of 70% test failed more than 20 or critical test failed is positive
      st.session_state['thepminspectionwarning'] = "Inspection planned or passed." 
      st.session_state['thepminspectflag'] = 0 
      if st.session_state.plntests == 0 or st.session_state.plntestscritical > 0 or (st.session_state.plntestsrun == 0 and st.session_state.pldinspectdate < daytoday ):
        st.session_state['thepminspectionwarning'] = "Inspection plan missing or failed." 
        st.session_state['thepminspectflag'] = 1 
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

with st.container():
      st.subheader("Grade")
      with st.expander("What is grade?"):
        st.write("Enter details to calculate a grade, number of features planned, completed and inspected.  The quality of the product reports if the product is working, the grade is about product scope, how many features does the product have.  A product regardless of its service must be high-quality, however a product does not have to be high-grade, it can have minimal features and meet the goals of the sponsor.  Normally higher grade products, with more features have more risks and most cost.")
      col1, col2, col3 = st.columns(3)
      with col1:
       st.slider ("Number of Features", value=setvalue('plnscopenumber'), format="%i", min_value=0, max_value=100, step=1, key="plnscopenumber" , disabled=disableplan)
      with col2:
       st.slider ("Number of Features nice to have", value=setvalue('plnscopenumberwish'), format="%i", min_value=0, max_value=100, step=1, key="plnscopenumberwish" , disabled=disableplan)
      with col3:
       st.slider ("Number of Features Comparable", value=setvalue('plnscopenumbercomp'), format="%i", min_value=0, max_value=100, step=1, key="plnscopenumbercomp", help="Describe the number of features in comparable products" , disabled=disableplan)


      #  Grade
      grade = (get_grade(st.session_state.plnscopenumbercomp, st.session_state.plnscopenumber)) 
      nonfunctlist = ' '.join(st.session_state.plmlistscopelist)
      st.session_state['thepmgrade'] = f'A product with {st.session_state.plnscopenumber} features has a grade of {grade}.  The number of actors or personas is {st.session_state.plnactors} increasing actors will increase cost however will improve grade.  Delivery of nice to have features or high quality non-functional attributes will also improve the grade.  The non-functional attributes are {nonfunctlist}' 
      st.success(st.session_state.thepmgrade) 
with st.container():
      st.subheader("Cost Planning")
      with st.expander("Cost Information"):
        st.write("Changes incur costs, and these costs are monitored to ensure that the investment is in line with the value of the change to the business.  Using feature completion, and timelines we calculate cost performance index (CPI) and schedule performance index (SPI) which are indicators if the project is in control. During planning and design, earned value will be 0, when in  execution your earned value will be realized as features are inspected and accepted")
      currchoice = pd.DataFrame({'Item': ['None', 'USD', 'CDN', 'EUR'], 'Value': [0, 1, 2, 3]})
      col4, col5 = st.columns(2)
      with col4:
       selected_cur1 = st.selectbox("Income Currency", currchoice.Item, index=setvalue('pllistincomecurrency'), disabled=disableplan) 
       st.session_state['pllistincomecurrency'] = currchoice.loc[currchoice.Item == selected_cur1]["Value"].iloc[0]
      with col5:
       selected_cur2 = st.selectbox("Expense Currency", currchoice.Item, index=setvalue('pllistexpensecurrency'), disabled=disableplan) 
       st.session_state['pllistexpensecurrency'] = currchoice.loc[currchoice.Item == selected_cur2]["Value"].iloc[0]
      st.slider('Budget', min_value=0, max_value=200000, value=setvalue('plnbudget'), step=5000, key='plnbudget', disabled=disableplan)
      col1, col2, col3, col4, col5 = st.columns(5)
      with col1:
       st.slider('Estimated Work Hours', min_value=0, max_value=2000, value=setvalue('plnhours'), step=10, key='plnhours', disabled=disableplan)
      with col2:
       st.slider('Average Rate', min_value=0, max_value=200, value=setvalue('plnavgrate'), step=5, key='plnavgrate', disabled=disableplan)
      with col4:
       st.slider('Estimate Confidence', min_value=0, max_value=100, value=setvalue('plnhoursconfidence'), step=5, key='plnhoursconficence', disabled=disableplan)
      st.subheader("Cost Monitoring")
      with st.expander("Cost monitoring and control"):
       st.write("During cost monitoring, capture the actual spend, and resource hours or resource usage.") 
      col4, col5 = st.columns(2)
      with col4:
       st.slider('Spend to Date', min_value=0, max_value=250000, value=setvalue('plnspend'), step=500, key='plnspend')
      with col5:
       st.slider('Work Hours Performed', min_value=-1, max_value=st.session_state.plnhours, value=setvalue('plnhoursused'), step=10, key='plnhoursused')
      if st.session_state.plnhours > 1:
       st.session_state['plnestimatecomplete'] =  ( st.session_state.plnhoursused / st.session_state.plnhours ) * 100
      else:
       st.session_state.plnestimatecomplete = 0
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

with st.container():
      st.subheader("Return on Investment")
     #https://www.investopedia.com/articles/basics/10/guide-to-calculating-roi.asp
     #[200~https://www.coface.com/news-economy-and-insights/business-risk-dashboard/country-risk-files/canada
      with st.expander('What is ROI'):
        st.write("Measure the benefits or return on the investment over time based on the benefits, either savings or increased income after release.  Provide the date when new benefits are expected to start, and the number of periods to allocate the investment.  A benefit date before end of project is a sign of agile delivery or iterative delivery to give value in increments, or a maintanance project.  The ROI is a number that is used to measure the value of the investment in this project against other projects in your portfolio. Consider factors like country, gdp, inflation, unemployment, growth,  Business climate, country risk and where the investment money is sourced.")

# https://www.focus-economics.com/countries/spain/
# https://santandertrade.com/en/portal/analyse-markets/spain/economic-political-outline#
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.session_state['plnincreaseincome']  = st.slider ("Benefit Income", value=setvalue('plnincreaseincome'), format="%i", min_value=-100000, max_value=1000000, step=5000, disabled=disableplan )
      with col2:
       st.session_state['plnincreaseexpense']  = st.slider ("New Expenses against Benefits", value=setvalue('plnincreaseexpense'), format="%i", min_value=-100000, max_value=1000000, step=5000 , disabled=disableplan)
      with col3:
       st.session_state['plnbenefitperiod']  = st.slider ("Benefit Period", value=setvalue('plnbenefitperiod'), format="%i", min_value=1, max_value=36, step=1,  help="Enter the number of months you want to spread out this investment", disabled=disableplan )
      with col4:
       st.session_state['pldbenefitdate']  = st.date_input ("Benefit Start Date", value=setvalue('pldbenefitdate'), disabled=disableplan)
      cb12 = st.checkbox("Askme for ROI Information.", disabled=disableplan)
      st.session_state['plproigoal'] = st.text_area("ROI Goal", value=setvalue('plproigoal'), disabled=disableplan)
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

with st.container():
   with st.container():
      st.subheader("Environment and Constraints")
      st.write("What constraints impact time, scope, quality or cost. Little to no flexibility in time, cost or scope is normally a risk but can be a constraint when the probability of risks are almost certain.  Environmental issues are risks that are expected to occur in a project such as weather events, or limits of people and resources, when plans are not clear or finalized they become a constraint.")
      st.write("Describe the approach and authority of the project team to limit impact of issues with Scope, Time, Budget or Resources. Choose a range on the slider related to the impact with 5 highest impact.  Example, if scope changes will have a significant impact on the product or the plan (5 - High) or are scope changes tolerated and have low impact on the plan and project (1 - Low).  ")
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnscoperange']  = st.slider ("Scope Risk", value=setvalue('plnscoperange'), format="%i", min_value=0, max_value=5, step=1,disabled=disableplan  )
      with col2:
       cb7 = st.checkbox("Askme for scope mitigation strategies.", disabled=disableplan)
       st.session_state['plpscopecontingency']  = st.text_area ("What are three ways to mitigate the impact of scope changes in a project?", value=setvalue('plpscopecontingency'),disabled=disableplan)
       if cb7 and len(st.session_state.plpscopecontingency) < 10:
         query = "What are three strategies to reduce the impact of scope changes in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)

      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnschedulerange']  = st.slider ("Schedule Risk", value=setvalue('plnschedulerange'), format="%i", min_value=0, max_value=5, step=1,disabled=disableplan )
      with col2:
       cb8 = st.checkbox("Askme for schedule mitigation strategies.", disabled=disableplan)
       st.session_state['plptimecontingency']  = st.text_area ("Schedule Contingency?", value=setvalue('plptimecontingency'), disabled=disableplan)
       if cb8 and len(st.session_state.plptimecontingency) < 10:
         query = "What are three strategies to reduce the impact of schedule issues in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnbudgetrange']  = st.slider ("Budget Risk", value=setvalue('plnbudgetrange'), format="%i", min_value=0, max_value=5, step=1,disabled=disableplan )
      with col2:
       cb9 = st.checkbox("Askme for budget mitigation strategies.", disabled=disableplan)
       st.session_state['plpbudgetcontingency']  = st.text_area ("Budget Contingency", value=setvalue('plpbudgetcontingency'),disabled=disableplan)
       if cb9 and len(st.session_state.plpbudgetcontingency) < 10:
         query = "What are three strategies to reduce the impact of cost overruns in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnteamrange']  = st.slider ("Team Risk", value=setvalue('plnteamrange'), format="%i", min_value=0, max_value=5, step=1,disabled=disableplan )
      with col2:
       cb10 = st.checkbox("Askme for team mitigation strategies", disabled=disableplan)
       st.session_state['plpteamcontingency']  = st.text_area ("Team Contingency", value=setvalue('plpteamcontingency'),disabled=disableplan)
       if cb10 and len(st.session_state.plpteamcontingency) < 10:
         query = "What are three strategies to reduce the impact of low performing teams in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query, "The response is provided below, paste and edit in the form above")
         message = chatbot.query(query)
         st.code(message)
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnresourcerange']  = st.slider ("Resource Risk", value=setvalue('plnresourcerange'), format="%i", min_value=0, max_value=5, step=1,disabled=disableplan )
      with col2:
       cb11 = st.checkbox("Askme for resource or technology mitigation strategies", disabled=disableplan)
       st.session_state['plpresourcecontingency']  = st.text_area ("Resource Contingency", value=setvalue('plpresourcecontingency'),disabled=disableplan)
       if cb11 and len(st.session_state.plpresourcecontingency) < 10:
         query = "What are three strategies to reduce the impact of resource or technology challenges in a " + st.session_state.plpname + " project?"
         info = chatbot.get_conversation_info()
         st.write("Asking AI for a response", cb2, info.id, info.title, info.model, info.system_prompt, query)
         message = chatbot.query(query)
         st.code(message)
      thepmcontingencysummary = "The project contingency plans include Scope: " + st.session_state['plpscopecontingency']+ " Schedule: " + st.session_state['plptimecontingency'] + " Budget:  " + st.session_state['plpbudgetcontingency'] + " and Resource:  " + st.session_state['plpresourcecontingency']
      st.markdown("{}".format(thepmcontingencysummary), unsafe_allow_html=True)

      st.session_state['thepmteam'] = f'The team is composed of {st.session_state.plnteam:.0f}  members and have collaborated together for {st.session_state.plnteamweeks:.0f} weeks.  \n\n   The solution architect is {st.session_state.plpsolutionname}. The Operations Lead is {st.session_state.plpoperationname}. The inspector is {st.session_state.plpinspectorname}.  There are currently {st.session_state.plnopenroles:.0f} open roles. '

with st.container():
    placeholder = st.empty()
    #textquestion = st.text_input ("Ask AI for general help, enter a question", key="textquestion", on_change=clearaskme)
    #st.button('askmeforhelp', key='askmeforhelp')  
    #chatbot.change_conversation(id)
    #if  len(textquestion) > 20:
    #  message = chatbot.query(textquestion)
    #  st.write(textquestion)
    #  st.code(message)

with st.container():
   with st.expander("Risk Trigger settings"):
     st.write("Risk trigger default values.  Currently these are for information purposes only and cannot be changed in the application.  ")
     risktriggers = {'Inflation': 10, 'Changes': 1, 'Earned Value': 0, 'Sentiment': 70, 'Engagement': 80, 
        'CPI': 0,
        'SPI': 0, 'Inspection': 3, 'ROI': 120, 'Late Start': 3, 'Climate': 1, 'Unemployment': 8, 'Business Climate': 'B',
        'Country Risk': 'B' }
     st.dataframe(risktriggers)

with st.container():

# 1. Download Settings Button convert dataframe to list there is a pandas problem with data serialization set to legacy
  dataitems = st.session_state.items()
  datalist = list(dataitems)
  df = pd.DataFrame(datalist)
  csv = df.to_csv().encode('utf-8')
  settings_to_download = {k: v for k, v in datalist if "button" not in k and "file_uploader" not in k}
  st.write("Save Plan to save a copy of the form. Save often")
  pmid="CS1"
  today = date.today()
  reportdate = today.strftime("%b-%d-%Y")
  pmfile_name = "thepmmonitorplan_" + pmid + "_" + reportdate + ".csv"
  button_download = st.download_button(label="Save Plan",
                                           data=csv,
                                           file_name=pmfile_name,
                                           help="Click to Download Current Settings")

