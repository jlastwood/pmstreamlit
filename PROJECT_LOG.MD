# General TODO 
[ ] Python Streamlit app with input form, analytics, and output reports
- [ ] upgrade version of python and modules, bug fixes and update git and deploy to streamlit
    - [X] upgrade python modules
        - [X] identified and updated core modules and dependencies
        - [X] still need to update or remove mystery dependencies (they have to do with scripts)
        - [ ] make notes on extra dependencies
    - [ ] fix bugs 
        - risk
            
    - [ ] deploy to streamlit << I have no idea how you are deploying this :smile:
- [ ] utilities - refactoring, bug fixes and cleanup code
# Pages TODO
## Home 
- [ ] landing page - add a slider, clean up menu options
## Plan
- [ ] input form - fix bugs, cleanup code

## Save Plan
- [ ] tasks - read task list from CSV, calculate critical path, late tasks, show resource utilization, 
## Charter
## Canvas
- [ ] canvas output page, make three templates like canvanizer, with print to PDF
## StopLight
- [ ] stoplight report - add graphs, outputs and print to PDF
## About
## Communication
- [ ] communication - read a communication channel source, calculate sentiment, engagement and topics
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