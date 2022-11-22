import streamlit as st
import pathlib
from math import log
from datetime import datetime, timedelta, date
import pandas as pd
from utilities import currencyrisk, evreport, plancomment, get_table_download_link, datedifferences
from annotated_text import annotated_text
import altair as alt
from st_aggrid import AgGrid
#from st_radial import st_radial

primaryColor="#264653"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F4A261"
textColor="#2A9D8F"

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
            if saved_settings.iloc[i, 1].startswith('pln'):
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
  for key in st.session_state.keys():
    del st.session_state[key]

#@st.cache

st.markdown("<h3 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)

with st.form(key="pmmonitorplan", clear_on_submit=False):
     tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Info", "Scope", "Cost", "Schedule", "Communication", "Quality", "Constraints", "ROI"])
     with tab1:
      st.subheader("Project Information")
      st.write("A project is finite, has a start and and end timeframe and is unique. A project is undertaken to reach a goal, implement change, deliver a new product, service or process.  The Project Plan outlines the timeline and the benefits, scope and contingency plans.  The plan provides the necessary information for the project manager and The PM Monitor to report on the progress of the project and manage issues.")
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
      weeksinplan = int(daystoend/7)

      st.session_state['thepmtimecomplete'] = 0
      if daystoend > 0:
        st.session_state['thepmtimecomplete'] = int(daystoday / daystoend * 100)

      col6, col7, col8 = st.columns(3)
      with col6:
       st.session_state['plncadence'] = st.slider('Cadence', min_value=0, max_value=12, value=setvalue('plncadence'), help="Cadence is the frequency that the project replans and reports on progress.  In a maintenance project you should plan and report quarterly.  In active development projects when investment is higher, you should be planning and reporting weekly")
      with col7:

       phasechoice = {0: "None", 1: "Initiation", 2: "Planning", 3: "Execution", 4: "Closure"}
       st.session_state['pllistphase'] = st.radio('Project Phase', options=phasechoice.keys(), format_func=lambda x: "{}: {}".format(phasechoice.get(x),x), help="The phase of the project will determine which risks are higher or may be closed.  In the early phases of the project you have higher technology and cost risks and in later phases you can have engagement and resource risks. ", index=setvalue('pllistphase'))
      with col8:
       classchoice = {0: "None", 1: "Software Build", 2: "Software Design", 3: "Site Build", 4: "Brand Marketing", 5: "New Procedures", 6: "Scheduled Maintenance"}
       st.session_state['pllisttype'] = st.radio('Project Classification', options=classchoice.keys(), format_func=lambda x: "{} {}".format(classchoice.get(x),x), help="The type of project will be used to determine risks, a physical build can be impacted by weather.  Changes to procedures or pipelines require more focus on communication activities", index=setvalue('pllisttype'))
       plannote = plancomment(st.session_state['pldstartdate'], st.session_state['pldenddate'], daystoday, daystoend, st.session_state['thepmtimecomplete'], 3, st.session_state['plnumber'], st.session_state['plpname'], st.session_state['plsbenefits'], st.session_state['plncadence'], st.session_state['pllistphase'])
      st.write(plannote)
     st.session_state['thepmheader'] = pd.DataFrame({
       "Project": [st.session_state.plpname, st.session_state.plpmname, st.session_state.pllisttype],
       "Sponsor": [st.session_state.plnumber, st.session_state.plspname, st.session_state.pldcharterdate]
      })

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
       st.session_state['plscopechangeadd']  = st.text_area ("Scope Change Additions", value=setvalue('plscopechangeadd'))
      with col5:
       st.session_state['plscopechangedel']  = st.text_area ("Scope Change Removal", value=setvalue('plscopechangedel'))
      with col4:
       st.session_state['plmlistscopelist'] = st.multiselect(
         'Select non functional attributes',
         ['Security', 'Availability', 'Usability', 'Maintainability','Documentation', 'Robustness', 'None'],
         default=setvalue('pllistscoplist'))
      with col5:
       st.session_state['plmlistscopeoption'] = st.multiselect(
         'Select technical architecture attributes',
         ['CMS', 'Framework', 'SEO', 'Search', 'Custom Theme', 'None'], default=setvalue('plmlistscopeoption'))
      planscope = "The scope includes " + st.session_state['plscopenicetohave'] + " and " + st.session_state['plscopeifpossible'] + " The following must be delivered as part of scope. " + st.session_state['plscopemusthave'] + " and the following are out of scope " + st.session_state['plscopeoutofscope'] 
      st.write(planscope)

     milestonestatus = {0: "Not started", 1: "In Progress", 2: "On Hold", 3: "Complete"}
     with tab4:
      st.subheader("Schedule")
      st.write("Our plan is managed and controlled by the defined milestones.  Your project should have no less than 5 milestones however you can define more. Milestones are point in time events that are used to verify if the project is on track.  Releases completed result in business value to the users and customer.  Features are decomposed into unique stories, stories are SMART,  Specific, Measurable, Achievable, Realistic and have a time frame. ")
      dfmilestone = pd.read_csv(r'milestones.csv', parse_dates=['reportdate','plandate'])
      dfresponse = AgGrid(dfmilestone, height=200, theme='streamlit', editable=True, fit_columns_on_grid_load=True)
      chart = alt.Chart(dfmilestone).mark_line(point = True).encode(
          alt.X('monthdate(reportdate):O', title='Report Date'),
          alt.Y('monthdate(plandate):O', title='Plan Date', scale=alt.Scale(reverse=True)),
          color="Milestone")
      st.altair_chart(chart, use_container_width=True)

     with tab5:
      st.subheader("Communication")
      st.write("Projects are executed and implemented by people, the team, the stakeholders and are implemented to provide benefit to users or customers.  The communication plan outlines the needs of the stakeholders, team and users. The complexity maintaining good communication and establishing trust between the team and the stakeholders is a factor of the size of the team, and how long they have been working together.  Trust is earned, not given.  Typically engagement of the team is high at the beginning of the project and decreases over time, and engagement of the stakeholders follows the opposite pattern  ")
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
      with col1:
       st.session_state['plpsolutionname'] = st.text_input ("Solution Architect Name", max_chars=30, value=setvalue('plpsolutionname'))
      with col2:
       st.session_state['plpoperationname'] = st.text_input ("Operations Lead Name", max_chars=30, value=setvalue('plpoperationname'))
      with col3:
       st.session_state['plpinspectorname'] = st.text_input ("Inspection Lead Name", max_chars=30, value=setvalue('plpinspectorname'))
      with col4:
       st.session_state['plpaccountname'] = st.text_input ("Account Manager Name", max_chars=30, value=setvalue('plpaccountname'))
      planchannels = (plnstakeholder + plnteam) * (plnstakeholder + plnteam - 1)

      plancommunication = "There are " + str(planchannels) + " communication channels " 
      st.write(plancommunication)
      st.markdown('##') 

     with tab6:
      st.subheader("Quality")
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       st.session_state['plntests']  = st.slider ("Number of Tests", value=setvalue('plntests'), format="%i", min_value=0, max_value=52, step=1 )
      with col2:
       st.session_state['plntestsrun']  = st.slider ("Number of Tests Run", value=setvalue('plntestsrun'), format="%i", min_value=0, max_value=52, step=1 )
      with col3:
       st.session_state['plntestsfailed']  = st.slider ("Number of Tests Failed", value=setvalue('plntestsfailed'), format="%i", min_value=0, max_value=52, step=1 )
      with col4:
       st.session_state['pldinspectdate']  = st.date_input ("Inspection Report Date", setvalue('pldinspectdate'))

     with tab3:
      st.subheader("Cost")
      st.write("Changes incur costs, and these costs are monitored to ensure that the investment is in line with the value of the change to the business.  Using release completion, and timelines we calculate cost performance index (CPI) and schedule performance index (SPI) which are indicators if the project is in control. During conception and planning, earned value will be 0, when you start execution your earned value will be realized as releases are implemented")
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
      mcomplete = len(dfmilestone[dfmilestone.Status == 'Completed'])
      mplanned = len(dfmilestone[dfmilestone.Status == 'Planned'])
      (evsummary, st.session_state['thepmcpi'], st.session_state['thepmspi'], etc)  = evreport((plbudget + (plbudget *.3)), plbudget, plhours, plavgrate, plexpensecurrency , st.session_state['pldstartdate'], st.session_state['pldenddate'], plspend, mplanned, mcomplete, daystoend, daystoday, st.session_state['thepmtimecomplete'])
     #col1, col2, col3 = st.columns(3)
     #with col1:
     # st_radial('% Complete',timecomplete)
     #with col2:
     # st_radial('% Spent',(plspend/plbudget*100))
     #with col3:
     # st_radial('% Effort',(int(plhoursused/plhours*100)))
      st.markdown("{}".format(evsummary), unsafe_allow_html=True)

     with tab8:
      st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Return on Investment</h4>", unsafe_allow_html=True)
     #https://www.investopedia.com/articles/basics/10/guide-to-calculating-roi.asp
      st.write("Measure the benefits or return on the investment over time based on the benefits, either savings or increased income after release.  A release means that a feature has been delivered and benefits can be realized, the reason for agile delivery and multiple releases is to realize some benefits earlier.  Execution of MVP or release of limited features can also test assumptions in the market.    ")
      col1, col2, col3 = st.columns(3)
      with col1:
       st.session_state['plnincreaseincome']  = st.slider ("Benefit Income", value=setvalue('plnincreaseincome'), format="%i", min_value=-100000, max_value=1000000, step=5000 )
      with col2:
       st.session_state['plnincreaseexpense']  = st.slider ("Benefit Expense", value=setvalue('plnincreaseexpense'), format="%i", min_value=-100000, max_value=1000000, step=5000 )
      with col3:
       st.session_state['plnbenefitdate']  = st.slider ("Benefit Period", value=1, format="%i", min_value=1, max_value=12, step=1 )
      benefitdelta = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'])
      roi = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'] - plbudget) / (plbudget + etc) * 100
      rateofreturn = (st.session_state['plnincreaseincome'] - st.session_state['plnincreaseexpense'] - plbudget) / (plbudget + etc)
     # annualroi = (1 + rateofreturn) ^ (1 / st.session_state['plnbenefitdate']) - 1
     # st.write(annualroi)
      roisummary = f'The roi is {roi:.3f} with an investment of {plbudget:.0f} and a benefit of {benefitdelta:.0f} to begin  months after delivery '
      st.write(roisummary)

     with tab7:
      st.subheader("Constraints")
      st.write("What constraints and flexibility does the team have in decisions that impact time, scope, quality or cost, meaning little to no flexibility or a risk can be a constraint when the probability is almost certain.   Flexibility in these factors will impact your risk mitigation strategies.  If you have no flexiblity in cost variances, then risks that impact costs in your project should be monitored more closely.  If you have a weather risk, rain will delay the project and you live in a part of the world where it mostly rains such as London, weather is a constraint, it will occur, where is a risk is a known event that may occur. ")
      st.session_state['plmlistconstraint'] = st.multiselect(
         'Select constraints (select in order by importance)',
         ['Budget', 'Resource', 'Schedule', 'Scope', 'None'], default=setvalue('plmlistconstraint'))
      st.session_state['plpscopecontingency']  = st.text_area ("Scope Contingency", value=setvalue('plpscopecontingency'))
      st.session_state['plptimecontingency']  = st.text_area ("Schedule Contingency", value=setvalue('plptimecontingency'))
      st.session_state['plpbudgetcontingency']  = st.text_area ("Budget Contingency", value=setvalue('plpbudgetcontingency'))
      st.session_state['plpresourcecontingency']  = st.text_area ("Resource Contingency", value=setvalue('plpresourcecontingency'))
      thepmcontingencysummary = "The project contingency plans include Scope: " + st.session_state['plpscopecontingency']+ " Schedule: " + st.session_state['plptimecontingency'] + " Budget:  " + st.session_state['plpbudgetcontingency'] + " and Resource:  " + st.session_state['plpresourcecontingency']
      st.markdown("{}".format(thepmcontingencysummary), unsafe_allow_html=True)

     #  the buttons to validate and save information
     col1, col2, col3 = st.columns(3)
     with col1:
       submit = st.form_submit_button("Save Plan")
     with col2:
       clear = st.form_submit_button("Clear Plan", on_click=clear_form)
     if clear:
      clear_form()
      st.info("The information was cleared, thank you for using the PM Monitor.  Use Export Plan to save a copy of your plan offline")
     if submit:
        st.info("The information was updated, thank you for using the PM Monitor.  Use Export to save a copy of your plan offline")

    # 1. Download Settings Button
dataitems = st.session_state.items()
datalist = list(dataitems)
df = pd.DataFrame(datalist)
csv = df.to_csv().encode('utf-8')
col1, col2, col3, col4 = st.columns([1, 1, 3, 3])
settings_to_download = {k: v for k, v in st.session_state.items()
                            if "button" not in k and "file_uploader" not in k}

    # 2. Select Settings to be uploaded
with col3:
 uploaded_file = st.file_uploader(label="Select the Settings File to be uploaded",
                                     help="Select the Settings File (Downloaded in a previous run) that you want"
                                          " to be uploaded and then applied (by clicking 'Apply Settings' above)")
with col4:
 if uploaded_file is not None:
         uploaded_settings = pd.read_csv(uploaded_file)
 else:
        uploaded_settings = settings_to_download
        st.warning("**WARNING**: Select the Settings File to be uploaded")

button_apply_settings = col2.button(label="Apply Plan",
                                        on_click=upload_saved_settings,
                                        args=(uploaded_settings,),
                                        help="Click to Apply the Settings of the Uploaded file.\\\n"
                                             "Please start by uploading a Settings File below")

button_download = col1.download_button(label="Export Plan",
                                           data=csv,
                                           file_name=f"pmmonitorsettings.csv",
                                           help="Click to Download Current Settings")
