import streamlit as st
from PIL import Image
import pathlib
from math import log
from datetime import datetime 
from datetime import timedelta, date
import pandas as pd
from utilities import currencyrisk, evreport, plancomment, get_table_download_link, datedifferences
from annotated_text import annotated_text
import altair as alt
from st_aggrid import AgGrid
import io
import base64

# 3. Apply Settings
def upload_saved_settings(saved_settings):
        #st.write(saved_settings)
        """Set session state values to what specified in the saved_settings."""
        for i in range(len(saved_settings)):
          if isinstance(saved_settings.iloc[i, 2],type(str)):
            # st.write(st.session_state[saved_settings.iloc[i, 1]])
            if saved_settings.iloc[i, 1].startswith('plp'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
            if saved_settings.iloc[i, 1].startswith('pls'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
            if saved_settings.iloc[i, 1].startswith('pln'):
              st.session_state[saved_settings.iloc[i, 1]] = int(saved_settings.iloc[i, 2])
            if saved_settings.iloc[i, 1].startswith('plrlist'):
              st.session_state[saved_settings.iloc[i, 1]] = int(saved_settings.iloc[i, 2])
            if saved_settings.iloc[i, 1].startswith('pllist'):
              st.session_state[saved_settings.iloc[i, 1]] = int(saved_settings.iloc[i, 2])
            if saved_settings.iloc[i, 1].startswith('plmlist'):
              string_without_brackets = saved_settings.iloc[i, 2].strip("[]")
              string_without_brackets = string_without_brackets.replace("'", "")
              string_list = string_without_brackets.split(", ")
              for x in string_list:
               if x != "":
                 if x not in st.session_state[saved_settings.iloc[i, 1]]:  # prevent duplicates
                    st.session_state[saved_settings.iloc[i, 1]].append(x)
            if saved_settings.iloc[i, 1].startswith('pld'):
              datetime1 = saved_settings.iloc[i, 2]
              datetime2 = datetime.strptime(datetime1, '%Y-%m-%d').date()
              st.session_state[saved_settings.iloc[i, 1]] = datetime2
        return

def setvalue(var):
    if var.startswith('pllist'):
        if var in st.session_state:
          if st.session_state[var] == "":
           return 0
          else:
           return int(st.session_state[var])
           #return int(st.session_state[var])-1
        else:
         return 0
    if var.startswith('pld'):
       return st.session_state[var] if var in st.session_state else date.today()
    else:
       if var.startswith('pln'):
          return int(st.session_state[var]) if var in st.session_state else 0
       else:
          return st.session_state[var] if var in st.session_state else "None"

def clear_form():
  for key in st.session_state.keys():
    del st.session_state[key]
#@st.cache

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Plan",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

st.markdown("<h3 style='text-align: center; color: white; background: grey;'>The PM Monitor</h3>", unsafe_allow_html=True)

tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tabr = st.tabs(["Start", "Info", "Scope", "Cost", "Schedule", "Communication", "Quality", "Constraints", "ROI", "Save", "Restore"])
with st.form(key="pmmonitorplan", clear_on_submit=False):

     ##  Introduction to Planning
     with tab0:
      st.subheader("How to Create a Plan")
     
      st.write("Meet with stakeholders, gather information, identify and document the goal, deliverables, and budget.  Create a schedule.  Identify the resources and constraints. Create an activity plan and validate the resources with the plan.   Review the risks and plan contingency. Moving one tab at a time, fill in the information, click update and check the summary.  Fill in all information, then publish and share the canvas, the poster for the team.  ")

      st.subheader("How to Update and Run Stoplight Report")
      st.write("Restore your plan from backup.  Update Cost, spend to date, and work hours performed.  Update project phase if needed.   Were there scope changes this period?  In schedule, note if milestone delivery dates are changing.  Has the team changed?  What is the active member and engagement score for the period? Was there a quality report.  Create your brief video/audio report and save.  Following these questions, save and go to the Stoplight report.  ")
     ##  The basic intro information 
     with tab1:
      st.subheader("Project Information")
      st.write("A project is finite, has a start and and end timeframe and is unique. A project is undertaken to reach a goal, implement change, deliver a new product, service or process.  The Project Plan outlines the timeline and the benefits, scope and contingency plans.  The plan provides the necessary information for the project manager and The PM Monitor to report on the progress of the project, manage risks and identify issues.")
      col4, col5 = st.columns(2)
      with col4:
       st.session_state['plpnumber']  = st.text_input ("Project ID", max_chars=10, value=setvalue('plpnumber'), help="A unique id to identify this project")
      with col5:
       st.session_state['plpname']  = st.text_input ("Project Name", help="A short project name for reports", max_chars=50, value=setvalue('plpname'))
      col4, col5 = st.columns(2)
      with col4:
       st.session_state['plpmname'] = st.text_input ("Project Manager Name", max_chars=30, value=setvalue('plpmname'))
      with col5:
       st.session_state['plspname']  = st.text_input ("Product Owner or Sponsor Name", max_chars=30, value=setvalue('plspname'))
      st.session_state['plspurpose']  = st.text_area ("What is the purpose?", value=setvalue('plspurpose'))
      st.session_state['plsbenefits']  = st.text_area ("What are the benefits?", value=setvalue('plsbenefits'))
      st.session_state['plsbenchmarks']  = st.text_area ("Are there comparable benchmarks or services?", value=setvalue('plsbenchmarks'))

     # set some dates
      week  = timedelta(days = 7)
      daytoday = date.today()
     
      col1, col2, col3 = st.columns(3)
      with col1:
       st.session_state['pldstartdate']  = st.date_input ("Start Date", setvalue('pldstartdate'))
      with col2:
       st.session_state['pldenddate']  = st.date_input ("End Date", setvalue('pldenddate'))
      with col3:
       st.session_state['pldcharterdate']  = st.date_input ("Report Date", setvalue('pldcharterdate'))

     # how much time to end of plan
      daystoend = (st.session_state['pldenddate']-st.session_state['pldstartdate']).days
      daystoday = (daytoday-st.session_state['pldstartdate']).days
      weeksinplan = int(daystoend/7)
      st.session_state['thepmtimecomplete'] = 0
      if daystoend > 0:
        st.session_state['thepmtimecomplete'] = int(daystoday / daystoend * 100)

      col6, col7, col8 = st.columns([1,1,3])
      with col6:
       st.session_state['plncadence'] = st.slider('Cadence', min_value=0, max_value=12, value=setvalue('plncadence'), help="Cadence is the frequency that the project replans and reports on progress.  In a maintenance project you should plan and report quarterly.  In active development projects when investment is higher, you should be planning and reporting weekly")
      with col7:
       phasechoice = {"None", "Initiation", "Planning", "Execution", "Launch and Training", "Closure"}
       phaselist = ["None", "Initiation", "Planning", "Execution", "Launch and Training", "Closure"]
       st.session_state['plnlistphase'] = st.slider('Project Phase', min_value=0, max_value=5, help="The phase of the project will determine which risks are higher or may be closed.  In the early phases of the project you have higher technology and cost risks and in later phases you can have engagement and resource risks. A project has 5 phases, 1 initiation, 2 planning, 3 execution, 4 monitor and review, 5 closure", value=setvalue('plnlistphase'))
       st.session_state['thepmphase'] = phaselist[int(st.session_state['plnlistphase'])]
      with col8:
       classchoice = pd.DataFrame({'Item': ['None', 'Software Build', 'Software Design', 'Brand Marketing', 'Process Automation', 'Scheduled Maintenance', 'Content Migration'], 'Value': [0, 1, 2, 3, 4, 5, 6]})
       selected_class = st.selectbox("Project Classification", classchoice.Item, index=setvalue('pllisttype'), help="The type of project will be used to determine risks, a physical build can be impacted by weather.  Changes to procedures or pipelines require more focus on communication activities")
       st.session_state['pllisttype'] = classchoice.loc[classchoice.Item == selected_class]["Value"].iloc[0]

     ##  output information and create header block
       st.session_state['thepmplannote'] = plancomment(st.session_state['pldstartdate'], st.session_state['pldenddate'], daystoday, daystoend, st.session_state['thepmtimecomplete'], 3, st.session_state['plpnumber'], st.session_state['plpname'], st.session_state['plsbenefits'], st.session_state['plncadence'], st.session_state['thepmphase'], st.session_state['plpmname'], selected_class)
      st.success(st.session_state['thepmplannote'])

     ndays = st.session_state['plncadence']*7
     st.session_state['thepmheader'] = pd.DataFrame({
       "Project": [st.session_state.plpname, st.session_state.plpmname],
       "Sponsor": [st.session_state.plpnumber, st.session_state.plspname],
       "Phase": [st.session_state.thepmphase, st.session_state.pldcharterdate]
      })

     #  Scope section 
     with tab2:
      st.subheader("Scope")
      st.write("The scope information outlines the features that the product should have. Scope also clarifies what is not planned and what may be negotiable")
      col4, col5 = st.columns(2)
      with col4:
       st.session_state['plscopemusthave']  = st.text_area ("Must Have", value=setvalue('plscopemusthave'))
      with col5:
       st.session_state['plscopenicetohave']  = st.text_area ("Nice to Have", value=setvalue('plscopenicetohave'))
      col4, col5 = st.columns(2)
      with col4:
       st.session_state['plscopeifpossible']  = st.text_area ("If Possible", value=setvalue('plscopeifpossible'))
      with col5:
       st.session_state['plscopeoutofscope']  = st.text_area ("Out of Scope", value=setvalue('plscopeoutofscope'))
      with col4:
       st.session_state['plscopechangeadd']  = st.text_area ("Scope Additions", value=setvalue('plscopechangeadd'))
      with col5:
       st.session_state['plscopechangedel']  = st.text_area ("Scope Removal", value=setvalue('plscopechangedel'))
      with col4:
       st.session_state['plmlistscopelist'] = st.multiselect(
         'Select non functional attributes',
         ['Security', 'Availability', 'Usability', 'Maintainability','Documentation', 'Accessibility', 'Compliance', 'Robustness', 'Reliablity', 'Performance', 'Localization', 'Compatiblity', 'Portability', 'Scalability', 'None'],
         default=setvalue('plmlistscopelist'))
      with col5:
       st.session_state['plmlistscopeoption'] = st.multiselect(
         'Select technical architecture attributes or resources',
         ['CMS', 'Web Framework', 'SEO', 'Search', 'Cloud Hosting', 'Automation',  'ERP', 'CDN', 'CI/CD', 'Custom Theme', 'No Code', 'Native Mobile App', 'Process Model', 'Database', 'Testing', 'None'], default=setvalue('plmlistscopeoption'))
      scopechange = ""
      if len(st.session_state['plscopechangeadd']) > 5 or len(st.session_state['plscopechangedel']) > 5:
         st.session_state['thepmcopechanged'] = True
         scopechange = f'There are scope changes. {st.session_state.plscopechangeadd} {st.session_state.plscopechangedel}'
      else:
         st.session_state['thepmcopechanged'] = False
      st.session_state['thepmplanscope'] = f'{st.session_state.plscopenicetohave} {st.session_state.plscopeifpossible} {st.session_state.plscopemusthave} {st.session_state.plscopeoutofscope} {scopechange}'
      st.success(st.session_state['thepmplanscope'])
     ##  Schedule
     milestonestatus = {0: "Not started", 1: "In Progress", 2: "On Hold", 3: "Complete"}
     with tab4:
      st.subheader("Schedule")
      st.write("Our plan is managed and controlled by the defined milestones.  Your project should have no less than 5 milestones however you can define more. Milestones are point in time events that are used to verify if the project is on track.  Releases completed result in business value to the users and customer.  Features are decomposed into unique stories, stories are SMART,  Specific, Measurable, Achievable, Realistic and have a time frame. ")
      dfm = pd.DataFrame()
      sdate = st.session_state['pldstartdate']
      #[sdate+timedelta(days=x) for x in range((edate-sdate).days)]
      if st.session_state['plncadence'] > 0:
       reportsinplan = int(weeksinplan/st.session_state['plncadence'])
      else:
       reportsinplan = 1

      for i in range(1, reportsinplan + 1):
         ldays = ndays*i
         data = {'Milestone': 'Baseline', 'reportdate': sdate+timedelta(days=ldays), 'plandate': sdate+timedelta(days=ldays)}
         #dfm.loc[len(dfm.index)] = data
         dfm = dfm.append(data, ignore_index=True)

      milestones_file = st.file_uploader("own milestones",type=['csv'])
      if milestones_file is not None:
       dfmilestone = pd.read_csv(milestones_file, parse_dates=['reportdate','plandate'])
      else:
       dfmilestone = pd.read_csv(r'milestones.csv', parse_dates=['reportdate','plandate'])
      for index, row in dfmilestone.iterrows():
         xdays = int((row['MSStart']+1)*7*st.session_state['plncadence'])
         str = row['MSDisplace']
         #  set the end point on baseline (eg. 2,2)
         data = {'Milestone': row['Milestone'], 'reportdate': sdate+timedelta(days=xdays), 'plandate': sdate+timedelta(days=xdays)}
         dfm = dfm.append(data, ignore_index=True)
         #split string
         splits = str.split(";")
         #for loop to iterate over words array
         for i in range(1, len(splits)):
           xsplit=int(splits[i-1])
           ndays = xdays + (xsplit*7*st.session_state['plncadence'])
           vdays=int(i*7*st.session_state['plncadence'])
           data = {'Milestone': row['Milestone'], 'reportdate': sdate+timedelta(days=vdays), 'plandate': sdate+timedelta(days=ndays)}
           dfm = dfm.append(data, ignore_index=True)
      dfresponse = AgGrid(dfmilestone, height=200, theme='streamlit', editable=True, fit_columns_on_grid_load=True)
      chart = alt.Chart(dfm).mark_line(point = True).encode(
          alt.X('monthdate(reportdate):O', title='Report Date'),
          alt.Y('monthdate(plandate):O', title='Plan Date', scale=alt.Scale(reverse=True)),
          color="Milestone", text="Milestone")
      st.altair_chart(chart, use_container_width=True)
      st.session_state['thepmmilestones'] = dfmilestone[dfmilestone['Status'] == "Planned"]['Description'].to_string()

     with tab5:
      st.subheader("Communication")
      st.write("Projects are executed and implemented by people, the team, the stakeholders and are implemented to provide benefit to users or customers.  The communication plan outlines the needs of the stakeholders, team and users. The complexity maintaining good communication and establishing trust between the team and the stakeholders is a factor of the size of the team, and how long they have been working together.  Trust is earned, not given, and as trust increases, performance will improve and quality will follow.  Typically engagement and team sentiment is high at the beginning of the project and decreases over time, and engagement of the stakeholders follows the opposite pattern  ")
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.session_state['plnstakeholder']  = st.slider ("Number of Stakeholders", value=setvalue('plnstakeholder'), format="%i", min_value=0, max_value=10, step=1 )
      with col2:
       st.session_state['plnteam']  = st.slider ("Number of Core Team Members", value=setvalue('plnteam'), format="%i", min_value=0, max_value=15, step=1)
      with col3:
       st.session_state['plnusers']  = st.slider ("Number of Users", value=setvalue('plnusers'), format="%i", min_value=0, max_value=100000, step=10000)
      with col4:
       st.session_state['plnactors']  = st.slider ("Number of Actors", value=setvalue('plnactors'), format="%i", min_value=0, max_value=10, step=1)
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.session_state['plnteamweeks']  = st.slider ("Weeks with Full Team", value=setvalue('plnteamweeks'), format="%i", min_value=0, max_value=12, step=1 )
      with col2:
       st.session_state['plnopenroles']  = st.slider ("Number of Open Roles", value=setvalue('plnopenroles'), format="%i", min_value=0, max_value=15, step=1)
      with col3:
       st.session_state['plpactivitylink']  = st.text_input ("Activity Source Link (URL)", value=setvalue('plpactivitylink') )
      with col4:
       st.session_state['plpstanduplink']  = st.text_input ("Standup Async Link (URL)" , value=setvalue('plpstanduplink'))
      with col1:
       st.session_state['plpsolutionname'] = st.text_input ("Solution Architect Name", max_chars=30, value=setvalue('plpsolutionname'))
      with col2:
       st.session_state['plpoperationname'] = st.text_input ("Operations Lead Name", max_chars=30, value=setvalue('plpoperationname'))
      with col3:
       st.session_state['plpinspectorname'] = st.text_input ("Inspection Lead Name", max_chars=30, value=setvalue('plpinspectorname'))
      with col4:
       st.session_state['plpaccountname'] = st.text_input ("Account Manager Name", max_chars=30, value=setvalue('plpaccountname'))
      with col1:
       st.session_state['plpmcustname'] = st.text_input ("Customer Project Manager Name", max_chars=30, value=setvalue('plpmcustname'))
      st.write("---")
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       # SAM = (Active Channel Members/ Total Channel Members)
       st.session_state['plnactivesam']  = st.slider ("Active Member Score", value=setvalue('plnactivesam'), format="%i", min_value=0, max_value=100, step=5 )
      with col2:
        #SES = ((Unique Commenters + Unique Reactors) / 2) / (Active Channel Members)
        #SES Simplified = (Average Active Members) / (Active Channel Members)
       st.session_state['plnactiveses']  = st.slider ("Active Engagement Score", value=setvalue('plnactiveses'), format="%i", min_value=0, max_value=100, step=5 )
      planchannels = (int(st.session_state['plnstakeholder']) + int(st.session_state['plnteam'])) * (int(st.session_state['plnstakeholder']) + int(st.session_state['plnteam']) - 1)
      with col3:
       st.session_state['plpmreport'] = st.text_input ("PM report (youtube)", value=setvalue('plpmreport'))
      with col4:
       st.session_state['plpmid'] = st.text_input ("PM report ID", value=setvalue('plpmid'))
      plancommunication = f' There are {planchannels:.0f} communication channels. The team has a message formum at {st.session_state.plpstanduplink} and a task activity board at {st.session_state.plpactivitylink}'
      st.session_state['thepmteam'] = f'The team is composed of {st.session_state.plnteam:.0f}  members and have collaborated together for {st.session_state.plnteamweeks:.0f} weeks.  The solution architect is {st.session_state.plpsolutionname}. The Operations Lead is {st.session_state.plpoperationname}. '
      st.markdown('##') 
      st.success(st.session_state['thepmteam'])
      st.success(plancommunication)

     with tab6:
      st.subheader("Quality")
      st.session_state['plsqualitygoal']  = st.text_input ("Describe Quality Goal", value=setvalue('plsqualitygoal'))
      col1, col2, col3, col4, col5 = st.columns(5)
      with col1:
       st.session_state['plntests']  = st.slider ("Number of Tests", value=setvalue('plntests'), format="%i", min_value=0, max_value=100, step=1 )
      with col2:
       st.session_state['plntestsrun']  = st.slider ("Number of Tests Run", value=setvalue('plntestsrun'), format="%i", min_value=0, max_value=100, step=1 )
      with col3:
       st.session_state['plntestsfailed']  = st.slider ("Number of Tests Failed", value=setvalue('plntestsfailed'), format="%i", min_value=0, max_value=100, step=1 )
      with col4:
       st.session_state['plntestscritical']  = st.slider ("Number Critical Failed", value=setvalue('plntestscritical'), format="%i", min_value=0, max_value=100, step=1 )
      with col5:
       st.session_state['pldinspectdate']  = st.date_input ("Inspection Report Date", setvalue('pldinspectdate'))

     #  test results, test not done, test run less than tolerance of 70% test failed more than 20 or critical test failed is positive
       st.session_state['thepminspectionwarning'] = "Inspection planned or passed." 
       st.session_state['thepminspectionflag'] = 0 
      if st.session_state['plntests'] == 0 or st.session_state['plntestscritical'] > 0 or (st.session_state['plntestsrun'] == 0 and st.session_state['pldinspectdate'] < daytoday ):
        st.session_state['thepminspectionwarning'] = "Inspection plan missing or failed." 
        st.session_state['thepminspectionflag'] = 1 
      planquality = f'There are {st.session_state.plntests:.0f}  tests planned. '
      passfail = 0
      passcoverage = 0
      if int(st.session_state['plntests']) > 0:
        passfail = int(st.session_state['plntestsfailed'] / st.session_state['plntests'] * 100) 
        passcoverage = int(st.session_state['plntestsrun'] / st.session_state['plntests'] * 100) 
      st.session_state['thepmquality'] = f'{planquality} {st.session_state.plnteam}  members and have collaborated together for {st.session_state.plnteamweeks}  weeks. The inspector team/name is {st.session_state.plpinspectorname}.  The inspection report is planned on {st.session_state.pldinspectdate.strftime("%Y-%m-%d")}  Pass to fail rate is {passfail:.0f}%. Test coverage is {passcoverage}%. ' 
      st.markdown('##') 
      st.success(st.session_state['thepmquality'])
      st.success(st.session_state['thepminspectionwarning'])

     with tab3:
      st.subheader("Cost")
      st.write("Changes incur costs, and these costs are monitored to ensure that the investment is in line with the value of the change to the business.  Using release completion, and timelines we calculate cost performance index (CPI) and schedule performance index (SPI) which are indicators if the project is in control. During conception and planning, earned value will be 0, when you start execution your earned value will be realized as releases are implemented")
      currchoice = pd.DataFrame({'Item': ['None', 'USD', 'CDN', 'EUR'], 'Value': [0, 1, 2, 3]})
      col4, col5 = st.columns(2)
      with col4:
       selected_cur1 = st.selectbox("Income Currency", currchoice.Item, index=setvalue('pllistincomecurrency')) 
       st.session_state['pllistincomecurrency'] = currchoice.loc[currchoice.Item == selected_cur1]["Value"].iloc[0]
      with col5:
       selected_cur2 = st.selectbox("Expense Currency", currchoice.Item, index=setvalue('pllistexpensecurrency')) 
       st.session_state['pllistexpensecurrency'] = currchoice.loc[currchoice.Item == selected_cur2]["Value"].iloc[0]
      st.session_state['plnbudget'] = st.slider('Budget', min_value=0, max_value=200000, value=setvalue('plnbudget'), step=5000)
      st.session_state['plnspend'] = st.slider('Spend to Date', min_value=0, max_value=250000, value=setvalue('plnspend'), step=500)
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.session_state['plnhours'] = st.slider('Estimated Work Hours', min_value=0, max_value=2000, value=setvalue('plnhours'), step=10)
      with col2:
       st.session_state['plnavgrate'] = st.slider('Average Rate', min_value=0, max_value=200, value=setvalue('plnavgrate'), step=5)
      with col3:
       st.session_state['plnhoursused'] = st.slider('Work Hours Performed', min_value=0, max_value=2000, value=setvalue('plnhoursused'), step=10)
      with col4:
       st.session_state['plnhoursconfidence'] = st.slider('Estimate Confidence', min_value=0, max_value=100, value=setvalue('plnhoursconfidence'), step=5)
      plbudget = st.session_state['plnbudget'] + (st.session_state['plnhours'] * st.session_state['plnavgrate'])
      plspend = st.session_state['plnspend'] + (st.session_state['plnhoursused'] * st.session_state['plnavgrate'])
      mcomplete = len(dfmilestone[dfmilestone.Status == 'Complete'])
      mplanned = len(dfmilestone.index)
      st.session_state['thepmdelivery'] = int (mcomplete / mplanned * 100)
      (evsummary, st.session_state['thepmcpi'], st.session_state['thepmspi'], etc)  = evreport((plbudget + (plbudget *.3)), plbudget, st.session_state['plnhours'], st.session_state['plnavgrate'], "EUR" , st.session_state['pldstartdate'], st.session_state['pldenddate'], plspend, mplanned, mcomplete, daystoend, daystoday, st.session_state['thepmtimecomplete'])
      st.session_state['thepmbudgetcomplete'] = 0
      if plbudget > 0:
        st.session_state['thepmbudgetcomplete'] = int(plspend / plbudget * 100)
      st.markdown("{}".format(evsummary), unsafe_allow_html=True)


     with tab8:
      st.subheader("Return on Investment")
     #https://www.investopedia.com/articles/basics/10/guide-to-calculating-roi.asp
      st.write("Measure the benefits or return on the investment over time based on the benefits, either savings or increased income after release.  Provide the date when new benefits are expected to start, and the number of periods to allocate the investment.  A benefit date before end of project is a sign of agile delivery or iterative delivery to give value in increments, or a maintanance project")
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.session_state['plnincreaseincome']  = st.slider ("Benefit Income", value=setvalue('plnincreaseincome'), format="%i", min_value=-100000, max_value=1000000, step=5000 )
      with col2:
       st.session_state['plnincreaseexpense']  = st.slider ("Benefit Expense", value=setvalue('plnincreaseexpense'), format="%i", min_value=-100000, max_value=1000000, step=5000 )
      with col3:
       st.session_state['plnbenefitperiod']  = st.slider ("Benefit Period", value=setvalue('plnbenefitperiod'), format="%i", min_value=1, max_value=36, step=1 )
      with col4:
       st.session_state['pldbenefitdate']  = st.date_input ("Benefit Start Date", value=setvalue('pldbenefitdate'))
      benefitdelta = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'])
      roi = 0
      rateofreturn = 0
      benefitdate = st.session_state['pldbenefitdate']
      if plbudget > 0:
        roi = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'] - plbudget) / (plbudget + etc) * 100
        rateofreturn = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'] - (plbudget + etc)) / (plbudget + etc)
     # annualroi = (1 + rateofreturn) ^ (1 / st.session_state['plnbenefitdate']) - 1
     # st.write(annualroi)
      roisummary = f'The roi is {roi:.3f} with an investment of {plbudget:.0f} and a benefit of {benefitdelta:.0f} to begin {benefitdate :%B %d, %Y} '
      st.write(roisummary)

     with tab7:
      st.subheader("Environment and Constraints")
      st.write("What constraints impact time, scope, quality or cost. Little to no flexibility in time, cost or scope is normally a risk but can be a constraint when the probability of risks are almost certain.  Environmental issues are risks that are expected to occur in a project such as weather events, or limits of people and resources, when plans are not clear or finalized they become a constraint. Describe the approach to limit impact of issues with Scope, Time, Budget or Resources, and choose a range on the slider related to amount of risk (5 highest) ")
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnscoperange']  = st.slider ("Scope Risk", value=setvalue('plnscoperange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       st.session_state['plpscopecontingency']  = st.text_area ("Scope Contingency", value=setvalue('plpscopecontingency'))
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnschedulerange']  = st.slider ("Schedule Risk", value=setvalue('plnschedulerange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       st.session_state['plptimecontingency']  = st.text_area ("Schedule Contingency", value=setvalue('plptimecontingency'))
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnbudgetrange']  = st.slider ("Budget Risk", value=setvalue('plnbudgetrange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       st.session_state['plpbudgetcontingency']  = st.text_area ("Budget Contingency", value=setvalue('plpbudgetcontingency'))
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnteamrange']  = st.slider ("Team Risk", value=setvalue('plnteamrange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       st.session_state['plpteamcontingency']  = st.text_area ("Team Contingency", value=setvalue('plpteamcontingency'))
      col1, col2 = st.columns([1,5])
      with col1:
       st.session_state['plnresourcerange']  = st.slider ("Resource Risk", value=setvalue('plnresourcerange'), format="%i", min_value=0, max_value=5, step=1 )
      with col2:
       st.session_state['plpresourcecontingency']  = st.text_area ("Resource Contingency", value=setvalue('plpresourcecontingency'))
      thepmcontingencysummary = "The project contingency plans include Scope: " + st.session_state['plpscopecontingency']+ " Schedule: " + st.session_state['plptimecontingency'] + " Budget:  " + st.session_state['plpbudgetcontingency'] + " and Resource:  " + st.session_state['plpresourcecontingency']
      st.markdown("{}".format(thepmcontingencysummary), unsafe_allow_html=True)

     with tab9:
      st.write("save and export plan")
     #  the buttons to validate and save information
     col1, col2, col3 = st.columns(3)
     with col1:
       submit = st.form_submit_button("Update Plan")
     if submit:
       st.info("The information was updated, thank you for using the PM Monitor.  Use Save Plan to save a copy of your plan offline.  Go to Canvas or Stoplight reports")
     with col2:
       clear = st.form_submit_button("Clear Plan", on_click=clear_form)
     if clear:
      clear_form()
      st.info("The information was cleared, thank you for using the PM Monitor.  Use Save Plan to save a copy of your plan offline")

with tabr:
 # 1. Download Settings Button convert dataframe to list
 dataitems = st.session_state.items()
 datalist = list(dataitems)
 df = pd.DataFrame(datalist)
 csv = df.to_csv().encode('utf-8')
 col1, col2, col3, col4 = st.columns([1, 1, 3, 3])
#settings_to_download = {k: v for k, v in st.session_state.items()
 settings_to_download = {k: v for k, v in datalist if "button" not in k and "file_uploader" not in k}

    # 2. Select Settings to be uploaded
 with col3:
  uploaded_file = st.file_uploader(label="Select a Plan to be uploaded",
                                     help="Select the Plan File (Downloaded in a previous run) that you want"
                                          " to be uploaded and then applied (by clicking 'Apply Plan' above)")
 with col4:
  if uploaded_file is not None:
         uploaded_settings = pd.read_csv(uploaded_file)
  else:
        uploaded_settings = settings_to_download
        st.warning("**WARNING**: Select the Plan File to be uploaded")

 button_apply_settings = col2.button(label="Apply Plan",
                                        on_click=upload_saved_settings,
                                        args=(uploaded_settings,),
                                        help="Click to Apply the Plan of the Uploaded file.\\\n"
                                             "Please start by uploading a Plan File below")
 pmid="CS1"
 reportdate="12-01-2022"
 pmfile_name = "pmmonitorsettings_" + pmid + "_" + reportdate + ".csv"
 button_download = col1.download_button(label="Save Plan",
                                           data=csv,
                                           file_name=pmfile_name,
                                           help="Click to Download Current Settings")
 with open("milestones.csv", "rb") as file:
         milestonebtn = st.download_button(
         label="Download Milestone as CSV",
         data=file,
         file_name='miletstones.csv',
         mime='text/csv',
      )
