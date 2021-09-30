#  thepmmonitor slack processing

import slack
from slack import WebClient
from slack.errors import SlackApiError
import json, time
from datetime import datetime, timedelta
from collections import Counter

def float_to_datetime(fl):
   flnum = float(fl)
   return datetime.fromtimestamp(flnum)

def get_users(sc):
  try:
    users = sc.api_call( api_method='users.list', json={'limit': '30'})
  except SlackApiError as e:
    if e.response['ok'] is False: 
      clientmessage = "Slack users " + e.response["error"] 
      # print("user error",e.response["error"] )
      return
  return users

def analyse_users(sc):
  users = get_users(sc) 
  duser = 0
  userlist = []
  tzlist = []
  if users:
    for i in users['members']:
      if i['profile']['real_name'] != 'Slackbot':
            # don't display deleted users
            if not i['deleted']:
              if not i['is_bot']:
                # display real name
                # userlist.append((i['profile']['real_name']))
                userlist.append(i['id'])
                tzlist.append((i['tz'])) if i['tz'] not in tzlist else tzlist
            else:
                duser += 1 
  # print("duser", duser, len(userlist), userlist[1:3], tzlist)
  return (duser, len(userlist), tzlist)

def slack_messages_pm(slack_token, selectchannel):

  # Initialize
  # slack_token = "xoxb-"
  # selectchannel = "C01DKKPS5PY"
  # xoxb-1468607639699-1492476234416-xbSeV6LGivaiXKwZf42RU0Cw  (bot)
  # xoxp-1468607639699-1453660456023-2358821896773-f89fe9793027b3e22222dfd06d0e137b  user
  sc = WebClient(slack_token)
  commentdata = ""
  clientmessage = ""
  getchannel = "general"
  datecal = datetime.today() - timedelta(days=7)

  try:
    channels = sc.api_call( api_method='conversations.list', json={'exclude_archived': 'true', 'limit': '20', 'types': 'public_channel,private_channel,mpim,im'})
  except SlackApiError as e:
    if e.response['ok'] is False: 
      clientmessage = "Slack " + e.response["error"] 
      return(commentdata, clientmessage)

  # use all public channelse
  for c in channels['channels']:
    print ("channels ", c['name'], c['is_group'], c['is_private'], c['is_mpim'])
    if c['name'] == selectchannel:
       getchannel = c['id']
    if c['id'] == selectchannel:
       getchannel = c['id']

  try:
    info = sc.conversations_info(channel=getchannel)
  except SlackApiError as e:
    if e.response['ok'] is False: 
      clientmessage = "Slack " + e.response["error"] + " channel " + getchannel
      return(commentdata, clientmessage)

  res = sc.conversations_history(channel=getchannel,limit="1000") 
  clientmessage = "found " + str(len(res['messages'])) + " messages in " + getchannel + selectchannel

  # todo fix this
  while res['has_more']:
    for message in res['messages']:
        time.sleep(1)
    res = sc.conversations_history(channel=getchannel,limit="1000") 

  eusers = [] 
  erecent = [] 
  edates = [] 
  for message in res['messages']:
    time.sleep(1)
    #  all contributions
    eusers.append(message['user']) if message['user'] not in eusers else eusers
    #  contributions in last 2 week
    if float_to_datetime(message['ts']) > datecal:
      erecent.append(message['user']) if message['user'] not in erecent else erecent
    # print("date", float_to_datetime(message['ts'])) 
    # append all the text for analysis
    weekdate=float_to_datetime(message['ts'])
    #edates.append(datetime.strftime("%V", weekdate))

    commentdata += message['text']
    commentdata += ". "

  (duser, cuser, tzlist) = analyse_users(sc)

  cnteusers = Counter(eusers)
  print("engagement", cnteusers.keys(), cnteusers.values())
  cnterecent = Counter(erecent)
  print("engagement recent", cnterecent.keys(), cnterecent.values())
  cntdates = Counter(edates)
  print("engagement dates", cntdates.keys(), cntdates.values())
 
  ensumm=f'{len(cnteusers.keys())} Active users in this project board, with {len(cnterecent.keys())} contributors in the last 7 days.  {duser} users have left. Users are found in {len(edates)} time zones. '
  print ("Engagement", ensumm)  


  return(commentdata, clientmessage)
