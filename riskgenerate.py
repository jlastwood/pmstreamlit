import json
import pandas as pd

def calculate_risks_json(risks, phasenumber):
   for d in risks:
        d['riskselect'] = 'Y'
        # timeframe when risk will have an impact
        # the risk probablility can be 0 when risk has elapsed

   selectedrisks = [d for d in risks if d['riskselect'] == 'Y']

    #  set the score value and count scores and risktable
   for d in selectedrisks:
        d['riskscore'] = 'Lowest'
        if d['riskimpact'] == '3' or d['riskprobability'] == '3':
           d['riskscore'] = 'Highest'
        if d['riskimpact'] == '1' or d['riskprobability'] == '1':
           d['riskscore'] = 'Lowest'
        if d['riskimpact'] == '2' or d['riskprobability'] == '2':
           d['riskscore'] = 'Moderate'
        if d['riskimpact'] == '' and d['riskprobability'] == '':
           d['riskscore'] = 'Moderate'

        if d['risktimeline'] < '4' and phasenumber > 2:
           d['riskprobability'] = pd.NA
           d['riskimpact'] = pd.NA
           d['riskresponse'] = pd.NA
           d['riskselect'] = 'N'
           d['riskscore'] = pd.NA
   return(selectedrisks)

#  get the risks and set the current value of probability and impact

#  using probability in the plan, set (scope risk)

#  if plan has contingency, set to avoid, otherwise accept, decrease impact

#  using CPI and SPI, if negative, increase probabilyt, if positive decrease probability

#  using quality failure, increase probability

#  using changes, increase probability

#  using negative sentiment increase probability and engagement low increase

#  issues probablity high, not avoid, risk high

