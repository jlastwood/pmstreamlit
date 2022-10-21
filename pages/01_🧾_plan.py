import streamlit as st
import pathlib
from datetime import datetime, timedelta, date
import pandas as pd
from utilities import currencyrisk, evreport, plancomment, get_table_download_link, datedifferences
#from st_radial import st_radial

def setvalue(var):
    if var == 'pllistphase':
        return st.session_state[var] if var in st.session_state else 1
    if var == 'pllisttype':
        return st.session_state[var] if var in st.session_state else 1
    if var.startswith('pld'):
       return st.session_state[var] if var in st.session_state else date.today()
    else:
       if var.startswith('pln'):
          return st.session_state[var] if var in st.session_state else 0
       else:
          return st.session_state[var] if var in st.session_state else "None"

def clear_form():
  #  st.session_state['plscopenicetohave'] = "none"
  # caching.clear_cache()
  for key in st.session_state.keys():
    del st.session_state[key]
  #vars = ['plnumber', 'plpname', 'plpmname', 'plsbenefits']
  #for _ in vars:
  #  if _ in st.session_state:
  #      st.session_state[_] = 'none'

#@st.cache
#ast.shared.components.title_awesome("Charter")
    # with st.spinner("Loading  ..."):

with st.form(key="pmmonitorplan", clear_on_submit=False):

     st.markdown("<h3 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     my_expander0 = st.expander("A project is finite, has a start and and end timeframe and is unique. A project is undertaken to reach a goal, implement change, deliver a new product, service or process.  The Project Charter outlines the timeline and the benefits, scope and contingency plans.  The plan provides the necessary information for the project manager and The PM Monitor to control and report on the progress of the project.", expanded=True)
     with my_expander0:
      col4, col5 = st.columns(2)
      with col4:
       st.session_state['plnumber']  = st.text_input ("Project ID", max_chars=10, value=setvalue('plnumber'), help="A unique id to identify this project")
      with col5:
       st.session_state['plpname']  = st.text_input ("Project Name", help="A short project name for reports", max_chars=50, value=setvalue('plpname'))
      col4, col5 = st.columns(2)
      with col4:
       st.session_state['plpmname'] = st.text_input ("Project Manager Name", max_chars=30, value=setvalue('plpmname'))
      with col5:
       st.session_state['plspname']  = st.text_input ("Product Owner or Sponsor Name", max_chars=30, value=setvalue('plspname'))
      st.session_state['plsbenefits']  = st.text_input ("What are the Benefits?", value=setvalue('plsbenefits'))
      col6, col7 = st.columns([3,1])
      with col6:
       st.session_state['plpmreport'] = st.text_input ("PM report (youtube)", value=setvalue('plpmreport'))
      with col7:
       st.session_state['plpmid'] = st.text_input ("PM report ID", value=setvalue('pmpmid'))
     # set some dates
      week  = timedelta(days = 7)
      daytoday = date.today()
     
      col1, col2, col3 = st.columns(3)
      with col1:
       st.session_state['pldstartdate']  = st.date_input ("Start Date", setvalue('pldstartdate'))
      with col2:
       st.session_state['pldenddate']  = st.date_input ("End Date", setvalue('pldenddate'))
      with col3:
       st.session_state['pldcharterdate']  = st.date_input ("Charter Date", setvalue('pldcharterdate'))

      daystoend = (st.session_state['pldenddate']-st.session_state['pldstartdate']).days
      daystoday = (daytoday-st.session_state['pldstartdate']).days
      st.session_state['thepmtimecomplete'] = 0
      if daystoend > 0:
        st.session_state['thepmtimecomplete'] = int(daystoday / daystoend * 100)

      col6, col7, col8 = st.columns(3)
      with col6:
       st.session_state['plncadence'] = st.slider('Cadence', min_value=0, max_value=12, value=setvalue('plncadence'), help="Cadence is the frequency that the project replans and reports on progress.  In a maintenance project you should plan and report quarterly.  In active development projects when investment is higher, you should be planning and reporting weekly")
      with col7:

       phasechoice = {0: "Select", 1: "Initiation", 2: "Planning", 3: "Execution", 4: "Closure"}
       st.session_state['pllistphase'] = st.radio('Project Phase', options=phasechoice.keys(), format_func=lambda x: "{}: {}".format(phasechoice.get(x),x), help="The phase of the project will determine which risks are higher or may be closed.  In the early phases of the project you have higher technology and cost risks and in later phases you can have engagement and resource risks. ", index=setvalue('pllistphase'))
      with col8:
       classchoice = {0: "Select", 1: "Software Build", 2: "Execution", 3: "Closure"}
       st.session_state['pllisttype'] = st.radio('Project Classification', options=classchoice.keys(), format_func=lambda x: "{} {}".format(classchoice.get(x),x), help="The type of project will be used to determine risks, a physical build can be impacted by weather.  Changes to procedures or pipelines require more focus on communication activities", index=setvalue('pllisttype'))
       plannote = plancomment(st.session_state['pldstartdate'], st.session_state['pldenddate'], daystoday, daystoend, st.session_state['thepmtimecomplete'], 3, st.session_state['plnumber'], st.session_state['plpname'], st.session_state['plsbenefits'], st.session_state['plncadence'], st.session_state['pllistphase'])
     st.markdown("{}".format(plannote), unsafe_allow_html=True)

     st.session_state['thepmheader'] = pd.DataFrame({
       "Project": [st.session_state.plpname, st.session_state.plpmname, st.session_state.pllisttype],
       "Sponsor": [st.session_state.plnumber, st.session_state.plspname, st.session_state.pldcharterdate]
      })

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Scope</h4>", unsafe_allow_html=True)
     my_expander2 = st.expander("The scope information outlines the features that the product should have. Scope also clarifies what is not planned and what may be negotiable", expanded=True)
     with my_expander2:
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
       st.session_state['plmlistscopelist'] = st.multiselect(
         'Select the non functional attributes',
         ['Security', 'Availability', 'Usability', 'Maintainability','Documentation', 'Robustness', 'None'],
         default=setvalue('pllistscoplist'))
      with col5:
       st.session_state['plmlistscopeoption'] = st.multiselect(
         'Select the technical architecture attributes',
         ['CMS', 'Framework', 'SEO', 'Search', 'Custom Theme', 'None'], default=setvalue('plmlistscopeoption'))
      planscope = "The scope includes " + st.session_state['plscopenicetohave'] + " and " + st.session_state['plscopeifpossible'] + " The following must be delivered as part of scope. " + st.session_state['plscopemusthave'] + " and the following are out of scope " + st.session_state['plscopeoutofscope'] 
     st.markdown(" :fireworks: {}".format(planscope), unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Schedule</h4>", unsafe_allow_html=True)
     milestonestatus = {0: "Not started", 1: "In Progress", 2: "On Hold", 3: "Complete"}
     my_expander6 = st.expander("Our plan has 7 phases or milestones, counters for milestones, features and releases.  Your project should have no less than 5 milestones however you can define more. Milestones are point in time events that are used to verify if the project is on track.  Releases completed result in business value to the users and customer.  Features are decomposed into unique stories, stories are SMART,  Specific, Measurable, Achievable, Realistic and have a time frame. ", expanded=True)
     with my_expander6:
      col4, col5 = st.columns(2)
      with col4:
       st.session_state['plnmilestoneplanned']  = 5
      with col5:
       #  calculate value based on chart
       st.session_state['plnmilestonecompleted']  = 2
      col1, col2, col3, col4, col5 = st.columns(5)
      with col1:
       st.session_state['plsml1phase']  = st.text_input ("Milestone 1", value=setvalue('plsm1phase'))
      with col2:
       st.session_state['plnml1status']  = st.radio ("Status 1", options=milestonestatus.keys(), format_func=lambda x: "{} {}".format(milestonestatus.get(x),x), index=setvalue('plnml1status'))
      with col3:
       st.session_state['pldml1completedate']  = st.date_input ("End 1", setvalue('pldml1completedate'))
      with col4:
       st.session_state['plnml1effort']  = st.number_input ("Effort 1", value=setvalue('plnml1effort'), step=5, max_value=100)
      with col5:
       st.session_state['pldml1actualedate']  = st.date_input ("Actual 1", setvalue('pldml1actualdate'))
      col1, col2, col3, col4, col5 = st.columns(5)
      with col1:
       st.session_state['plsml2phase']  = st.text_input ("Phase 2", value=setvalue('plsm2phase'))
      with col2:
       st.session_state['pldml2planneddate']  = st.date_input ("Start 2", setvalue('pldstartdate'))
      with col3:
       st.session_state['pldml2completedate']  = st.date_input ("End 2", setvalue('pldenddate'))
      with col4:
       st.session_state['plnml2effort']  = st.number_input ("Effort 2", value=setvalue('plnml2effort'))
      with col5:
       st.session_state['pldml2actualedate']  = st.date_input ("Actual 2", setvalue('pldml2actualdate'))
      (time2plan, time2inplan, time2toend) = datedifferences(st.session_state['pldml2planneddate'], st.session_state['pldml2completedate'])
      col1, col2, col3 = st.columns(3)
      with col1:
       pldml3planneddate  = st.date_input ("Build Start", st.session_state['pldstartdate'])
      with col2:
       pldml3completedate  = st.date_input ("Build End", st.session_state['pldenddate'])
      with col3:
       plnml3effort  = st.number_input ("Build Effort", value=40, key="plnml3effort")
      (time3plan, time3inplan, time3toend) = datedifferences(pldml3planneddate, pldml3completedate)
      col1, col2, col3 = st.columns(3)
      with col1:
       pldml4planneddate  = st.date_input ("Launch Start", st.session_state['pldstartdate'])
      with col2:
       pldml4completedate  = st.date_input ("Launch End", st.session_state['pldenddate'])
      with col3:
       plnml4effort  = st.number_input ("Launch Effort", value=20, key="plnml4effort")
      (time4plan, time4inplan, time4toend) = datedifferences(pldml4planneddate, pldml4completedate)
      col1, col2, col3 = st.columns(3)
      with col1:
       pldml5planneddate  = st.date_input ("Observe Start", st.session_state['pldstartdate'])
      with col2:
       pldml5completedate  = st.date_input ("Observe End", st.session_state['pldenddate'])
      with col3:
       plnml5effort  = st.number_input ("Observe Effort", value=10, key="plnml5effort")
      col4, col5 = st.columns(2)
      with col4:
       plfeaturesplanned  = st.slider ("Number of Features Planned", value=3, format="%i", min_value=1, max_value=20, step=1)
      with col5:
       plfeaturescompleted  = st.slider ("Number of Features Completed", value=0, format="%i", min_value=0, max_value=20, step=1)
      col4, col5 = st.columns(2)
      with col4:
       plreleasesplanned  = st.slider ("Number of Releases Planned", value=3, format="%i", min_value=1, max_value=20, step=1)
      with col5:
       plreleasescompleted  = st.slider ("Number of Releases Completed", value=0, format="%i", min_value=0, max_value=20, step=1)


     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Communication</h4>", unsafe_allow_html=True)
     my_expander3 = st.expander("Projects are executed and implemented by people, the team, the stakeholders and are implemented to provide benefit to users or customers.  The communication plan outlines the needs of the stakeholders, team and users. The complexity maintaining good communication and establishing trust between the team and the stakeholders is a factor of the size of the team, and how long they have been working together.  Trust is earned, not given.  Typically engagement of the team is high at the beginning of the project and decreases over time, and engagement of the stakeholders follows the opposite pattern  ", expanded=True)
     with my_expander3:
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       plnstakeholder  = st.slider ("Number of Stakeholders", value=3, format="%i", min_value=2, max_value=10, step=1 )
      with col2:
       plnteam  = st.slider ("Number of Core Team Members", value=2, format="%i", min_value=2, max_value=15, step=1)
      with col3:
       plnusers  = st.slider ("Number of Users", value=10, format="%i", min_value=10, max_value=1000000, step=100)
      with col4:
       plnactors  = st.slider ("Number of Actors", value=5, format="%i", min_value=1, max_value=10, step=1)
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       plnteamweeks  = st.slider ("Weeks with Full Team", value=3, format="%i", min_value=1, max_value=52, step=1 )
      with col2:
       plnopenroles  = st.slider ("Number of Open Roles", value=0, format="%i", min_value=0, max_value=15, step=1)
      with col3:
       plactivitylink  = st.text_input ("Activity Source Link (URL)" )
      with col4:
       plstanduplink  = st.text_input ("Standup Async Messaging Link (URL)" )
      planchannels = (plnstakeholder + plnteam) * (plnstakeholder + plnteam - 1)
      plancommunication = "There are " + str(planchannels) + " communication channels " 

     st.markdown(" :fireworks: {}".format(plancommunication), unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Cost</h4>", unsafe_allow_html=True)
     my_expander4 = st.expander("Changes incur costs, and these costs are monitored to ensure that the investment is in line with the value of the change to the business.  Using release completion, and timelines we calculate cost performance index (CPI) and schedule performance index (SPI) which are indicators if the project is in control. During conception and planning, earned value will be 0, when you start execution your earned value will be realized as releases are implemented", expanded=True)
     with my_expander4:
      col4, col5 = st.columns(2)
      with col4:
       plincomecurrency = st.radio('Currency Business', ('EUR', 'USD', 'CAN'))
      with col5:
       plexpensecurrency = st.radio('Currency Expense', ('USD', 'EUR', 'CAN'), help="When your expenses are in another currency you need to watch forex fluctuations")
      col4, col5 = st.columns(2)
      with col4:
       plbudget = st.slider('Budget', min_value=10000, max_value=200000, value=20000, step=5000)
      with col5:
       plspend = st.slider('Spend to Date', min_value=1000, max_value=250000, value=2000, step=500)
      col1, col2, col3 = st.columns(3)
      with col1:
       plhours = st.slider('Estimated Work Hours', min_value=100, max_value=20000, value=500, step=50)
      with col2:
       plavgrate = st.slider('Average Rate', min_value=10, max_value=200, value=45, step=5)
      with col3:
       plhoursused = st.slider('Work Hours Performed', min_value=50, max_value=20000, value=500, step=50)
      (evsummary, st.session_state['thepmcpi'], st.session_state['thepmspi'], etc)  = evreport((plbudget + (plbudget *.3)), plbudget, plhours, plavgrate, plexpensecurrency , st.session_state['pldstartdate'], st.session_state['pldenddate'], plspend, plreleasesplanned, plreleasescompleted, daystoend, daystoday, st.session_state['thepmtimecomplete'])
     #col1, col2, col3 = st.columns(3)
     #with col1:
     # st_radial('% Complete',timecomplete)
     #with col2:
     # st_radial('% Spent',(plspend/plbudget*100))
     #with col3:
     # st_radial('% Effort',(int(plhoursused/plhours*100)))
     st.markdown("{}".format(evsummary), unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Return on Investment</h4>", unsafe_allow_html=True)
     #https://www.investopedia.com/articles/basics/10/guide-to-calculating-roi.asp
     my_expander8 = st.expander("Measure the benefits or return on the investment over time based on the benefits, either savings or increased income after release.  A release means that a feature has been delivered and benefits can be realized, the reason for agile delivery and multiple releases is to realize some benefits earlier.  Execution of MVP or release of limited features can also test assumptions in the market.    ", expanded=True)
     with my_expander8:
      col1, col2, col3 = st.columns(3)
      with col1:
       plnincreaseincome  = st.slider ("Benefit Income", value=50000, format="%i", min_value=-100000, max_value=1000000, step=5000 )
      with col2:
       plnincreaseexpense  = st.slider ("Benefit Expense", value=-10000, format="%i", min_value=-100000, max_value=1000000, step=5000 )
     roi = (plnincreaseincome - plnincreaseexpense - plbudget) / (plbudget + etc) * 100
     roisummary = f'The roi {roi:.3f}'
     st.markdown(":fireworks: {}".format(roisummary), unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Constraints</h4>", unsafe_allow_html=True)
     my_expander5 = st.expander("What constraints and flexibility does the team have in decisions that impact time, scope, quality or cost, meaning little to no flexibility or a risk can be a constraint when the probability is almost certain.   Flexibility in these factors will impact your risk mitigation strategies.  If you have no flexiblity in cost variances, then risks that impact costs in your project should be monitored more closely.  If you have a weather risk, rain will delay the project and you live in a part of the world where it mostly rains such as London, weather is a constraint, it will occur, where is a risk is a known event that may occur. ", expanded=True)
     with my_expander5:
      st.session_state['plmlistconstraint'] = st.multiselect(
         'Select constraints (select in order by importance)',
         ['Budget', 'Resource', 'Schedule', 'Scope', 'None'], default=setvalue('plmlistconstraint'))
      st.session_state['plpscopecontingency']  = st.text_area ("Scope Contingency", value=setvalue('plpscopecontingency'))
      st.session_state['plptimecontingency']  = st.text_area ("Schedule Contingency", value=setvalue('plptimecontingency'))
      st.session_state['plpbudgetcontingency']  = st.text_area ("Budget Contingency", value=setvalue('plpbudgetcontingency'))
      st.session_state['plpresourcecontingency']  = st.text_area ("Resource Contingency", value=setvalue('plpresourcecontingency'))
     submit = st.form_submit_button("Save")
     clear = st.form_submit_button("Clear", on_click=clear_form)
     if clear:
      clear_form()
      st.info("The information was cleared, thank you for using the PM Monitor.  Use Download to save a copy of your charter offline")
     if submit:
        st.info("The information was updated, thank you for using the PM Monitor.  Use Download to save a copy of your charter offline")

#with st.expander(label="Save or Restore Plan", expanded=False):
with st.sidebar:

    # 1. Download Settings Button
    dataitems = st.session_state.items()
    datalist = list(dataitems)
    df = pd.DataFrame(datalist)
    csv = df.to_csv().encode('utf-8')
    col1, col2 = st.columns([6, 5])
    settings_to_download = {k: v for k, v in st.session_state.items()
                            if "button" not in k and "file_uploader" not in k}
    button_download = col1.download_button(label="Download Settings",
                                           data=csv,
                                           file_name=f"pmmonitorsettings.csv",
                                           help="Click to Download Current Settings")

    # 2. Select Settings to be uploaded
    uploaded_file = st.file_uploader(label="Select the Settings File to be uploaded",
                                     help="Select the Settings File (Downloaded in a previous run) that you want"
                                          " to be uploaded and then applied (by clicking 'Apply Settings' above)"
                                          " in order to filter the perimeter")
    if uploaded_file is not None:
        uploaded_settings = pd.read_csv(uploaded_file)
    else:
        uploaded_settings = settings_to_download
        st.warning("**WARNING**: Select the Settings File to be uploaded")

    # 3. Apply Settings
    def upload_saved_settings(saved_settings):
        """Set session state values to what specified in the saved_settings."""
        for i in range(len(saved_settings)):
          if isinstance(saved_settings.iloc[i, 2],str):
            # st.write(st.session_state[saved_settings.iloc[i, 1]])
            if saved_settings.iloc[i, 1].startswith('plp'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
            if saved_settings.iloc[i, 1].startswith('pls'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
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
              #st.session_state[saved_settings.iloc[i, 1]] = datetime.strptime(saved_settings.iloc[i, 2], '%m-%m-%y').date()
              st.session_state[saved_settings.iloc[i, 1]] = datetime2
        return

    button_apply_settings = col2.button(label="Apply Settings",
                                        on_click=upload_saved_settings,
                                        args=(uploaded_settings,),
                                        help="Click to Apply the Settings of the Uploaded file.\\\n"
                                             "Please start by uploading a Settings File below")


