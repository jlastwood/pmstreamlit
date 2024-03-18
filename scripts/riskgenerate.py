import json
import pandas as pd
import streamlit as st

def get_risk_triggers():
     risktriggers = ['Inflation', 'Changes', 'Earned Value', 'Sentiment', 'Engagement', 'CPI', 'SPI', 'Inspection', 'ROI', 'Late Start', 'Climate', 'Unemployment', 'Business Climate', 'Country Risk']
     risktriggersamber = [5,  1,  0,  70,  80,  1, 1,  3,  30, 3,  1,  8,  'B',  'B' ]
     risktriggersred = [10,  5,  0,  50,  50,  .8, .7,  5,  10, 5,  .8,  8,  'E',  'E' ]
     #riskt = {'Trigger': (risktriggers[i], 'Amber': risktriggersamber[i], 'Red': risktriggersred[i]) for i in range(0, len(risktriggers))]
     riskd = {'Trigger': risktriggers, 'Amber': risktriggersamber, 'Red': risktriggersred} 
     riskt = pd.DataFrame(riskd)
     #riskt.set_index('Trigger', inplace=True)
     return(riskt)


def get_impact(value):
   impact = '1-High'
   if value == 3:
     impact = '2-Moderate'
   if value == 2:       
     impact = '3-Low'
   if value == 1:       
     impact = '3-Low'
   return(impact)

def calculate_risks_json():

   # get the trigger values from the controls
   triggers = get_risk_triggers()

   # get the values from the plan
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
   roi = st.session_state.thepmannualroi
   latestart = st.session_state.plnactiveses
   inspectfail = st.session_state.plntestsfailed

   # currently this is an input file
   risks = pd.read_csv('files/risksver4.csv')

   rows = len(risks)
   risks.loc[0:rows,['riskselect']] = ['Y']

   currentphase =  str(phasenumber) + '-' + st.session_state.thepmphasename
   if currentphase == '5-Accept':
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build;4-Inspect;5-Accept") , 'risktimeline'] = currentphase
   if currentphase == '4-Inspect':
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build;4-Inspect") , 'risktimeline'] = currentphase
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build;4-Inspect;5-Accept") , 'risktimeline'] = currentphase
   if currentphase == '3-Build':
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build"), 'risktimeline'] = currentphase
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build;4-Inspect") , 'risktimeline'] = currentphase
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build;4-Inspect;5-Accept") , 'risktimeline'] = currentphase
   if currentphase == '2-Design':
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build") , 'risktimeline'] = currentphase
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build;4-Inspect") , 'risktimeline'] = currentphase
     risks.loc[(risks['risktimeline'] == "2-Design;3-Build;4-Inspect;5-Accept") , 'risktimeline'] = currentphase

   # Find issues in current phase based on trigger
   if 1 < earnedvalue < 20:
      risks.loc[(risks['risktrigger'] == "earnedvalue") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   inspectvalue = triggers.loc[triggers['Trigger'] == 'Inspection', 'Amber'].values[0]
   if inspectfail > inspectvalue:
      risks.loc[(risks['risktrigger'] == "inspectionfailure") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if latestart > 0:
      risks.loc[(risks['risktrigger'] == "latestart") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   roivalue = triggers.loc[triggers['Trigger'] == 'ROI', 'Amber'].values[0]
   if  roi < roivalue:
      risks.loc[(risks['risktrigger'] == "roi") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if 1 < engagementscoreteam < 80:
      risks.loc[(risks['risktrigger'] == "engagement") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   sentimentvalue = triggers.loc[triggers['Trigger'] == 'Sentiment', 'Amber'].values[0]
   if 1 < sentimentscoreteam < sentimentvalue:
      risks.loc[(risks['risktrigger'] == "sentiment") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   #if CPI > 1:
   #   risks.loc[(risks['risktrigger'] == "cpipositive") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   cpivalue = triggers.loc[triggers['Trigger'] == 'CPI', 'Amber'].values[0]
   if CPI < cpivalue:
      risks.loc[(risks['risktrigger'] == "cpi") & (currentphase == risks['risktimeline']), 'riskselect'] = "I"
   spivalue = triggers.loc[triggers['Trigger'] == 'SPI', 'Amber'].values[0]
   if SPI < spivalue:
      risks.loc[(risks['risktrigger'] == "spi") & (currentphase == risks['risktimeline']), 'riskselect'] = "I"
   if scopechange > 0:
      risks.loc[(risks['risktrigger'] == "scopechange") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if 1 < roi < 20:
      risks.loc[(risks['risktrigger'] == "roi") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if retention > 0:
      risks.loc[(risks['risktrigger'] == "retention") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"

   risks.loc[(risks['riskselect'] == "I"), 'riskresponse'] = "Mitigate"
   # if past phase then close risks
   if phasenumber > 1:
      risks.loc[risks['risktimeline'] == "1-Plan", 'riskprobability'] = pd.NA 
      risks.loc[risks['risktimeline'] == "1-Plan", 'riskselect'] =  "N"
      risks.loc[risks['risktimeline'] == "1-Plan", 'riskresponse'] =  pd.NA
   if phasenumber > 2:
      risks.loc[risks['risktimeline'] == "2-Design", 'riskprobability'] = pd.NA 
      risks.loc[risks['risktimeline'] == "2-Design", 'riskselect'] =  "N"
      risks.loc[risks['risktimeline'] == "2-Design", 'riskresponse'] = pd.NA 
   if phasenumber > 3:
      risks.loc[risks['risktimeline'] == "3-Build", 'riskprobability'] = pd.NA 
      risks.loc[risks['risktimeline'] == "2-Design;3-Build", 'riskprobability'] = pd.NA 
      risks.loc[risks['risktimeline'] == "3-Build", 'riskselect'] =  "N"
      risks.loc[risks['risktimeline'] == "2-Design;3-Build", 'riskselect'] = "N"
      risks.loc[risks['risktimeline'] == "3-Build", 'riskresponse'] = pd.NA 
      risks.loc[risks['risktimeline'] == "2-Design;3-Build", 'riskresponse'] = pd.NA
   if phasenumber > 4:
      risks.loc[risks['risktimeline'] == "4-Inspect", 'riskprobability'] = pd.NA 
      risks.loc[risks['risktimeline'] == "2-Design;3-Build;4-Inspect", 'riskprobability'] = pd.NA 
      risks.loc[risks['risktimeline'] == "4-Inspect", 'riskselect'] =  "N"
      risks.loc[risks['risktimeline'] == "2-Design;3-Build;4-Inspect", 'riskselect'] =  "N"
      risks.loc[risks['risktimeline'] == "4-Inspect", 'riskresponse'] = pd.NA 
      risks.loc[risks['risktimeline'] == "2-Design;3-Build;4-Inspect", 'riskresponse'] = pd.NA 
   if phasenumber > 5:
      risks.loc[risks['risktimeline'] == "5-Accept", 'riskprobability'] = pd.NA 
      risks.loc[risks['risktimeline'] == "2-Design;3-Build;4-Inspect;5-Accept", 'riskprobability'] = pd.NA 
      risks.loc[risks['risktimeline'] == "5-Accept", 'riskselect'] =  "N"
      risks.loc[risks['risktimeline'] == "2-Design;3-Build;4-Inspect;5-Accept", 'riskselect'] =  "N"
      risks.loc[risks['risktimeline'] == "5-Accept", 'riskresponse'] = pd.NA 
      risks.loc[risks['risktimeline'] == "2-Design;3-Build;4-Inspect;5-Accept", 'riskresponse'] = pd.NA 

   #  fill blanks
   risks['potentialconsequences'] = risks['potentialconsequences'].fillna('None')
   risks['riskmitigationmeasures'] = risks['riskmitigationmeasures'].fillna('None')
   #  setting impact based on plan
   impact = get_impact(st.session_state.plnscoperange)
   risks.loc[risks['riskclassification'] == "Scope", 'riskimpact'] = impact
   risks.loc[risks['riskclassification'] == "Change", 'riskimpact'] = impact
   risks.loc[risks['riskclassification'] == "Stakeholders", 'riskimpact'] = impact
   risks.loc[risks['riskclassification'] == "Requirements", 'riskimpact'] = impact
   impact = get_impact(st.session_state.plnbudgetrange)
   risks.loc[risks['riskclassification'] == "Cost", 'riskimpact'] = impact
   impact = get_impact(st.session_state.plnschedulerange)
   risks.loc[risks['riskclassification'] == "Project", 'riskimpact'] = impact
   impact = get_impact(st.session_state.plnteamrange)
   risks.loc[risks['riskclassification'] == "Team", 'riskimpact'] = impact
   risks.loc[risks['riskclassification'] == "Communicatino", 'riskimpact'] = impact
   impact = get_impact(st.session_state.plnresourcerange)
   risks.loc[risks['riskclassification'] == "Procurement", 'riskimpact'] = impact
   risks.loc[risks['riskclassification'] == "Technology", 'riskimpact'] = impact

   #  recacalculate score 
   #  set the score value and count scores and risktable
   risks.loc[(risks['riskimpact'] == "1-High") | (risks['riskprobability'] == "1-High"), 'riskscore'] = "1-High"
   risks.loc[(risks['riskimpact'] == "2-Moderate") | (risks['riskprobability'] == "2-Moderate"), 'riskscore'] = "2-Moderate"
   risks.loc[(risks['riskimpact'] == "3-Low") | (risks['riskprobability'] == "3-Low"), 'riskscore'] = "3-Lowest"
   # for i in range (0, rows):
   #  risks.at[i, 'riskimpact'] = 'dummy'
   #     risks.at[i, 'riskscore'] = '3-Lowest'
   issuecount = sum(risks['riskselect'] == 'I')
   riskcount = sum(risks['riskselect'] == 'Y')
   closedcount = sum(risks['riskselect'] == 'N')
   avoidcount = sum(risks['riskresponse'] == 'Avoid')
   risktotal = len(risks)

   risksummary = f'In Phase {phasenumber}, there are {riskcount} risks identified.  {issuecount} risks have been triggered and are possible issues.  {avoidcount} risks have planned mitigation or avoidance strategies. {closedcount} risks from previous phases have been closed. '

   st.write(risksummary)
   #st.write("Stats", risktotal, issuecount, closedcount)

   return(risks, issuecount, riskcount, risktotal, risksummary)

#  get the risks and set the current value of probability and impact
#  using probability in the plan, set (scope risk)
#  if plan has contingency, set to avoid, otherwise accept, decrease impact
#  using quality failure, increase probability
#  using changes, increase probability
#  using negative sentiment increase probability and engagement low increase
#  issues probablity high, not avoid, risk high
