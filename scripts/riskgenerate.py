import json
import pandas as pd
import streamlit as st

def get_impact(value):
   impact = '1-High'
   if value == 3:
     impact = '2-Moderate'
   if value == 3:       
     impact = '3-Low'
   return(impact)

def calculate_risks_json(phasenumber, SPI, CPI, engagementscoreteam, sentimentscoreteam, retention, scopechange, earnedvalue, roi, latestart, inspectfail):

   risks = pd.read_csv('files/risksver4.csv')

   rows = len(risks)
   risks.loc[0:rows,['riskselect']] = ['Y']


   currentphase =  str(phasenumber) + '-' + st.session_state.thepmphasename

   # Find issues in current phase based on trigger
   if 1 < earnedvalue < 20:
      risks.loc[(risks['risktrigger'] == "earnedvalue") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if inspectfail > 0:
      risks.loc[(risks['risktrigger'] == "inspectfail") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if latestart > 0:
      risks.loc[(risks['risktrigger'] == "latestart") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if 1 < roi < 130:
      risks.loc[(risks['risktrigger'] == "roi") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if 1 < engagementscoreteam < 80:
      risks.loc[(risks['risktrigger'] == "engagement") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if 1 < sentimentscoreteam < 80:
      risks.loc[(risks['risktrigger'] == "sentiment") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   #if CPI > 1:
   #   risks.loc[(risks['risktrigger'] == "cpipositive") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if CPI < 1:
      risks.loc[(risks['risktrigger'] == "cpi") & (currentphase == risks['risktimeline']), 'riskselect'] = "I"
   if SPI < 1:
      risks.loc[(risks['risktrigger'] == "spi") & (currentphase == risks['risktimeline']), 'riskselect'] = "I"
   if scopechange > 0:
      risks.loc[(risks['risktrigger'] == "scopechange") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if 1 < roi < 20:
      risks.loc[(risks['risktrigger'] == "roi") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"
   if retention > 0:
      risks.loc[(risks['risktrigger'] == "retention") & (currentphase == risks['risktimeline'] ), 'riskselect'] = "I"

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
   risks.loc[risks['riskclassification'] == "Cost", 'riskimpact'] = impact

   #  recacalculate score 
   #  set the score value and count scores and risktable
   #for i in range (0, rows):
   #  risks.at[i, 'riskimpact'] = 'dummy'
   #     risks.at[i, 'riskscore'] = '3-Lowest'
   issuecount = sum(risks['riskselect'] == 'I')
   riskcount = sum(risks['riskselect'] == 'Y')
   closedcount = sum(risks['riskselect'] == 'N')
   avoidcount = sum(risks['riskresponse'] == 'Avoid')
   risktotal = len(risks)

   risksummary = f'In Phase {phasenumber}, there are {riskcount} risks identified.  {issuecount} risks have been triggered and are possible issues.  {avoidcount} risks have planned mitigation or avoidance strategies. {closedcount} risks from previous phases have been closed. '

   st.write(risksummary)
   st.write("Stats", risktotal, issuecount, closedcount)

   return(risks, issuecount, riskcount, risktotal, risksummary)

#  get the risks and set the current value of probability and impact
#  using probability in the plan, set (scope risk)
#  if plan has contingency, set to avoid, otherwise accept, decrease impact
#  using quality failure, increase probability
#  using changes, increase probability
#  using negative sentiment increase probability and engagement low increase
#  issues probablity high, not avoid, risk high
