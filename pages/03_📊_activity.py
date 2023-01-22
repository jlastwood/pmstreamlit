import streamlit as st
from st_aggrid import AgGrid
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
from  PIL import Image
import io 
import base64
from utilities import reporttitle

# https://levelup.gitconnected.com/how-to-create-a-multi-layer-gantt-chart-using-plotly-e7d7f158938c
#Main interface section 

reporttitle("Activity", st.session_state['thepmheader'])

st.subheader('Gantt and WBS (Work Breakdown Structure)')
uploaded_file = st.file_uploader("WBS is a deliverable orientied hierarchical decomposition of work to be executed by the project team.  Fill out the project plan activities and upload your file here. After you upload the file, you can edit your activities within the app.  If you are performing a fixed price or have a complex project to manage, you will want to create a WBS and map the related activities so that you can assign work concurrently to multiple team members and to link work and notify team members when their work can start.   The tasks are related to the project objectives and completion of the work will create the required deliverables. ", type=['csv'])
st.write("Analyse the results and update the plan and status.  Monitor activities that are late and on the critical path, activities that are late and not assigned, monitor the load of resources.  If you are tracking time, monitor overall estimate to completion rates")
if uploaded_file is not None:
    Tasks=pd.read_csv(uploaded_file, quotechar='"', delimiter=',', skipinitialspace=True)
    Tasks['Start'] = Tasks['Start'].astype('datetime64')
    Tasks['Finish'] = Tasks['Finish'].astype('datetime64')
   
    #st.dataframe(Tasks)
    df = Tasks
 
    grid_response = AgGrid(
        Tasks,
        editable=True, 
        height=300, 
        )

    updated = grid_response['data']
    df = pd.DataFrame(updated) 
    
    #Main interface - section 3
    st.subheader('Step 3: Generate the Gantt chart')
    
    Options = st.selectbox("View Gantt Chart by:", ['Team','Completion Pct'],index=0)
    if st.button('Generate Gantt Chart'): 
        fig = px.timeline(
                        df, 
                        x_start="Start", 
                        x_end="Finish", 
                        y="id",
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
   
else:
    st.warning('Upload a csv file.')
    with open("tasks.csv", "rb") as file:
      btn = st.download_button(
         label="Download data as CSV",
         data=file,
         file_name='tasks.csv',
         mime='text/csv',
      )
 
