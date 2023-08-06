# TODO 

Python Streamlit app with input form, analytics, and output reports
- [ ] upgrade version of python and modules, bug fixes and update git and deploy to streamlit
    - [ ] upgrade python modules
    - [ ] fix bugs 
        - [ ] on About > AttributeError: st.session_state has no attribute "plpname"
    - [ ] deploy to streamlit 
- [ ] landing page - add a slider, clean up menu options
- [ ] input form - fix bugs, cleanup code
- [ ] utilities - refactoring, bug fixes and cleanup code
- [ ] canvas output page, make three templates like canvanizer, with print to PDF
- [ ] stoplight report - add graphs, outputs and print to PDF
- [ ] add Q&A question/answer lookup using huggingface model
- [ ] risk - set impact, prioirity and status based on events, add reports and outputs, outputs go to stoplight report
- [ ] tasks - read task list from CSV, calculate critical path, late tasks, show resource utilization, and generate reports and output for stoplight report
- [ ] communication - read a communication channel source, calculate sentiment, engagement and topics

# other stuff I did
- .vscode cleanup
    - I got rid of extraneous files
    - I added a launch app config
- got rid of a few other extraneous files

- cleanup
    - got rid of activate folder
    - got rid of package folder 
    - got rid of src folder 
    - got rid of pytest.ini
    - got rid of scripts\app_dev_vscode (my launch.json does this - you can just put breakpoints in there)
    - got rid of run_awesome_stremlit_with_ping.sh
    