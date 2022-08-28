import streamlit as st
import pathlib
from datetime import datetime, timedelta, date
import pandas as pd
from utilities import currencyrisk, evreport, plancomment, get_table_download_link, datedifferences
from st_radial import st_radial

#@st.cache

#ast.shared.components.title_awesome("Charter")
    # with st.spinner("Loading  ..."):

    # initialize session state variables and form values
    #if savedform.has_key("plnumber"):
fields=["plnumber","plname", "plpmname","plspname", "plbenefits"]
savedform=dict.fromkeys(fields)

    #with st.form("my_plan", clear_on_submit = True):
with st.form(key="my_plan"):

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     #col6aa, col7aa = st.columns([1, 3])
     my_expander0 = st.expander("A project is finite, has a start and and end timeframe and is unique. A project is undertaken to implement change, deliver a new product, service or process.  The Project Charter outlines the timeline and the benefits, scope and contingency plans", expanded=True)
     with my_expander0:
      col4, col5 = st.columns(2)
      with col4:
       savedform['plnumber']  = st.text_input ("Project ID", max_chars=10, value=savedform['plnumber'], help="A unique id to identify this project")
      with col5:
       savedform['plname']  = st.text_input ("Project Name", help="A short project name for reports", max_chars=50, key="plname", value=savedform['plname'])
      col4, col5 = st.columns(2)
      with col4:
       savedform['plpmname'] = st.text_input ("Project Manager Name", max_chars=30, key="plpmname", value=savedform['plpmname'])
      with col5:
       savedform['plspname']  = st.text_input ("Product Owner or Sponsor Name", max_chars=30, key="plspname", value=savedform['plspname'])
      savedform['plbenefits']  = st.text_input ("What are the Benefits?", key="plbenefits", value=savedform['plbenefits'])
      col6, col7 = st.columns([3,1])
      with col6:
       plpmreport = st.text_input ("PM report", key="plpmreport", value="https://www.youtube.com/watch?v=c4fEms85NQQ")
      with col7:
       plpmreportid = st.text_input ("PM report", key="plpmreportid", value="c4fEms85NQQ")
     # set some dates
      week  = timedelta(days = 7)
      daytoday = date.today()
     
      col1, col2, col3 = st.columns(3)
      with col1:
       pldstartdate  = st.date_input ("Start Date", daytoday - (week * 4), key="pldstartdate")
      with col2:
       pldenddate  = st.date_input ("End Date", daytoday + (week * 8), key="pldenddate")
      with col3:
       pldcharterdate  = st.date_input ("Charter Date", daytoday, key="pldcharterdate")

      daystoend = (pldenddate-pldstartdate).days
      daystoday = (daytoday-pldstartdate).days
      if daystoend > 0:
        timecomplete = int(daystoday / daystoend * 100)
      else:
        timecomplete = 0

      col6, col7, col8 = st.columns(3)
      with col6:
       pllistcadence = st.radio('Cadence', ('weekly', 'monthly', 'biweekly', 'quarterly'), help="Cadence is the frequency that the project replans and reports on progress.  In a maintenance project you should plan and report quarterly.  In active development projects when investment is higher, you should be planning and reporting weekly", key="pllistcadence")
      with col7:
       pllistphase = st.radio('Project Phase', ('Idea', 'Plan', 'Build', 'Launch', 'Observe'), help="The phase of the project will determine which risks are higher or may be closed.  In the early phases of the project you have higher technology and cost risks and in later phases you can have engagement and resource risks. ", key="pllistphase")
      with col8:
       pllisttype = st.radio('Project Classification', ('Software Build', 'Site Build', 'New Procedures SOP', 'New Pipeline or Process',  'Sales and Marketing', 'Software Design', 'Other'), help="The type of project will be used to determine risks, a physical build can be impacted by weather.  Changes to procedures or pipelines require more focus on communication activities", key="pllisttype")
       plannote = plancomment(pldstartdate, pldenddate, daystoday, daystoend, timecomplete, 3, savedform['plnumber'], savedform['plname'], savedform['plbenefits'], pllistcadence, pllistphase)
     st.markdown(" :fireworks: {}".format(plannote), unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Scope</h4>", unsafe_allow_html=True)
     my_expander2 = st.expander("The scope information outlines the features that the product should have. Scope also clarifies what is not planned and what may be negotiable", expanded=True)
     with my_expander2:
      col4, col5 = st.columns(2)
      with col4:
       plscopemusthave  = st.text_area ("Must Have", key="plscopemusthave")
      with col5:
       plscopenicetohave  = st.text_area ("Nice to Have", key="plscopenicetohave")
      col4, col5 = st.columns(2)
      with col4:
       plscopeifpossible  = st.text_area ("If Possible", key="plscopeifpossible")
      with col5:
       plscopeoutofscope  = st.text_area ("Out of Scope", key="plscopeoutofscope")
      with col4:
       plmlistscopefunctionaloptions = st.multiselect(
         'Select the non functional attributes',
         ['Security', 'Availability', 'Usability', 'Maintainability','Documentation', 'Robustness'], key="plmlistscopefunctionaloptions")
      with col5:
       plmlistscopetechnicaloptions = st.multiselect(
         'Select the technical architecture attributes',
         ['CMS', 'Framework', 'SEO', 'Search', 'Custom Theme'], key="plmlistscopetechnicaloptions")
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Schedule</h4>", unsafe_allow_html=True)
     my_expander6 = st.expander("A project has 5 phases.  In your plan, these phases are tracked as milestones.  Your project will have no less than 5 milestones however you can define more. Milestones are point in time events that are used to verify if the project is on track.  Releases completed result in business value to the users and customer.  Features are decomposed into unique stories, stories are SMART,  Specific, Measurable, Achievable, Realistic and have a time frame. ", expanded=True)
     with my_expander6:
      col4, col5 = st.columns(2)
      with col4:
       plnmilestoneplanned  = st.slider ("Number of Milestones Planned", value=5, format="%i", min_value=1, max_value=20, step=1, key="plnmilestoneplanned")
      with col5:
       plnmilestonecompleted  = st.slider ("Number of Milestones Completed", value=0, format="%i", min_value=0, max_value=20, step=1, key="plnmilestonecompleted")
      col1, col2, col3 = st.columns(3)
      with col1:
       pldml1planneddate  = st.date_input ("Idea Start", pldstartdate, key="pldml1planneddate")
      with col2:
       pldml1completedate  = st.date_input ("Idea End", pldenddate, key="pldml1completedate")
      with col3:
       plnml1effort  = st.number_input ("Idea Effort", value=10, key="plnml1effort")
      col1, col2, col3 = st.columns(3)
      with col1:
       pldml2planneddate  = st.date_input ("Plan Start", pldstartdate)
      with col2:
       pldml2completedate  = st.date_input ("Plan End", pldenddate)
      with col3:
       plnml2effort  = st.number_input ("Plan Effort", value=20, key="plnml2effort")
      (time2plan, time2inplan, time2toend) = datedifferences(pldml2planneddate, pldml2completedate)
      col1, col2, col3 = st.columns(3)
      with col1:
       pldml3planneddate  = st.date_input ("Build Start", pldstartdate)
      with col2:
       pldml3completedate  = st.date_input ("Build End", pldenddate)
      with col3:
       plnml3effort  = st.number_input ("Build Effort", value=40, key="plnml3effort")
      (time3plan, time3inplan, time3toend) = datedifferences(pldml3planneddate, pldml3completedate)
      col1, col2, col3 = st.columns(3)
      with col1:
       pldml4planneddate  = st.date_input ("Launch Start", pldstartdate)
      with col2:
       pldml4completedate  = st.date_input ("Launch End", pldenddate)
      with col3:
       plnml4effort  = st.number_input ("Launch Effort", value=20, key="plnml4effort")
      (time4plan, time4inplan, time4toend) = datedifferences(pldml4planneddate, pldml4completedate)
      col1, col2, col3 = st.columns(3)
      with col1:
       pldml5planneddate  = st.date_input ("Observe Start", pldstartdate)
      with col2:
       pldml5completedate  = st.date_input ("Observe End", pldenddate)
      with col3:
       plnml5effort  = st.number_input ("Observe Effort", value=10, key="plnml5effort")
      #st.write(time5plan, time5inplan, time5toend)
      col1, col2, col3 = st.columns(3)
      with col1:
       rad2 = st_radial('% Complete Plan',time2plan)
      with col2:
       rad3 = st_radial('% Complete Build',time3plan)
      with col3:
       rad4 = st_radial('% Complete Launch',time4plan)
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

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Return on Investment</h4>", unsafe_allow_html=True)
     #https://www.investopedia.com/articles/basics/10/guide-to-calculating-roi.asp
     my_expander8 = st.expander("Measure the benefits or return on the investment over time based on the benefits, either savings or increased income after release.  A release means that a feature has been delivered and benefits can be realized, the reason for agile delivery and multiple releases is to realize some benefits earlier.  Release of some features can also test your assumptions in the market.    ", expanded=True)
     with my_expander8:
      col1, col2, col3 = st.columns(3)
      with col1:
       plnincreaseincome  = st.slider ("Benefit Income", value=-10, format="%i", min_value=2, max_value=10, step=1 )
      with col2:
       plnincreaseexpense  = st.slider ("Benefit Expense", value=-10, format="%i", min_value=2, max_value=10, step=1 )

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Team and Stakeholders</h4>", unsafe_allow_html=True)
     my_expander3 = st.expander("Projects are executed and implemented by people, the team, the stakeholders and are implemented to provide benefit to users or customers  ", expanded=True)
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
 
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Cost Information</h4>", unsafe_allow_html=True)
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
      (st.session_state.evsummary, st.session_state.cpi, st.session_state.spi, st.session_state.etc)  = evreport((plbudget + (plbudget *.3)), plbudget, plhours, plavgrate, plexpensecurrency , pldstartdate, pldenddate, plspend, plreleasesplanned, plreleasescompleted, daystoend, daystoday, timecomplete)
     col1, col2, col3 = st.columns(3)
     with col1:
      st_radial('% Complete',timecomplete)
     with col2:
      st_radial('% Spent',(plspend/plbudget*100))
     with col3:
      st_radial('% Effort',(int(plhoursused/plhours*100)))
     st.markdown("<h4 style='text-align: center;'>CPI and SPI report</h4>", unsafe_allow_html=True)
     st.markdown("{}".format(st.session_state.evsummary), unsafe_allow_html=True)


     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Constraints</h4>", unsafe_allow_html=True)
     my_expander5 = st.expander("What constraints and flexibility does the team have in decisions that impact time, scope, quality or cost, meaning little to no flexibility or a risk can be a constraint when the probability is almost certain.   Flexibility in these factors will impact your risk mitigation strategies.  If you have no flexiblity in cost variances, then risks that impact costs in your project should be monitored more closely.  If you have a weather risk, rain will delay the project and you live in a part of the world where it mostly rains such as London, weather is a constraint, it will occur, where is a risk is a known event that may occur. ", expanded=True)
     with my_expander5:
      plmlistconstraint = st.multiselect(
         'Select constraints',
         ['Budget', 'Resource', 'Schedule', 'Scope', 'Documentation'], key="plmlistconstraint")
      plscopecontingency  = st.text_area ("Scope Contingency")
      pltimecontingency  = st.text_area ("Schedule Contingency")
      plbudgetcontingency  = st.text_area ("Budget Contingency")
      plresourcecontingency  = st.text_area ("Resource Contingency")
     submit = st.form_submit_button("Save")
     if submit:
        st.info("The information was updated, thank you for using the PM Monitor.  Use Download to save a copy of your charter offline")

with st.expander(label="Save or Restore settings and data", expanded=False):

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
            st.write(st.session_state[saved_settings.iloc[i, 1]])
            if saved_settings.iloc[i, 1].startswith('pls'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
              st.write(st.session_state[saved_settings.iloc[i, 1]])
            if saved_settings.iloc[i, 1].startswith('plmlist'):
              string_without_brackets = saved_settings.iloc[i, 2].strip("[]")
              string_without_brackets = string_without_brackets.replace("'", "")
              string_list = string_without_brackets.split(", ")
              for x in string_list:
               if x != "":
                 if x not in st.session_state[saved_settings.iloc[i, 1]]:  # prevent duplicates
                    st.session_state[saved_settings.iloc[i, 1]].append(x)
            if saved_settings.iloc[i, 1].startswith('pld'):
              #st.session_state[saved_settings.iloc[i, 1]] = datetime.strptime(saved_settings.iloc[i, 2], '%Y-%m-%d').date()
              st.session_state[saved_settings.iloc[i, 1]] = date.today()
              st.write(st.session_state[saved_settings.iloc[i, 1]])
        return

    button_apply_settings = col2.button(label="Apply Settings",
                                        on_click=upload_saved_settings,
                                        args=(uploaded_settings,),
                                        help="Click to Apply the Settings of the Uploaded file.\\\n"
                                             "Please start by uploading a Settings File below")


