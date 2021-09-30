"""Page for viewing the awesome Project canvas"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import pandas as pd
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

def write():
    """Method used to write the page in the app.py file"""
    ast.shared.components.title_awesome("Plan")
    # with st.spinner("Loading  ..."):

    # initialize session state variables
    if 'plnumber' not in st.session_state:
     st.session_state.plnumber = ""

    with st.form("my_plan"):

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
     my_expander0 = st.expander("A project is finite, has a start and and end timeframe and is unique. A project is undertaken to implement change, deliver a new product, service or process.  Outline the timeline and the benefits in the Project Introduction.", expanded=True)
     with my_expander0:
      col6, col7 = st.columns([1, 3])
      with col6:
       plnumber  = st.text_input ("Project ID", value=st.session_state.plnumber, max_chars=10, help="A unique id to identify this project", key="plnumber")
      with col7:
       plname  = st.text_input ("Project Name", help="A short project name for reports", max_chars=50)
      col4, col5 = st.columns(2)
      with col4:
       plpmname  = st.text_input ("Project Manager Name", max_chars=30)
      with col5:
       plspname  = st.text_input ("Product Owner or Sponsor Name", max_chars=30)
      plbenefits  = st.text_input ("What are the Benefits?")
  
     # set some dates
      week  = datetime.timedelta(days = 7)
      daytoday = datetime.date.today()
     
      col1, col2, col3 = st.columns(3)
      with col1:
       plstartdate  = st.date_input ("Start Date", daytoday - (week * 4))
      with col2:
       plenddate  = st.date_input ("End Date", daytoday + (week * 8))
      with col3:
       plreportdate  = st.date_input ("Report Date", daytoday)

      daystoend = (plenddate-plstartdate).days
      daystoday = (daytoday-plstartdate).days
      timecomplete = int(daystoday / daystoend * 100)

      col6, col7 = st.columns([1, 3])
      with col6:
       plcadence = st.radio('Cadence', ('weekly', 'monthly', 'biweekly', 'quarterly'), help="Cadence is the frequence that the project replans and reports on progress.  In a maintenance project you should plan and report quarterly.  In active development projects when investment is higher, you should be planning and reporting weekly")
      with col7:
       plphase = st.radio('Project Phase', ('Conception', 'Planning', 'Launch or Execution', 'Performance and Control', 'Project Close'), help="The phase of the project will determine which risks are higher or may be closed.  In the early phases of the project you have higher technology and cost risks and in later phases you can have engagement and resource risks")
       plannote = plancomment(plstartdate, plenddate, daystoday, daystoend, timecomplete, 3, plnumber, plname, plbenefits, plcadence, plphase)
     st.markdown(" :fireworks: {}".format(plannote), unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Management Report</h4>", unsafe_allow_html=True)

     my_expander1 = st.expander("The Product owner and Project Manager provide a brief insight of accomplishments and challenges in the last period and make note of any stakeholder action items planned for the next period", expanded=True)
     with my_expander1:
       plcsmcomment  = st.text_area ("Product Owner or Sponsor Comments")
       plpmcomment  = st.text_area ("Project Manager Comments")
       plmgmtactions  = st.text_area ("Management Action items in next period", key="plmgmtactions")
       st.session_state.plcomments = "#### Product Owner says:\n" + plcsmcomment + "\n#### Project Manager says:\n" + plpmcomment + "\n#### Stakeholder action items:\n" + plmgmtactions + "\n\nReport date:" + daytoday.strftime("%Y %m %d")
     st.markdown(st.session_state.plcomments)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Scope</h4>", unsafe_allow_html=True)
     my_expander2 = st.expander("The scope information outlines the features that the product should have, and how these features will be delivered, how many milestones, stories and releases are planned ", expanded=True)
     with my_expander2:
      col4, col5 = st.columns(2)
      with col4:
       plscopemusthave  = st.text_input ("Must Have", max_chars=30)
      with col5:
       plscopenicetohave  = st.text_input ("Nice to Have", max_chars=30)
      col4, col5 = st.columns(2)
      with col4:
       plscopeifpossible  = st.text_input ("If Possible", max_chars=30)
      with col5:
       plscopeoutofscope  = st.text_input ("Out of Scope", max_chars=30)
     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Schedule</h4>", unsafe_allow_html=True)
     my_expander6 = st.expander("A project has 5 phases.  Milestones are point in time events that are used to verify if the project is on track.  This is shown using the milestone trend chart. Releases completed result in business value to the users and customer.  Features are defined as stories, stories are SMART,  Specific, Measurable, Achievable, Realistic and have a time frame.  ", expanded=True)
     with my_expander6:
      col4, col5 = st.columns(2)
      with col4:
       plmilestoneplanned  = st.slider ("Number of Milestones Planned", value=3, format="%i", min_value=1, max_value=20, step=1)
      with col5:
       plmilestonecompleted  = st.slider ("Number of Milestones Completed", value=0, format="%i", min_value=0, max_value=20, step=1)
      col1, col2, col3 = st.columns(3)
      with col1:
       plml1planned  = st.date_input ("Conception Planned", plstartdate)
      with col2:
       plml1revised  = st.date_input ("Conception Revised", plstartdate)
      with col3:
       plml1complete  = st.date_input ("Conception Completed", plstartdate)
      col4, col5 = st.columns(2)
      with col4:
       plstoriesplanned  = st.slider ("Number of Stories Planned", value=3, format="%i", min_value=1, max_value=20, step=1)
      with col5:
       plstoriescompleted  = st.slider ("Number of Stories Completed", value=0, format="%i", min_value=0, max_value=20, step=1)
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
      evsummary = evreport((plbudget + (plbudget *.3)), plbudget, plhours, plavgrate, plexpensecurrency , plstartdate, plenddate, plspend, plreleasesplanned, plreleasescompleted, daystoend, daystoday, timecomplete)
     col1, col2, col3 = st.columns(3)
     with col1:
      st_radial('% Complete',timecomplete)
     with col2:
      st_radial('% Spent',(plspend/plbudget*100))
     with col3:
      st_radial('% Effort',(int(plhoursused/plhours*100)))
     st.markdown("<h4 style='text-align: center;'>CPI and SPI report</h4>", unsafe_allow_html=True)
     st.markdown("{}".format(evsummary), unsafe_allow_html=True)

     st.markdown("<h4 style='text-align: center; color: white; background: grey;'>Constraints</h4>", unsafe_allow_html=True)
     my_expander5 = st.expander("What flexibility does the team have in decisions that impact time, scope, quality or cost, 1 meaning little to no flexibility and 3 is high.  Flexibility in these factors will impact your risk mitigation strategies.  If you have no flexiblity in costs, then your cost risks have high impact on your project. ", expanded=True)
     with my_expander5:
      col1, col2, col3 = st.columns(3)
      with col2:
       plcostconstraing = st.slider('Cost Constraint', min_value=1, max_value=3, value=2, step=1)
      col1, col2, col3 = st.columns(3)
      with col1:
       pltimeconstraing = st.slider('Time Constraint', min_value=1, max_value=3, value=2, step=1)
      with col3:
       plscopeconstraing = st.slider('Scope Constraint', min_value=1, max_value=3, value=2, step=1)
     submit = st.form_submit_button("Save")
     if submit:
        st.info("The information was updated, thank you for using the PM Monitor")
     download = st.form_submit_button("Download Analysis")
     df = pd.DataFrame({'numbers': [1, 2, 3], 'colors': ['red', 'white', 'blue']})
     # d = {'Budget': [plbudget], 'Hours': [plhours]} 
     # st.markdown(get_table_download_link(df), unsafe_allow_html=True)
     if download:
        open('df.csv', 'w').write(df.to_csv())
        # st.success("The download is presented in another tab,  thank you for using the PM monitor")
        # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/



