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

reporttitle("Task Analysis", st.session_state['thepmheader'])

st.write("The PM monitor activity analysis is not intended as a replacement to your task management system.  Instead it is used to analyse the information to provide insight into potential issues with tasks started late, or tasks on the critical path not completed")


st.subheader('Gantt and WBS (Work Breakdown Structure)')

uploaded_file = st.file_uploader("WBS is a deliverable orientied hierarchical decomposition of work to be executed by the project team.  Fill out the project plan activities and upload your file here. After you upload the file, you can edit your activities within the app.  If you are performing a fixed price or have a complex project to manage, you will want to create a WBS and map the related activities so that you can assign work concurrently to multiple team members and to link work and notify team members when their work can start.   The tasks are related to the project objectives and completion of the work will create the required deliverables. ", type=['csv'])
st.write("Analyse the results and update the plan and status.  Monitor activities that are late and on the critical path, activities that are late and not assigned, monitor the load of resources.  If you are tracking time, monitor overall estimate to completion rates")

if uploaded_file is not None:
    Tasks=pd.read_csv(uploaded_file, quotechar='"', delimiter=',', skipinitialspace=True, keep_default_na=False)
    st.warning('WBS not found, using phase tasks')
else:
    Tasks = pd.read_csv('files/tasks2.csv', sep=',')

# fix missing values
values = {'pr': 'Start', 'Duration': int(1), 'Assign': 'Team', 'Completion Pct': 0}
Tasks.fillna(value=values, inplace=True)
#new_df = df.drop_duplicates(subset='ORDER ID')
Tasks = Tasks.astype({'Duration':'int'})

assigned = Tasks.Assign.unique().tolist()
max_resources = len(assigned)
max_array = [1]*len(assigned)

for x in assigned:
    Tasks[x] = 0
    Tasks.loc[Tasks["Assign"] == x, x] = 1

p = Project()
#p.add_activity(activity_name='A',activity_duration=2,activity_precedence = [None], activity_resources= [2,4,5])
for index, row in Tasks.iterrows():
   # handle more than one
   var = str(row['pr'])
   prec = list(var.split(" "))
   index = assigned.index(row['Assign'])
   rlist = [0]*len(assigned)
   rlist[index] = 1
   cost = int(row['Duration']*st.session_state.plnavgrate*5)
   p.add_activity(a_desc=row['Description'],activity_name=row['ac'],activity_duration=row['Duration'],activity_precedence = prec, activity_resources= rlist, activity_cost=cost)
#st.table(Tasks)

p.create_project_dict()
PROJECT = pd.DataFrame(p.PROJECT).T
st.write(PROJECT)

Tasks_cpm = p.CPM(verbose=True)
#st.write("CPM report")
#st.table(Tasks_cpm)
Tasks_cp = p.get_critical_path()
st.write("Critical Path")
st.write(str(Tasks_cp))
Tasks_sched = pd.DataFrame(p.cpm_schedule).T
#st.write("Schedule")
#st.table(Tasks_sched)

PL = p.get_priority_list(priority_rule= 'LRD',verbose=True,save=True)
#st.table(PL)

psg = p.PSG(PL,max_resources=max_array,verbose=False)
#st.table(psg)

plt1 = p.plot_network_diagram(plot_type = 'nx')
st.pyplot(plt1, use_container_width=True)

res = p.get_resources()
st.write(res)

startdate = st.session_state.pldstartdate.strftime("%Y-%m-%d")
firstdate = st.session_state.pldstartdate 
todaydate = datetime.now()

#best_heuristic = PROJECT.run_all_pl_heuristics()[psg]

#  start tasks at end of design
Tasks_dates = p.generate_datetime_schedule(solution = psg,start_date=startdate,weekends_work=False,max_resources=max_array,verbose=False)

Project_dates = pd.merge(Tasks_dates, PROJECT, left_index=True, right_index=True)
st.dataframe(Project_dates)
#plt2= p.plot_date_gantt(Tasks_dates, plot_type = 'matplotlib')
#st.pyplot(plt2, use_container_width=True)


#plt3 = p.plot_resource_levels(psg)
#st.pyplot(plt3)

#plt4 = p.RCPSP_plot(psg,resource_id=0)
#st.pyplot(plt4)

# resource consumption

# max resource capacity

if True:
    # do not need this any longer
    graph = defaultdict(list)
    duration = {}

    # input start, duration, type, name
    Tasks['Start'] = Tasks['Start'].astype('datetime64[ns]')
    #Tasks['Finish'] = Tasks['Finish'].astype('datetime64[ns]')
    Tasks['Duration'] = Tasks['Duration'].astype('int')
    Tasks['Duration'] = Tasks['Duration'].fillna(0)
    # force type to int
    firstdate = Tasks['Start'].iloc[0].date()
    # firstdate = (st.session_state.ldstartdate)
    daysoffset = (st.session_state['pldstartdate']-firstdate).days
    # get diff startdate and firstdate
    # Tasks['Start'] = firstdate
    Tasks['Start'] = Tasks['Start'] + pd.Timedelta(days=daysoffset)
    Tasks['Finish'] = Tasks['Start'] + pd.to_timedelta(Tasks['Duration'], unit='D') 
    #Tasks = st.dataframe( Tasks[Tasks['Type'] == 'Milestone'] )
    Tasks.loc[Tasks['pr'] == "Start", 'pr'] = "plan"

    tottasks = len(Tasks) 
    latetasks = closedtasks = cpmlate = 0
    col3, col4, col5, col6 = st.columns(4)
    col3.metric("Total Tasks", tottasks)
    col4.metric("Late Start", latetasks)
    col5.metric("Critical Path Late", cpmlate)
    col6.metric("Completed Tasks", closedtasks)

    #for index, row in Tasks.iterrows():
    #     nodes = row['pr'].split(' ')
    #     for node in nodes:
    #           graph[node].append(row['ac'])
    #     duration[row['ac']] = int(row['Duration'])

    #no_axis_title = axis = alt.Axis(title="")
    #x_scale = alt.Scale(domain=(st.session_state.pldstartdate.isoformat(), st.session_state.pldenddate.isoformat()), nice=10) 

    conditions = [
    (Tasks['Completion Pct'] == 0),
    (Tasks['Completion Pct'] >= 1) & (Tasks['Completion Pct'] < 100),
    (Tasks['Completion Pct'] == 100)
    ]

    # create a list of the values we want to assign for each condition
    values = ['NotStarted', 'InProgress', 'Completed']
    Tasks['Status'] = np.select(conditions, values)
    #st.write(Tasks[(Tasks["Start"] < pd.to_datetime(todaydate)) & (Tasks["Status"] == 'NotStarted')])

    #st.write("Filter or view activities") 

    #grid_response = AgGrid(
    #    Tasks,
    #    editable=False, 
    #    height=300, 
    #    filter=True,
    #    )

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
    st.dataframe(Tasks[(Tasks["Start"] < pd.to_datetime(todaydate)) & (Tasks["Status"] == 'NotStarted')][['ac', 'Duration', 'Assign', 'Start']])
    #display(dataFrame[(dataFrame['Salary']>=100000) & (dataFrame['Age']<40) & dataFrame['JOB'].str.startswith('P')][['Name','Age','Salary']])
    st.subheader("What is the team working on now")
    columns = ['Duration','ac', 'Start']
    st.dataframe( Tasks[Tasks['Status'] == "InProgress"][columns])
    st.subheader("Size of Product Build in days")
    totalbuild = Tasks['Duration'].sum()
    totalcomplete = Tasks.loc[Tasks['Status'] == 'Completed', 'Duration'].sum()
    st.write(totalbuild)
    st.write(totalcomplete)
    #st.metric("Total build", totalbuild, totalcomplete)
    st.dataframe( Tasks[Tasks['Completion Pct'] == 100][columns])

    st.subheader("Resource Load")
    st.write("Show the total resource committment, start and end date of the resource, total hours, complete")
    
    #Main interface - section 3
    st.subheader('Step 3: Generate the Gantt chart')
    Tasks_dates['Task'] = Tasks_dates.index
 
    #Options = st.selectbox("View Gantt Chart by:", ['Assign','Completion Pct'],index=0)
    #if st.button('Generate Gantt Chart'): 
    fig = px.timeline(
                        Tasks_dates, 
                        x_start="ES_date", 
                        x_end="EF_date", 
                        y="Task",
                        color="D",
                        hover_name="Task"
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

        #st.subheader('Export the interactive Gantt chart to HTML and share with others!') #Allow users to export the Plotly chart to HTML
        #buffer = io.StringIO()
        #fig.write_html(buffer, include_plotlyjs='cdn')
        #html_bytes = buffer.getvalue().encode()
        #st.download_button(
        #    label='Export to HTML',
        #    data=html_bytes,
        #    file_name='Gantt.html',
        #    mime='text/html'
        #) 
    #else:
    #    st.write('---') 

    st.subheader("Heatmap Assign by Month")
    heatmap = alt.Chart(Tasks).mark_rect().encode(
       alt.Y('Assign'),
       alt.X('monthdate(Finish):O'),
       alt.Color('sum(Duration)', scale=alt.Scale(scheme='redyellowblue'))
    ) 
    st.altair_chart(heatmap, use_container_width=True)

    alt_work = alt.Chart(Tasks).mark_point().encode(
     x=alt.Y('Duration', axis=alt.Axis(title="Duration task")),
     y=alt.X('Type', axis=alt.Axis(title="Phase Name")),
     tooltip='Type',
     color=alt.Color('sum(Duration)', scale=alt.Scale(scheme='redyellowblue'))
     )
   
    st.altair_chart(alt_work, use_container_width=True)

    alt_util = alt.Chart(Tasks).mark_area(interpolate="monotone").encode(
     x=alt.X('monthdate(Start):O'),
     y=alt.Y('sum(Duration)', axis=alt.Axis(title="Sum hours required")),
     color='Assign'
    )
    st.altair_chart(alt_util, use_container_width=True)

    alt_cat = alt_util.mark_line().encode(
     x=alt.X('monthdate(Start):O'),
     y=alt.Y('sum(Duration)', axis=alt.Axis(title="FTE required")),
     color='Assign'
    )
    st.altair_chart(alt_cat, use_container_width=True)

    #  make_gantt_chart(graph, startTimes, completionTimes, duration, slackTimes)
    #  make_pert_chart(graph, startTimes, completionTimes, slackTimes, criticalPaths)
#import pandas as pd
#import plotly.express as px
#import plotly.figure_factory as ff
#import plotly.graph_objs as go
#import chart_studio
#import chart_studio.plotly as py 
#import chart_studio.tools as tls
# print(df.dtypes)
# print(df.head())
    colors = {'Story' : 'rgb(30,144,255)'
          , 'Feature' : 'rgb(211,211,211)'
          , 'start' : 'rgb(95,158,160)'
          , 'Process' : 'rgb(0,0,128)'
          , 'Process - Date TBD' : 'rgb(211,211,210)'}
    
    orders = list(Tasks['ac'])
    fig = px.timeline(Tasks
                  , x_start="Start"
                  , x_end="Finish"
                  , y="Assign"
                  , hover_name="ac"
#                   , facet_col="Dimension"
#                   , facet_col_wrap=40
#                   , facet_col_spacing=.99
#                   , color_discrete_sequence=['green']*len(df)
                  , color_discrete_sequence=px.colors.qualitative.Prism
                  , opacity=.7
#                   , text="ac"
                  , range_x=None
                  , range_y=None
                  , template='plotly_white'
                  , height=1200
#                   , width=1500
                  , color='Type'
                  , title ="<b>IE 3.0 Gantt Chart 2021</b>"
#                   , color=colors
                 )
    fig.update_layout(
    bargap=0.5
    ,bargroupgap=0.1
    ,xaxis_range=[Tasks.Start.min(), Tasks.Finish.max()]
    ,xaxis = dict(
        showgrid=True
        ,rangeslider_visible=True
        ,side ="top"
        ,tickmode = 'array'
        ,dtick="M1"
        ,tickformat="Q%q %Y \n"
        ,ticklabelmode="period"        
        ,ticks="outside"
        ,tickson="boundaries"
        ,tickwidth=.1
        ,layer='below traces'
        ,ticklen=20
        ,tickfont=dict(
            family='Old Standard TT, serif',size=24,color='gray')
        ,rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
            ,x=.37
            ,y=-.05
            ,font=dict(
                family="Arial",
                size=14,
                color="darkgray"
    )))
    
    ,yaxis = dict(
        title= ""
        ,autorange="reversed"
        ,automargin=True
#         ,anchor="free"
        ,ticklen=10
        ,showgrid=True
        ,showticklabels=True
        ,tickfont=dict(
            family='Old Standard TT, serif', size=16, color='gray'))
    
    ,legend=dict(
        orientation="h"
        ,yanchor="bottom"
        ,y=1.1
        ,title=""
        ,xanchor="right"
        ,x=1
        ,font=dict(
            family="Arial"
            ,size=14
            ,color="darkgray"))
 )
    fig.update_traces( #marker_color='rgb(158,202,225)'
                   marker_line_color='rgb(8,48,107)'
                  , marker_line_width=1.5, opacity=0.95)
    fig.update_layout(
    title="<b>IE 3.0 Gantt Chart 2021</b>",
    xaxis_title="",
#     margin_l=400,
    yaxis_title="Initiatives",
#     legend_title="Dimension: ",
    font=dict(
        family="Arial",
        size=24,
        color="darkgray"
    )
    )
#    st.write(fig.show())

# fig.write_html("C:/Users/maxwell.bade/Downloads/ie_3_gantt.html")
else:
    st.warning('Upload a csv file.')
    with open("files/tasks.csv", "rb") as file:
      btn = st.download_button(
         label="Download data as CSV",
         data=file,
         file_name='tasks.csv',
         mime='text/csv',
      )
    df = pd.read_csv('files/tasks.csv', sep=',')
    st.dataframe(df)

