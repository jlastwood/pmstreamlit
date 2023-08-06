# General TODO 
[ ] Python Streamlit app with input form, analytics, and output reports
- [ ] upgrade version of python and modules, bug fixes and update git and deploy to streamlit
    - [X] upgrade python modules
        - [X] identified and updated core modules and dependencies
        - [X] still need to update or remove mystery dependencies (they have to do with scripts)
        - [ ] make notes on extra dependencies
    - [ ] fix bugs 
    - [ ] deploy to streamlit << I have no idea how you are deploying this :smile:
- [ ] utilities - refactoring, bug fixes and cleanup code

- [ ] are all session state keys used properly? 
Values are stored in session_state variable so that you can use them on other pages. Almost all are working, there might be some values that are labelled with wrong key, but for the most part working

- [ ] confirm this is happening
Values that begin with thepm are intended to be dynamically created based on other information. You can export the values but they are ignored on import as they should always be recalculated.

- [ ] change scripts folder to utilities
- [ ] check how thepm values are calculated
Calculating all thepm values should probably be in the utilities function and not in the main code, so they can be updated from different places. I have a lot of duplication of calculating dates and other variables that could be done once.

- [ ] Fixing - list value input does not work well, you cannot enter a value, save and import. Sometimes you need the list index and sometimes the value.

- [ ] A text area field is intended to be a narrative, this is where the user can ask for assistance in writing from ask (openAI). We form the question and context for the user, then they get a response and can edit it. OpenAI works very well, you can see the code, but I wanted to move to an open source free model, or a lower cost option.

- [ ] Schedule tab - the logic does not work. The purpose is to take the planned start and end and to predict phase milestones and show in a burnup chart with planned and completed.
https://microfluidics.utoronto.ca/gitlab/help/user/project/milestones/burndown_and_burnup_charts.md
On the info page, we know the start date, end date, current phase in progress, and last phase completed, as well as the cadence. Plan and Close are always 2 cadence markers.

- [ ] ROI - formulas could be improved.

- [ ] Cost - formulas could be improved - this calculates CPI, SPI indexes in the utility function. This is an important measure for a PM to monitor.

- [ ] NLTK sentiment analysis and topic information - I am using TextBlob https://textblob.readthedocs.io/en/dev/. If you have another way to do this it is fine. https://www.datacamp.com/tutorial/text-analytics-beginners-nltk.


# Pages TODO
## Home 
- [ ] landing page - add a slider, clean up menu options
## Plan
- [ ] input form - fix bugs, cleanup code
I did build in openai into the plan but then found out they charge for it, and so started to move it to a huggingface model (needs to be finished)
## Save Plan
- [ ] tasks - read task list from CSV, calculate critical path, late tasks, show resource utilization, 
## Charter
## Canvas
- [ ] canvas output page, make three templates like canvanizer, with print to PDF
There is a streamlit feature called elements which I think will do what I am looking for which are canvas layouts (boxes need to be same height) and need to get output to a poster or slides. these outputs need to be able to print and share.
## StopLight
- [ ] stoplight report - add graphs, outputs and print to PDF
## About
## Communication
- [ ] communication - read a communication channel source, calculate sentiment, engagement and topics
Comms analysis needs to get information from a channel, the rate of engagement, and the sentiment. WBS analysis needs to get information such as late tasks, resource utilitization (typicial reports I would see in MS project), need to use Pert diagrams and use the critical path of a project, this is what most task systems lack, gantt charts are not useful for a PM decision (they look pretty) but do not say anything.

## Risk
- [ ] risk - set impact, prioirity and status based on events, add reports and outputs, outputs go to stoplight report
- [ ] bugs
    - [ ] AttributeError: st.session_state has no attribute "plnlistphase"
## WBS


# New Features TODO

- [ ] add Q&A question/answer lookup using huggingface model
- [ ] add a pert diagram somewhere


### other stuff I did
- cleanup
    - .vscode
        - I got rid of extraneous files
        - I added a launch app config
        - got rid of unnecessary launch configs
    - got rid of a few other extraneous files
        - hello_streamlit.py is a tutorial script
        - got rid of discourse_1436.py because its just a selectbox example
        - got rid of deliverycp.py because it looks like an unfinished experiment with pandas that doesn't have much to do with this project (easy to reproduce if it matters)
    - got rid of activate folder (this is all in the virtual env)
    - got rid of scripts\app_dev_vscode (my launch.json does this - you can just put breakpoints in there)
    - got rid of config files and the pylint file
    - awesome streamlit stuff removal
        - got rid of package folder 
        - got rid of src folder 
        - got rid of pytest.ini
        - got rid of run_awesome_stremlit_with_ping.sh
        - got rid of test_runner_app.py because its for awesome streamlit 
        - got rid of extract_resources_markdown.py
        - got rid of ping_awesome_streamlit.py

    - pages
        - got rid of duplicate and unused imports
        - cleaned up home page
        - renamed pages

    - created an experiments folder in scripts where I put stuff that we don't use but might still be cool to look at later

    - got rid of pages.toml because I don't think its doing anything

    - stuff I gitignored
        - secrets.toml
        - credentials.local.toml
        - credentials.prod.toml
        - config.local.toml
        - config.prod.toml

    - renamed pages files to fit with multipage app practices
    - added a project resources md file for useful project reference links