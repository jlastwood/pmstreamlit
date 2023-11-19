import streamlit as st
import pandas as pd 
import plotly.express as px
from  PIL import Image
import io 
import graphviz
import altair as alt
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
from scripts.thepmutilities import reporttitle, gradiant_header
# https://medium.com/@luisfernandopa1212/efficient-project-scheduling-with-python-the-critical-path-method-19a3f8235f91
# https://pypi.org/project/cheche-pm/###Risk_Analysis

st.session_state.update(st.session_state)

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
    #  plt.show()
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


reporttitle("Activity", st.session_state['thepmheader'])

st.subheader('Gantt and WBS (Work Breakdown Structure)')
uploaded_file = st.file_uploader("WBS is a deliverable orientied hierarchical decomposition of work to be executed by the project team.  Fill out the project plan activities and upload your file here. After you upload the file, you can edit your activities within the app.  If you are performing a fixed price or have a complex project to manage, you will want to create a WBS and map the related activities so that you can assign work concurrently to multiple team members and to link work and notify team members when their work can start.   The tasks are related to the project objectives and completion of the work will create the required deliverables. ", type=['csv'])
st.write("Analyse the results and update the plan and status.  Monitor activities that are late and on the critical path, activities that are late and not assigned, monitor the load of resources.  If you are tracking time, monitor overall estimate to completion rates")

if uploaded_file is None:
   st.error('WBS missing. Please enter or import a plan')
   st.stop()

if uploaded_file is not None:

    graph = defaultdict(list)
    duration = {}

    Tasks=pd.read_csv(uploaded_file, quotechar='"', delimiter=',', skipinitialspace=True)
    Tasks['Start'] = Tasks['Start'].astype('datetime64[ns]')
    Tasks['finish'] = Tasks['finish'].astype('datetime64[ns]')
    Tasks['du'] = Tasks['du'].astype('int')
    Tasks['du'] = Tasks['du'].fillna(0)
    # force type to int
    firstdate = Tasks['Start'].iloc[0].date()
    # firstdate = (st.session_state.pldstartdate)
    daysoffset = (st.session_state['pldstartdate']-firstdate).days
    # get diff startdate and firstdate
    #Tasks['Start'] = firstdate
    Tasks['Start'] = Tasks['Start'] + pd.Timedelta(days=daysoffset)
    #Tasks['Start'] = Tasks['Start'] + pd.Timedelta(days=daysoffset)
    #Tasks['finish'] = Tasks['Start'] + pd.to_timedelta(Tasks['du'], unit='D') 
    # Tasks = st.dataframe( Tasks[Tasks['Type'] == 'Milestone'] )
    df = Tasks
    #df = Tasks
    #df.replace('-', np.nan)


    for index, row in Tasks.iterrows():
         nodes = row['pr'].split(' ')
         for node in nodes:
               graph[node].append(row['ac'])
         duration[row['ac']] = int(row['du'])

    #duration = {'a': 5, 'b': 3, 'c': 9, 'd': 5, 'e': 9, 'f': 3, 'g': 2, 'End': 2}

    no_axis_title = axis = alt.Axis(title="")
    x_scale = alt.Scale(domain=(st.session_state.pldstartdate.isoformat(), st.session_state.pldenddate.isoformat()), nice=10) 

    tasks = duration.keys()
    # st.write("tasks", tasks) 
    #initialize start times
    startTimes = {}
    #for task in graph:
    #    startTimes[task] = 0
    graph.pop('NONE', None)
    #st.write("tasks", tasks, len(tasks)) 
    #st.write("starttime", startTimes, len(startTimes))
    #st.write("graph", graph)
    #st.write("duration", duration)

    while len(startTimes) < len(tasks): # while any node doesn't have a start time
        for task in tasks: # loop through all tasks
            if task not in startTimes: # if the task doesn't have a start time yet
                startTime = 1 # initialize start time to be some minimum value
                flag = True
                for parent in graph: # look for all tasks it depends on i.e. all nodes pointing to it
                    if task in graph[parent]: # we found a parent
                        if parent in startTimes: # if the parent has a start time, compare it to current max
                            startTime = max(startTime, (startTimes[parent] + duration[parent]))
                        else: # else, one of the parents doesn't have a start time, so we can't calculate start time of current task yet
                            flag = False
                #if flag:
                startTimes[task] = startTime
    
    #st.write('start times: {}'.format(startTimes))

    # calculate completion times
    completionTimes = {}
    for task in tasks:
        completionTimes[task] = startTimes[task] + duration[task]
    
    #st.write('completion times: {}'.format(completionTimes))

    # calculate slack times
    slackTimes = {}
    for task in tasks:
        slackTime = 9999999999999999999;
        for node in graph[task]:
            slackTime = min(slackTime, startTimes[node] - completionTimes[task])
        if not graph[task]:
            slackTimes[task] = 0
        else:
            slackTimes[task] = slackTime
    
    #st.write('slack times: {}'.format(slackTimes), type(slackTimes), len(slackTimes))
    
    criticalPaths = [[]]
    #for node in graph:
    #    if startTimes[node] == 0:
    #        find_paths(graph, node, slackTimes, criticalPaths)
    #criticalPaths.pop()
    st.write(criticalPaths)

    # push lists back to data frame but need to add extra line for end
    abca = list(slackTimes.values())
    #abca.append(0)
    Tasks['slack'] = abca
    abcb = list(startTimes.values())
    #abcb.append(0)
    Tasks['startdays'] = abcb
    Tasks['startdays'] = pd.to_numeric(Tasks['startdays'])
    abcc = list(completionTimes.values())
    #abcc.append(0)
    Tasks['enddays'] = abcc
    Tasks['enddays'] = pd.to_numeric(Tasks['enddays'])

    # now set the start and end dates
    firstdate = st.session_state.pldstartdate 
    todaydate = datetime.now()
    st.write(firstdate, todaydate)
    # daysoffset = (st.session_state['pldstartdate']-firstdate).days
    # get diff startdate and firstdate

    Tasks['Start'] = Tasks['Start'] + pd.to_timedelta(Tasks['startdays'], unit='d')
    Tasks['finish'] = Tasks['Start'] + pd.to_timedelta(Tasks['enddays'], unit='d')
    Tasks['Status'] = Tasks['Start'] + pd.to_timedelta(Tasks['enddays'], unit='d')
    conditions = [
    (Tasks['Completion Pct'] == 1),
    (Tasks['Completion Pct'] > 1) & (Tasks['Completion Pct'] < 100),
    (Tasks['Completion Pct'] == 100)
    ]

# create a list of the values we want to assign for each condition
    values = ['NotStarted', 'InProgress', 'Completed']
    #Tasks['Status'] = np.select(conditions, values)
    Tasks['Status'] = ['1','2']
    Tasks["Late"] = ((Tasks["Start"] < pd.to_datetime(todaydate)) &  (Tasks["Status"] != 'Completed'))

    st.write("Filter or view activities") 
    st.write(Tasks)

    #grid_response = AgGrid(
    #    Tasks,
    #    editable=False, 
    #    height=300, 
    #    filter=True,
    #    )

    st.subheader("Mindmap Critical path")

    st.write("The critical path can change in a project, monitoring the critical path is essential to verify that the end date is feasible.  Using the critical path and the estimate to complete, verify that the end date has not changed" )
    # Create a graphlib graph object
    graph = graphviz.Digraph()
    graph.attr('edge', shape='box', style='filled', color='lightgrey')
    for index, row in Tasks.iterrows():
      dep = str(row['pr']).split()
      for xdep in dep:
        graph.node(str(row['ac']), shape = "box", fillcolor = "lightgrey", style = "filled")
        graph.edge(xdep, str(row['ac']), label=str(row['du']))
    st.graphviz_chart(graph)

    st.subheader("Late start tasks")
    st.write("Show 5 tasks that are late, percentage complete is 0 and start date is less than the report date")
    st.dataframe( Tasks[ (Tasks['Late'] == 1) & (Tasks['Status'] == "NotStarted") ][['Late','ac','du', 'Team','name']])
    #display(dataFrame[(dataFrame['Salary']>=100000) & (dataFrame['Age']<40) & dataFrame['JOB'].str.startswith('P')][['Name','Age','Salary']])
    st.subheader("Work not complete")
    st.write("Show 5 tasks that are not completed, percentage complete is less than 100 and end date is less than the report date")
    st.subheader("Size of Project Build")
    st.write("How many tasks are not estimated")

    columns = ['ac', 'Type']
    st.dataframe( Tasks[Tasks['Completion Pct'] == 100] )

    st.subheader("Resource Load")
    st.write("Show the total resource committment, start and end date of the resource, total hours, complete")
    
    #Main interface - section 3
    st.subheader('Step 3: Generate the Gantt chart')
    
    Options = st.selectbox("View Gantt Chart by:", ['Team','Completion Pct'],index=0)
    if st.button('Generate Gantt Chart'): 
        fig = px.timeline(
                        df, 
                        x_start="Start", 
                        x_end="finish", 
                        y="ac",
                        color=Options,
                        hover_name="name"
                        )

        fig.update_yaxes(autorange="reversed")          #if not specified as 'reversed', the tasks will be listed from bottom up       
        fig.update_layout(
                        title='Project Plan Gantt Chart',
                        hoverlabel_bgcolor='#DAEEED',   #Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
                        bargap=0.2,
                        height=600,              
                        xaxis_title="", 
                        yaxis_title="",                   
                        title_x=0.5,                    #Make title centered                     
                        xaxis=dict(
                                tickfont_size=15,
                                tickangle = 270,
                                rangeslider_visible=True,
                                side ="top",            #Place the tick labels on the top of the chart
                                showgrid = True,
                                zeroline = True,
                                showline = True,
                                showticklabels = True,
                                tickformat="%x\n",      #Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
                                )
                    )
        
        fig.update_xaxes(tickangle=0, tickfont=dict(family='Rockwell', color='blue', size=15))

        st.plotly_chart(fig, use_container_width=True)  #Display the plotly chart in Streamlit

        st.subheader('Export the interactive Gantt chart to HTML and share with others!') #Allow users to export the Plotly chart to HTML
        buffer = io.StringIO()
        fig.write_html(buffer, include_plotlyjs='cdn')
        html_bytes = buffer.getvalue().encode()
        st.download_button(
            label='Export to HTML',
            data=html_bytes,
            file_name='Gantt.html',
            mime='text/html'
        ) 
    else:
        st.write('---') 

    st.subheader("Heatmap Team by Month")
    heatmap = alt.Chart(Tasks).mark_rect().encode(
       alt.Y('Team'),
       alt.X('monthdate(finish):O'),
       alt.Color('sum(du)', scale=alt.Scale(scheme='redyellowblue'))
    ) 
    st.altair_chart(heatmap, use_container_width=True)

    alt_work = alt.Chart(Tasks).mark_point().encode(
     x=alt.X('du', axis=alt.Axis(title="Duration task")),
     y=alt.X('name', axis=alt.Axis(title="Phase Name")),
     tooltip='name',
     color=alt.Color('Team', legend=None)
     )
   
    st.altair_chart(alt_work, use_container_width=True)

    alt_util = alt.Chart(Tasks).mark_area(interpolate="monotone").encode(
     x=alt.X('monthdate(Start):O'),
     y=alt.Y('sum(du)', axis=alt.Axis(title="Sum hours required")),
     color='Team'
    )
    st.altair_chart(alt_util, use_container_width=True)

    alt_cat = alt_util.mark_line().encode(
     x=alt.X('monthdate(Start):O'),
     y=alt.Y('sum(du)', axis=alt.Axis(title="FTE required")),
     color='Team'
    )
    st.altair_chart(alt_cat, use_container_width=True)

    make_gantt_chart(graph, startTimes, completionTimes, duration, slackTimes)
    #  make_pert_chart(graph, startTimes, completionTimes, slackTimes, criticalPaths)
   
else:
    st.warning('Upload a csv file.')
    with open("tasks.csv", "rb") as file:
      btn = st.download_button(
         label="Download data as CSV",
         data=file,
         file_name='tasks.csv',
         mime='text/csv',
      )


