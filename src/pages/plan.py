"""Page for viewing the awesome Project canvas"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import pandas as pd
#import caching
from utilities import currencyrisk, evreport, plancomment, get_table_download_link
from st_radial import st_radial

@st.cache
def get_plan_markdown() -> str:
    """Enter the plan and return CPI and SPI
    """
    url = pathlib.Path(__file__).parent.parent.parent / "AWESOME-STREAMLIT.md"
    with open(url, mode="r") as file:
        readme_md_contents = "".join(file.readlines())
    return readme_md_contents.split("\n", 3)[-1]

#  clear all the text fields in form
def clear_form():
    for key, value in st.session_state.items():
      st.write(type(st.session_state[key]), key, value)
      if key.startswith('pl'):
        if isinstance(st.session_state[key],str):
            st.session_state[key] = ""
        if isinstance(st.session_state[key],int):
          st.session_state[key] = 0
        #if isinstance(st.session_state[key],list):
        #  del st.session_state[key]
        if isinstance(st.session_state[key],datetime.date):
          st.session_state[key] = datetime.date.today()

#  show where we are in terms of plan and calendar
def datedifferences(startdate, enddate):
    daytoday = datetime.date.today()
    daysinplan = 0
    if enddate > startdate:
       daysinplan = (enddate-startdate).days
    daysdoneplan = 0
    if daytoday > startdate:
       daysdoneplan = (daytoday-startdate).days
    percentcomplete = 0
    if daysinplan > 0:
       percentcomplete = int(daysdoneplan / daysinplan * 100)
    return (daysinplan, daysdoneplan, percentcomplete)

def write():
    """Method used to write the page in the app.py file"""
    ast.shared.components.title_awesome("Charter")
    # with st.spinner("Loading  ..."):

    # dictionary with form responses
    savedform = {'plnumber': "1.1", 'plname': "project name"}

    # initialize session state variables
    if 'plnumber' not in st.session_state:
     st.session_state.plnumber = ""

    #with st.form("my_plan", clear_on_submit = True):
    with st.form("my_plan"):

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     #col6aa, col7aa = st.columns([1, 3])
     my_expander0 = st.expander("A project is finite, has a start and and end timeframe and is unique. A project is undertaken to implement change, deliver a new product, service or process.  The Project Charter outlines the timeline and the benefits, scope and contingency plans", expanded=True)
     with my_expander0:
      col4, col5 = st.columns(2)
      with col4:
       savedform['plnumber']  = st.text_input ("Project ID", max_chars=10, value=savedform['plnumber'], help="A unique id to identify this project", key="plnumber")
      with col5:
       plname  = st.text_input ("Project Name", help="A short project name for reports", max_chars=50, key="plname")
      col4, col5 = st.columns(2)
      with col4:
       plpmname  = st.text_input ("Project Manager Name", max_chars=30, key="plpmname")
      with col5:
       plspname  = st.text_input ("Product Owner or Sponsor Name", max_chars=30, key="plspname")
      plbenefits  = st.text_input ("What are the Benefits?", key="plbenefits")
  
     # set some dates
      week  = datetime.timedelta(days = 7)
      daytoday = datetime.date.today()
     
      col1, col2, col3 = st.columns(3)
      with col1:
       plstartdate  = st.date_input ("Start Date", daytoday - (week * 4), key="plstartdate")
      with col2:
       plenddate  = st.date_input ("End Date", daytoday + (week * 8), key="plenddate")
      with col3:
       plcharterdate  = st.date_input ("Charter Date", daytoday, key="plcharterdate")

      daystoend = (plenddate-plstartdate).days
      daystoday = (daytoday-plstartdate).days
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
       plannote = plancomment(plstartdate, plenddate, daystoday, daystoend, timecomplete, 3, savedform['plnumber'], plname, plbenefits, pllistcadence, pllistphase)
     st.markdown(" :fireworks: {}".format(plannote), unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Scope</h4>", unsafe_allow_html=True)
     my_expander2 = st.expander("The scope information outlines the features that the product should have. Scope also clarifies what is not in scope", expanded=True)
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
       pllistscopefunctionaloptions = st.multiselect(
         'Select the non functional attributes',
         ['Security', 'Availability', 'Usability', 'Maintainability','Documentation', 'Robustness'], key="pllistscopefunctionaloptions")
      with col5:
       pllistscopetechnicaloptions = st.multiselect(
         'Select the technical architecture attributes',
         ['CMS', 'Framework', 'SEO', 'Search', 'Custom Theme'], key="pllistscopetechnicaloptions")
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Schedule</h4>", unsafe_allow_html=True)
     my_expander6 = st.expander("A project has 5 phases.  In your plan, these phases are tracked as milestones.  Your project will have no less than 5 milestones however you can define more. Milestones are point in time events that are used to verify if the project is on track.  This is shown using the milestone trend chart. Releases completed result in business value to the users and customer.  Features are defined as stories, stories are SMART,  Specific, Measurable, Achievable, Realistic and have a time frame. ", expanded=True)
     with my_expander6:
      col4, col5 = st.columns(2)
      with col4:
       plmilestoneplanned  = st.slider ("Number of Milestones Planned", value=5, format="%i", min_value=1, max_value=20, step=1, key="plmilestoneplanned")
      with col5:
       plmilestonecompleted  = st.slider ("Number of Milestones Completed", value=0, format="%i", min_value=0, max_value=20, step=1, key="plmilestonecompleted")
      col1, col2, col3 = st.columns(3)
      with col1:
       plml1planned  = st.date_input ("Idea Start", plstartdate, key="plml1planned")
      with col2:
       plml1complete  = st.date_input ("Idea End", plenddate, key="plml1complete")
      with col3:
       plml1effort  = st.number_input ("Idea Effort", value=10, key="plml1effort")
      col1, col2, col3 = st.columns(3)
      with col1:
       plml2planned  = st.date_input ("Plan Start", plstartdate)
      with col2:
       plml2complete  = st.date_input ("Plan End", plenddate)
      with col3:
       plml2effort  = st.number_input ("Plan Effort", value=20, key="plml2effort")
      (time2plan, time2inplan, time2toend) = datedifferences(plml2planned, plml2complete)
      col1, col2, col3 = st.columns(3)
      with col1:
       plml3planned  = st.date_input ("Build Start", plstartdate)
      with col2:
       plml3complete  = st.date_input ("Build End", plenddate)
      with col3:
       plml3effort  = st.number_input ("Build Effort", value=40, key="plml3effort")
      (time3plan, time3inplan, time3toend) = datedifferences(plml3planned, plml3complete)
      col1, col2, col3 = st.columns(3)
      with col1:
       plml4planned  = st.date_input ("Launch Start", plstartdate)
      with col2:
       plml4complete  = st.date_input ("Launch End", plenddate)
      with col3:
       plml4effort  = st.number_input ("Launch Effort", value=20, key="plml4effort")
      (time4plan, time4inplan, time4toend) = datedifferences(plml4planned, plml4complete)
      col1, col2, col3 = st.columns(3)
      with col1:
       plml5planned  = st.date_input ("Observe Start", plstartdate)
      with col2:
       plml5complete  = st.date_input ("Observe End", plenddate)
      with col3:
       plml5effort  = st.number_input ("Observe Effort", value=10, key="plml5effort")
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

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Team and Stakeholders</h4>", unsafe_allow_html=True)
     my_expander3 = st.expander("Projects are executed and implemented by people, the team, the stakeholders and are implemented to provide benefit to users or customers  ", expanded=True)
     with my_expander3:
      col1, col2, col3 = st.columns(3)
      with col1:
       plstakeholder  = st.slider ("Number of Stakeholders", value=3, format="%i", min_value=2, max_value=10, step=1 )
      with col2:
       plteam  = st.slider ("Number of Core Team Members", value=2, format="%i", min_value=2, max_value=15, step=1)
      with col3:
       plusers  = st.slider ("Number of Users", value=10, format="%i", min_value=10, max_value=1000000, step=100)
 
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
      (st.session_state.evsummary, st.session_state.cpi, st.session_state.spi, st.session_state.etc)  = evreport((plbudget + (plbudget *.3)), plbudget, plhours, plavgrate, plexpensecurrency , plstartdate, plenddate, plspend, plreleasesplanned, plreleasescompleted, daystoend, daystoday, timecomplete)
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
     my_expander5 = st.expander("What flexibility does the team have in decisions that impact time, scope, quality or cost, 1 meaning little to no flexibility and 3 is high.  Flexibility in these factors will impact your risk mitigation strategies.  If you have no flexiblity in costs, then your cost risks have high impact on your project.  TIP: The flexibility matrix what constraints are flexible and what project goals must be held.  Place an “X” in the box that reflects the appropriate flexibility.  Some narrative examples are noted below and flagged in the table.  Schedule is least flexible because we must have the release ready by October 1.  Scope (quality) is the most flexible because we can release an upgrade or modification after December 1.  Resources and cost offer a moderate amount of flexibility.  ", expanded=True)
     with my_expander5:
      col1, col2, col3, col4 = st.columns(4)
      with col1:
       plcostconstraint = st.slider('Budget Constraint', min_value=1, max_value=3, value=2, step=1)
      with col2:
       plresourceconstraint = st.slider('Resource Constraint', min_value=1, max_value=3, value=2, step=1)
      with col3:
       pltimeconstraint = st.slider('Schedule Constraint', min_value=1, max_value=3, value=2, step=1)
      with col4:
       plscopeconstraint = st.slider('Scope Constraint', min_value=1, max_value=3, value=2, step=1)
      plscopecontingency  = st.text_area ("Scope Contingency")
      pltimecontingency  = st.text_area ("Schedule Contingency")
      plbudgetcontingency  = st.text_area ("Budget Contingency")
      plresourcecontingency  = st.text_area ("Resource Contingency")
     submit = st.form_submit_button("Save")
     clear = st.form_submit_button(label="Clear Form")
     #update = st.form_submit_button(label="Restore", on_click=update_form(dataframe))
     if submit:
        st.info("The information was updated, thank you for using the PM Monitor.  Use Download to save a copy of your charter offline")
     if clear:
        st.info("The form data was cleared")

    with st.expander(label="UPLOAD CUSTOM SETTINGS / DATA", expanded=False):
            download_upload_settings()
def download_upload_settings():
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
            if saved_settings.iloc[i, 1].startswith('pl'):
              st.session_state[saved_settings.iloc[i, 1]] = saved_settings.iloc[i, 2]
              st.write(st.session_state[saved_settings.iloc[i, 1]])
        return

    button_apply_settings = col2.button(label="Apply Settings",
                                        on_click=upload_saved_settings,
                                        args=(uploaded_settings,),
                                        help="Click to Apply the Settings of the Uploaded file.\\\n"
                                             "Please start by uploading a Settings File below")


