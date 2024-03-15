import streamlit as st
import pandas as pd 
import plotly.express as px
from cheche_pm import Project
from  PIL import Image
import io 
import graphviz
import altair as alt
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
from scripts.thepmutilities import reporttitle, gradiant_header
# https://medium.com/@luisfernandopa1212/efficient-project-scheduling-with-python-the-critical-path-method-19a3f8235f91
# https://pypi.org/project/cheche-pm/###Risk_Analysis
# https://codepal.ai/code-generator/query/DewVO5lk/python-cpm-algorithm
# https://github.com/vamsi-aribandi/PERTgen/blob/master/pert.py
st.session_state.update(st.session_state)
st.set_option('deprecation.showPyplotGlobalUse', False)

def make_pert_chart(graph, startTimes, completionTimes, slackTimes, criticalPaths):
    
    criticalEdges = defaultdict(list)
    
    for path in criticalPaths:
        for i in range(len(path) - 1):
            criticalEdges[path[i] + path[i+1]] = True
    
    g = nx.DiGraph()
    labelsDict = {}
    for parent in graph:
        for child in graph[parent]:
            parentStr = '{}/{}/{}'.format(startTimes[parent], completionTimes[parent], slackTimes[parent])
            childStr = '{}/{}/{}'.format(startTimes[child], completionTimes[child], slackTimes[child])
            labelsDict[parent] = parentStr
            labelsDict[child] = childStr
            if criticalEdges[parent + child]:
                g.add_edge(parent,child, color = 'red')
            else:
                g.add_edge(parent,child, color = 'black')
    pos=nx.shell_layout(g)
    for task in startTimes:
        x, y = pos[task]
        plt.text(x,y+0.1,s=labelsDict[task], bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
    print(nx.info(g))
    
    edges = g.edges()
    colors = [g[u][v]['color'] for u,v in edges]
    
    nx.draw(g, pos, edges = edges,with_labels = True, edge_color = colors)
    plt.savefig('pert.png', bbox_inches = 'tight')
    #plt.show()
    st.pyplot(fig)

def make_gantt_chart(graph, startTimes, completionTimes, durations, slackTimes):
    
    fig, ax = plt.subplots()
    y_values = sorted(startTimes.keys(), key = lambda x: startTimes[x])
    y_start = 40
    y_height = 5
    for value in y_values:
        ax.broken_barh([(startTimes[value], durations[value])], (y_start, y_height), facecolors = 'blue')
        ax.broken_barh([(completionTimes[value], slackTimes[value])], (y_start, y_height), facecolors = 'red')
        ax.text(completionTimes[value] + slackTimes[value] + 0.5,y_start + y_height/2, value)
        y_start += 10
    ax.set_xlim(0, max(completionTimes.values()) + 5)
    ax.set_ylim(len(durations)*20)
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    i = 5
    y_ticks = []
    y_ticklabels = []
    while i < len(durations)*20:    
        y_ticks.append(i)
        i += 10
    ax.set_yticks(y_ticks)
    plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left='off',         # ticks along the top edge are off
    labelleft='off') # labels along the bottom edge are off
    plt.savefig('gantt.png', bbox_inches = 'tight')
    st.pyplot(fig)

def find_paths(graph, node, slackTimes, paths):
    if not graph[node]:
        paths[-1].append(node)
        paths.append([])
        #print(node)
        return
    elif slackTimes[node] == 0:
        paths[-1].append(node)
        #print('{} -> '.format(node), end = '')
        for nxt in graph[node]:
            find_paths(graph, nxt, slackTimes, paths)

# https://github.com/sanatsingh/Critical-Path-Method-SE/blob/master/ca_2.py
# https://levelup.gitconnected.com/how-to-create-a-multi-layer-gantt-chart-using-plotly-e7d7f158938c

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Work Breakdown Activities",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

gradiant_header ('The PM Monitor Activity Analysis')
if 'thepmheader' not in st.session_state:
      st.error('Plan is missing. Please enter or import a plan')
      st.stop()

reporttitle("Task Analysis", st.session_state['thepmheader'])

st.write("The PM monitor activity analysis is not intended as a replacement to your task management system.  Instead it is used to analyse the information to provide insight into potential issues with top down planning. In top down planning, management or sales create a detailed list of activities and decisions about timeline, features and cost/effort.  In bottom up planning, there is a goal however activity definintion and decisions are left to the team.   However you plan, remember to not try to be too detailed, and remember to plan for change.  ")


st.subheader('Gantt and WBS (Work Breakdown Structure)')

uploaded_file = st.file_uploader("WBS is a deliverable orientied hierarchical decomposition of work to be executed by the project team.  Fill out the project plan activities and upload your file here. After you upload the file, you can edit your activities within the app.  If you are performing a fixed price or have a complex project to manage, you will want to create a WBS and map the related activities so that you can assign work concurrently to multiple team members and to link work and notify team members when their work can start.   The tasks are related to the project objectives and completion of the work will create the required deliverables. ", type=['csv'])
st.write("Analyse the results and update the plan and status.  Monitor activities that are late and on the critical path, activities that are late and not assigned, monitor the load of resources.  If you are tracking time, monitor overall estimate to completion rates")

if uploaded_file is not None:
    Tasks=pd.read_csv(uploaded_file, quotechar='"', delimiter=',', skipinitialspace=True, keep_default_na=False)
    st.warning('WBS loading from file')
else:
    Tasks = pd.read_csv('files/tasks.csv', sep=',')

# fix missing values
values = {'pr': 'Start', 'Duration': int(1), 'Assign': 'Team', 'Completion Pct': 0}
Tasks.fillna(value=values, inplace=True)
#new_df = df.drop_duplicates(subset='ORDER ID')
Tasks = Tasks.astype({'Duration':'int'})

# map the people to columns
assigned = Tasks.Assign.unique().tolist()
max_resources = len(assigned)
max_array = [1]*len(assigned)
for x in assigned:
    Tasks[x] = 0
    Tasks.loc[Tasks["Assign"] == x, x] = 1

p = Project()
oppdict = {"Start": 0, "End": 0}
pesdict = {"Start": 0, "End": 0}
#p.add_activity(activity_name='A',activity_duration=2,activity_precedence = [None], activity_resources= [2,4,5])
for index, row in Tasks.iterrows():
   # handle more than one
   var = str(row['pr'])
   prec = list(var.split(" "))
   if var == "":
     prec = ["Start"] 
   index = assigned.index(row['Assign'])
   rlist = [0]*len(assigned)
   rlist[index] = 1
   cost = int(row['Duration']*st.session_state.plnavgrate*5)
   p.add_activity(a_desc=row['Description'],activity_name=row['ac'],activity_duration=row['Duration'],activity_precedence = prec, activity_resources= rlist, activity_cost=cost)
   #  apply estimate confidence
   oppdict[row['ac']] = int(row['Duration'] * .75)
   pesdict[row['ac']] = int(row['Duration'] * 1.5)
#st.write(oppdict)

PROJECT = p.create_project_dict()

Tasks_cpm = p.CPM(verbose=False)
Tasks_cp = p.get_critical_path()
Tasks_sched = pd.DataFrame(p.cpm_schedule).T

#st.write("Priority list")
PL = p.get_priority_list(priority_rule= 'MAXF',save=True)

#st.write("SSG")
psg = p.SSG(PL,max_resources=max_array,verbose=False)
#psg = p.PSG(PL,max_resources=max_array,verbose=False)
#st.table(psg)

opt=.5
pess = 1.25
#st.write("Monte Carlo Simulation")
#mc = p.monte_carlo_cpm_detailed(optimistic=oppdict,pessimistic=pesdict, NumberIterations=10)
#st.write(mc)

#plt1 = p.plot_network_diagram(plot_type = 'nx')
#st.pyplot(plt1, use_container_width=True)

#st.write("Resources")
res = p.get_resources()
#st.write(res)

#  start WBS at end of design
startdate = st.session_state.pldstartdate.strftime("%Y-%m-%d")
firstdate = st.session_state.pldstartdate 
todaydate = datetime.now()

#best_heuristic = PROJECT.run_all_pl_heuristics()[psg]
Tasks_dates = p.generate_datetime_schedule(solution = psg,start_date=startdate,weekends_work=False,max_resources=max_array,verbose=False)
Project_dates = pd.merge(Tasks_dates, Tasks, left_index=True, right_on='ac')

#st.dataframe(Project_dates)
#plt2= p.plot_date_gantt(Tasks_dates, plot_type = 'matplotlib')
#st.pyplot(plt2, use_container_width=True)
#plt3 = p.plot_resource_levels(psg)
#st.pyplot(plt3)
#plt4 = p.RCPSP_plot(psg,resource_id=0)
#st.pyplot(plt4)

# do not need this any longer
graph = defaultdict(list)
duration = {}

# fix missing data
Project_dates.loc[Project_dates['Completion Pct'] == "", 'Completion Pct'] = "0"
Project_dates['Completion Pct'] = Project_dates['Completion Pct'].astype('int')
    # input start, duration, type, name
    #Tasks['Start'] = Tasks['Start'].astype('datetime64[ns]')
    #Tasks['Finish'] = Tasks['Finish'].astype('datetime64[ns]')
    #Tasks['Duration'] = Tasks['Duration'].astype('int')
    #Tasks['Duration'] = Tasks['Duration'].fillna(0)
    # force type to int
    #firstdate = Tasks['Start'].iloc[0].date()
    # firstdate = (st.session_state.ldstartdate)
    #daysoffset = (st.session_state['pldstartdate']-firstdate).days
    # get diff startdate and firstdate
    # Tasks['Start'] = firstdate
    #Tasks['Start'] = Tasks['Start'] + pd.Timedelta(days=daysoffset)
    #Tasks['Finish'] = Tasks['Start'] + pd.to_timedelta(Tasks['Duration'], unit='D') 
    #Tasks = st.dataframe( Tasks[Tasks['Type'] == 'Milestone'] )
    #Tasks.loc[Tasks['pr'] == "Start", 'pr'] = "plan"

tottasks = len(Tasks) 
latetasks = closedtasks = cpmlate = 0
    #myissues = (Project_dates[Project_dates['riskselect'] == 'I'])
    #latetasks = ((Project_dates['EF_date'].value_counts()[True]))
closedtasks = [(Project_dates['Completion Pct'] == 100)]
latetasks = (Project_dates["ES_date"] < pd.to_datetime(todaydate)) & ((Project_dates['Completion Pct'] == 0))
cpmlate = (Project_dates["EF_date"] < pd.to_datetime(todaydate)) & ((Project_dates['Completion Pct'] == 0))
tasksnow = Project_dates[(Project_dates["EF_date"] > pd.to_datetime(todaydate))  & (Project_dates["ES_date"] < pd.to_datetime(todaydate)) ]

# show the counters
col3, col4, col5, col6 = st.columns(4)
col3.metric("Total Tasks", tottasks)
col4.metric("Late Start", len(latetasks))
col5.metric("Critical Path Late", len(cpmlate))
col6.metric("Completed Tasks", len(closedtasks))


conditions = [
    (Project_dates['Completion Pct'] == 0),
    (Project_dates['Completion Pct'] >= 1) & (Project_dates['Completion Pct'] < 100),
    (Project_dates['Completion Pct'] == 100)
    ]

    # create a list of the values we want to assign for each condition
values = ['NotStarted', 'InProgress', 'Completed']
Project_dates['Status'] = np.select(conditions, values)

st.subheader("Mindmap Critical path")

st.write("The critical path can change in a project, monitoring the critical path is essential to verify that the end date is feasible.  Using the critical path and the estimate to complete, verify that the end date has not changed" )
    # Create a graphlib graph object
graph = graphviz.Graph()
graph.attr('edge', shape='box', style='filled', color='lightgrey')
for index, row in Tasks.iterrows():
  dep = str(row['pr']).split()
  for xdep in dep:
    graph.node(str(row['ac']), shape = "box", fillcolor = "lightgrey", style = "filled")
    graph.edge(xdep, str(row['ac']), label=str(row['Duration']))
st.graphviz_chart(graph)

st.subheader("Late start tasks")
st.write("Show 5 tasks that are late, percentage complete is 0 and start date is less than the report date")
    #st.dataframe(Tasks[(Tasks["Start"] < pd.to_datetime(todaydate)) & (Tasks["Status"] == 'NotStarted')][['ac', 'Duration', 'Assign', 'Start']])
    #display(dataFrame[(dataFrame['Salary']>=100000) & (dataFrame['Age']<40) & dataFrame['JOB'].str.startswith('P')][['Name','Age','Salary']])
st.subheader("What is the team working on now")
columns = ['ac', 'Duration','Assign', 'Description']
st.write(tasksnow[columns])
st.subheader("Size of Product Build in days")
totalbuild = Project_dates['Duration'].sum()
totalcomplete = Project_dates.loc[Project_dates['Status'] == 'Completed', 'Duration'].sum()
st.write(totalbuild)
st.write(totalcomplete)
    #st.metric("Total build", totalbuild, totalcomplete)
st.dataframe( Project_dates[Project_dates['Completion Pct'] == 100][columns])

st.subheader("Resource Load")
e = alt.Chart(Project_dates.dropna()).mark_bar().encode(
       x='Assign',
       y='sum(D)',
       color='D'
    )
st.altair_chart(e, use_container_width=True)
st.write(" ")

    #Main interface - section 3
    #st.subheader('Step 3: Generate the Gantt chart')
Project_dates['Task'] = Project_dates.index
 
    #Options = st.selectbox("View Gantt Chart by:", ['Assign','Completion Pct'],index=0)
    #if st.button('Generate Gantt Chart'): 
    #st.plotly_chart(fig, use_container_width=True)  #Display the plotly chart in Streamlit

st.subheader("Visualation of WBS")
gantt1 = alt.Chart(Project_dates).mark_bar().encode(
      x=alt.X('ES'),
      x2=alt.X2('EF'),
      y=alt.Y('ac', sort=None, title="Activity"),
      color=alt.Color('critical', scale=alt.Scale(scheme='redyellowblue'))
    )
st.altair_chart(gantt1, use_container_width=True)

st.subheader("Visualation of WBS")
gantt = alt.Chart(Project_dates.dropna()).mark_rect().encode(
       y=alt.Y('ac', sort=None, title="Activity"),
       x=alt.X('monthdate(ES_date):O'),
       x2=alt.X2('monthdate(EF_date):O'),
       color=alt.Color('sum(D)', scale=alt.Scale(scheme='redyellowblue'))
    ) 
st.altair_chart(gantt, use_container_width=True)

st.subheader("Resource Committment Matrix")
heatmap = alt.Chart(Project_dates.dropna()).mark_rect().encode(
       y=alt.Y('Assign').title("Resource"),
       x=alt.X('monthdate(ES_date):O', axis=alt.Axis(tickCount=4)),
       x2=alt.X2('monthdate(EF_date):O'),
       color=alt.Color('sum(D)', scale=alt.Scale(scheme='redyellowblue'))
    ) 
st.altair_chart(heatmap, use_container_width=True)
st.write("The total hours committed and when are displayed")

st.write(Project_dates)

