#calculate currency risk, weather, political events for the plan analysis

import streamlit as st
#  from forex_python.converter import CurrencyRates
import math
import pandas as pd
# import datetime
from datetime import datetime 
from datetime import date

# https://forex-python.readthedocs.io/en/latest/usage.html
# price of oil because USD is based on oil
# https://docs.quandl.com/docs/python-time-series

def get_grade(score, total):
     
    if score > 0: 
      avg = total/score * 100
    else:
      return("None")
    if avg > 100:
      avg = 0
 
    if avg >= 91 and avg <= 100:
      grade = "A1"
    elif avg >= 81 and avg < 91:
      grade = "A2"
    elif avg >= 71 and avg < 81:
      grade = "B1"
    elif avg >= 61 and avg < 71:
      grade = "B2"
    elif avg >= 51 and avg < 61:
      grade = "C1"
    elif avg >= 41 and avg < 51:
      grade = "C2"
    elif avg >= 33 and avg < 41:
      grade = "D"
    elif avg >= 0 and avg < 33:
      grade = "E"
    return(grade)

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'

# commented out module
def CurrencyRates():
  return

def currencyrisk(projectrevenue, projectcost, projecthours, projectcountries, projectbasecurrency, dateStart, dateEnd):
  #
  # using project countries calculate the impact of currency changes in USD market
  # USD is based on the price of oil, and this impacts global market prices
  # return currencyrisk (y/n),  currencyissue (y/n), currency summary for report
  #
  if projectbasecurrency == 'USD':
    currsummary = 'Project currency in USD, no forex opportunities were calculated'
  if projectbasecurrency != 'USD':
    currencysummary = [1, 0, "summary"] 
    c = CurrencyRates()
    ratenow = c.get_rate('USD', projectbasecurrency) 
    date_obj = dateStart
    # date_obj = datetime(2019, 5, 23, 18, 36, 28, 151012)
    ratebegin = c.get_rate('USD', projectbasecurrency, date_obj)
    ratemidpoint = c.get_rate('USD', projectbasecurrency, date_obj)
  #  when project amount (revenue) is in one currency and most of the costs are in a different currency, you have a forex risk
    costconvert = c.convert('USD', projectbasecurrency, projectcost)
    ratechangenow = ((float(ratenow)-ratebegin)/ratebegin)*100
    costbegin = projectcost * ratebegin
    costnow = projectcost * ratenow
    changenote = ""
    currsummary = ""
    if ratechangenow <= -1:
      changenote = f'<p>Opportunity realized, your local currency is <b>worth more</b></p><div class="text-success" ><i class="fas fa-level-up-alt"></i>Cost</div>'
    if ratechangenow > -1: 
      changenote = f'<p>Risk realized, your local currency is <b>worth less</b></p><div class="text-warning"><i class="fas fa-level-down-alt"></i>Cost</div>'
  # where are you in the project now near the end the currency issue goes away
    currsummary = f'{changenote}<p>The exchange rate is now {ratenow:.3f} and at the beginning of the project the rate was {ratebegin:.3f} for a change of {ratechangenow:.2f} your project { costbegin:,.0f} now costs { costnow:,.2f} with resources and costs in USD and project revenue in {projectbasecurrency}</p>'
  return(currsummary)

# calculate cpi and spi
def evreport(projectrevenue, projectbudget, projecthours, projectrate, projectbasecurrency, dateStart, dateEnd, actualcost, milestoneplanned, milestonecomplete, daystoend, daystoday, timecomplete ):
#  https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/15-9-2/Using-Classic-Clarity-PPM/project-management/create-projects-teams-and-tasks/calculate-earned-value-eac-etc-and-other-metrics.html
#  https://www.projectengineer.net/the-earned-value-formulas/
#  pv = percentage of completed work planned times projectcost
#  ev = percentage complete actual times project cost
#  ac = actual cost
#  sv = ev - pv (negative is behind schedule)
#  spi = ev/pv (less than 1 behind schedule)
#  cv = ev - ac
#  cpi = ev/ac
#  bac = BAC = ((Actuals + Remaining Work) x actual cost
#  when past cost and schedule performace will continue
#  EAC = AC + [(BAC – EV)/(SPI x CPI)]
#  etc = eac - ac
   cpi = 0
   eac = 0
   spi = 0
   etc = 0
   bac = 0
   evmstats = {}
   if projectbudget > 0:
      if milestoneplanned == 0:
         milestoneplanned = 1
      ev = int(projectbudget * (milestonecomplete / milestoneplanned))
      pv = int(projectbudget * (timecomplete / 100))
      acwp = actualcost
      sv = ev - pv
      st.write(sv, ev, pv)
      if pv > 0:
        spi = float(ev/pv)
      cv = ev - acwp
      if acwp > 0:
        cpi = ev/acwp
      if spi > 0 and cpi > 0:
        eac = float(acwp + ((projectbudget - ev)/(spi * cpi)))
      else:
        eac = projectbudget
      etc = float(eac - acwp)
      #  BAC is project budget, only change if approved change in scope
      bac = projectbudget
      if sv < 0:
        svcomment = 'Behind Schedule'
        bcomment = "behind "
        scomment = "negative "
      else:
        svcomment = 'On or ahead of Schedule'
        bcomment = "ahead of "
        scomment = "positive "
      if spi < 1:
        spcomment = "less than "
      else:
        spcomment = "greater than "
      if cv < 0:
        cvcomment = "Over Budget"
      else:
        cvcomment = "On or under Budget"
      if cpi < 1:
        cpicomment = "over budget"
      else:
        cpicomment = "performing well on or under budget "
      #  use markdown
      evsumm = f'**{svcomment} and {cvcomment}**   The project has a current Earned Value of {ev:,.0f} of a total spend to date of {acwp:,.0f}.  {timecomplete}% of the time has elapsed in the schedule.   Planned Value or the total cost of work that should have been done based on the schedule is {pv:,.0f}   Schedule Variance {sv:,.0f} is {scomment}. and Schedule Performance Index is {spi:.2f}% {spcomment} 1. The project is {bcomment} schedule.   Cost Variance is {cv} Cost Variance monitors budget.  The work can be ahead of schedule but over budget.  Cost Performance Index {cpi:.2f}% provides a guide as to the relative amount of the variance. The project is {cpicomment}.   Project Estimate at Completion is now {eac:,.0f} Estimate To Complete {etc:,.0f}.'
 
      
      eac =  acwp + etc
      evmstats = {
       "Budget at Completion": format(bac, ",.0f"),
       "Planned Value (PV)": pv,
       "Earned Value (EV)": ev,
       "Actual Cost (AC)": acwp,
       "Cost Variance": cv, 
       "Schedule Variance": sv, 
       "Cost Performance IndexI": cpi,
       "Schedule Performance Index": spi,
       "Estimate at Completion": format(eac,",.0f"),
       "Variance at Completion": format(bac - eac,",.0f"),
       "Estimate to Complete": format(etc,",.0f")} 

   else:
      evsumm = f'No Earned Value report,  missing budget'

   return(evsumm, cpi, spi, etc, pd.DataFrame([evmstats]))

def switch_cadence(argument):
    switcher = {
        "weekly": 1,
        "quarterly": 12,
        "biweekly": 2,
        "monthly": 4,
    }
    return switcher.get(argument, 1)

def plancomment(dateStart, dateEnd, daystoday, daystoend, timecomplete, coreteam, projectid, projectname, benefits, cadence, prphase, pmname, pmclass):
   weekstotal = (daystoday / 7) 
   weeksend = int(daystoend / 7) 
   cadnumber = cadence
   commentnote = f'Project {projectname} ({projectid}) sponsored by {pmname} is a {pmclass} project.  Project was initiated on {dateStart} and is currently in the {prphase} phase with planned completion in {weeksend:.0f} week(s) on {dateEnd} . Project management reports are delivered every {cadnumber} week(s).  \n  \n '
   return(commentnote)

# weather events
def teamcomment(dateStart, dateEnd, stoday, timecomplete, coreteam):
   commchannel = math.factorial(coreteam)
   commentnote = f'There are {commchannel} communication channels in this project, with a team size of {coreteam}.  The project runs for x weeks'
   return(commentnote)
# political events

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

def reporttitle(reportname, reporttable):
# CSS to inject contained in a string
  hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  # st.markdown("<h3 style='text-align: center; vertical-align: bottom; color: white; background: gray; '>The PM Monitor</h3><br/>", unsafe_allow_html=True)
  st.table(reporttable)

def gradiant_header(content):
  color1 = st._config.get_option('theme.primaryColor')
  color2 = st._config.get_option('theme.secondaryBackgroundColor')
  color3 = st._config.get_option('theme.backgroundColor')
  color1d = st._config.get_option('theme.textColor')
  st.markdown(f'<p style="text-align:center;background-image: linear-gradient(to right,{color1}, {color2});color:{color3};font-size:24px;border-radius:5px;">{content}</p>', unsafe_allow_html=True)

def reporttitleonly(reportname):
  st.markdown("<h3 style='text-align: center; vertical-align: bottom; color: white; background: gray; '>The PM Monitor</h3><br/>", unsafe_allow_html=True)
# Inject CSS with Markdown
#  col1, col2, col3  = st.columns(3)
#  with col1:
#   st.markdown(f'''
#<a target="_self" href={url1}><button style="background-color:#F4A261;text-align:border-radius: 12px; border: 2px solid #4CAF50;center;">Update Plan</button></a>
#''',
#unsafe_allow_html=True)
#  with col2:
#   st.markdown(f'''
#<a target="_self" href={url2}><button style="background-color:#F4A261;text-align:border-radius: 12px; border: 2px solid #4CAF50;center;">Canvas Report</button></a>
#''',
#unsafe_allow_html=True)
#  with col3:
#   st.markdown(f'''
#<a target="_self" href={url3}><button style="background-color:#F4A261;text-align:border-radius: 12px; border: 2px solid #4CAF50;center;">Stoplight Report</button></a>
#''',
#unsafe_allow_html=True)
#  st.markdown("---")
## output the header
  if reportname > " ":
   header="<p style='text-align: center; vertical-align: bottom; color: white; background: green; font-size: 120%;'>" + reportname + "</p>"
   st.markdown(header, unsafe_allow_html=True)
  return()

