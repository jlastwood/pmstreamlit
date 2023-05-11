import json
import pandas as pd

def calculate_risks_json(risks, phasenumber, SPI, CPI, engagementscoreteam, sentimentscoreteam, retention, scopechange, earnedvalue, roi, latestart, inspectfail):
   for d in risks:
        d['riskselect'] = 'Y'
        # timeframe when risk will have an impact
        # the risk probablility can be 0 when risk has elapsed

   selectedrisks = [d for d in risks if d['riskselect'] == 'Y']

    #  set the score value and count scores and risktable
   for d in selectedrisks:
        d['riskscore'] = '3-Lowest'
        if d['riskimpact'] == '3' or d['riskprobability'] == '3':
           d['riskscore'] = '1-Highest'
        if d['riskimpact'] == '2' or d['riskprobability'] == '2':
           d['riskscore'] = '2-Moderate'
        if d['riskimpact'] == '' and d['riskprobability'] == '':
           d['riskscore'] = '2-Moderate'

        if d['riskprobability'] == '1':
           d['riskprobability'] = '1-High'
        if d['riskprobability'] == '2':
           d['riskprobability'] = '2-Moderate'
        if d['riskprobability'] == '3':
           d['riskprobability'] = '3-Low'
        if d['riskimpact'] == '1':
           d['riskimpact'] = '1-High'
        if d['riskimpact'] == '2':
           d['riskimpact'] = '2-Moderate'
        if d['riskimpact'] == '3':
           d['riskimpact'] = '3-Low'

         # 1,3,5, and 9
        if (d['risktimeline'] == '1' and phasenumber > 2) or (d['risktimeline'] == '3' and phasenumber > 4) or (d['risktimeline'] == '5' and phasenumber > 5):
           d['riskprobability'] = pd.NA
           d['riskimpact'] = pd.NA
           d['riskresponse'] = pd.NA
           d['riskselect'] = 'N'
           d['riskscore'] = pd.NA
           d['riskowner'] = pd.NA
           d['risktrigger'] = pd.NA
        if d['risktimeline'] == '1':
           d['risktimeline'] = '1-Plan'
        if d['risktimeline'] == '3':
           d['risktimeline'] = '2-Design'
        if d['risktimeline'] == '5':
           d['risktimeline'] = '3-Build'
        if d['risktimeline'] == '9':
           d['risktimeline'] = '5-Accept'

   return(selectedrisks)

#  get the risks and set the current value of probability and impact

#  using probability in the plan, set (scope risk)

#  if plan has contingency, set to avoid, otherwise accept, decrease impact

#  using CPI and SPI, if negative, increase probabilyt, if positive decrease probability

#  using quality failure, increase probability

#  using changes, increase probability

#  using negative sentiment increase probability and engagement low increase

#  issues probablity high, not avoid, risk high

