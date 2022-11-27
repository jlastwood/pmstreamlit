"""Page for viewing the awesome Project canvas"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import base64
from utilities import reporttitle
from annotated_text import annotated_text
from PIL import Image
import textwrap
import hydralit_components as hc

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Canvas Report",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

# https://gist.github.com/treuille/8b9cbfec270f7cda44c5fc398361b3b1

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    url = pathlib.Path(__file__).parent.parent.parent / bin_file 
    with open(url, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def gradiant_header(color1, color2, color3, content):
  st.markdown(f'<p style="text-align:center;background-image: linear-gradient(to right,{color1}, {color2});color:{color3};font-size:24px;border-radius:5px;">{content}</p>', unsafe_allow_html=True)

def wrapbox(color1, color2, align, text, title, icon):
   text = "<p style='text-align: " + align + "; border-radius: 10px; color: " + color1 + "; background: " + color2 + ";opacity:0.6;'>header</p><p style='text-align: " + align + "; border-radius: 10px; color: " + color1 + "; background: " + color2 + ";'>" + title + "<br/>" + text + "</p>"
   return text

def fancy_box(wch_colour_box, wch_colour_font, iconname, sline, i):
  fontsize = 18
  valign = "left"
  lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

  htmlstr = f"""<p style='background-color: rgb({wch_colour_box});
                        color: rgb({wch_colour_font};
                        font-size: {fontsize}px;
                        border-radius: 7px;
                        padding-left: 12px;
                        padding-top: 18px;
                        padding-bottom: 18px;
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 14px;
                        margin-top: 0;'>{sline}</style></span></p>"""

  st.markdown(lnk + htmlstr, unsafe_allow_html=True)
  #st.write(htmlstr)

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    st.App {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    #st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

# set_bg_hack('background.png')
# initialize session state variables

if 'plnumber' not in st.session_state:
      st.session_state.plnumber = ""
      st.error('Please enter a plan')

theme_scope = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-check-circle'}
font_fmt = {'font-class':'h4','font-size':'50%'}

reporttitle("", st.session_state['thepmheader'])
gradiant_header ('#1aa3ff', '#00ff00', '#ffffff', 'Canvas Report')

cc = st.columns(3)
with cc[0]:
   p1intro = "<br>Project Introduction"
   p1summary = "<sup>" + p1intro + "</sup><br><br>" + st.session_state['thepmplannote']
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-balance-scale", p1summary, "Introduction")
   p2intro = "<br>Benefits"
   p2summary = "<sup>" + p2intro + "</sup><br><br>" + st.session_state['plsbenefits'] 
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-balance-scale", p2summary, "Benefits")
with cc[1]:
   p3intro = "<br>What is the intention behind the project?(Also challenge, cause) Why is the project important - and for whom?  What will be different a year after the project?  What would be missing if we did not do the project?"
   p3summary = "<sup>" + p3intro + "</sup><br><br>" + st.session_state['plspurpose'] + ". " + st.session_state['plsbenchmarks']
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-balance-scale", p2summary, "Purpose")
   scopeintro = "<br>What exactly should the project deliver for CUSTOMERS?  What is it most likely to deliver?  ... a new product/a new service ... new findings/knowledge When is the project successful?  "
   scopesummary = "<sup>" + scopeintro + "</sup><br><br>" + st.session_state['thepmplanscope']  
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-shopping-cart", scopesummary, "Outcome")
with cc[2]:
   riskintro = "<br>Which uncertain events, if they were to occur, would jeopardize or inspire the success of the project? Events that can be influenced are to be considered as ENVIRONMENTAL conditions.  In your risk plan these would be classified as Avoid assuming you have plans in place."
   risksummary = "<sup>" + riskintro + "</sup><br><br>" + 'Project start is ' + 'End is ' + ' Go live is '  + st.session_state['plptimecontingency']  
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-balance-scale", risksummary, "Risks and Opportunities")
   flexintro = "<br>Which characteristics of the project do you consider to be the most flexible? (most flexible on top)"
   flexsummary = "<sup>" + flexintro + "</sup><br><br>" + 'flex array'
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-balance-scale", flexsummary, "Flexibility of Project Constraints")
st.markdown("---")
cb = st.columns(3)
with cb[0]:
   custintro = "<br>Who is a customer? People who...  ... finance the project (sponsor) ... start & finish the project (owner) ... receive the project results (recipient, user) Are there foreseeable conflicts?  "
   custsummary = "<sup>" + custintro + "</sup><br><br>" + 'Project start is ' + 'End is ' + ' Go live is '  + st.session_state['plptimecontingency']  
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-balance-scale", risksummary, "Customer")
with cb[1]:
   msintro = "<br>Which milestones are important? What are the deadlines for ...  ... intermediate results ... important decisions ... visible and measurable successes "
   milestones = st.session_state['thepmmilestones']
   mssummary = "<sup>" + msintro + "</sup><br><br>" + milestones
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-balance-scale", mssummary, "Milestones")
with cb[2]:
   quintro = "<br>What makes the CUSTOMERS really happy in terms of ...  ... the OUTCOME of the project?  ... the MILESTONES on the way there?  ... the kind of information/cooperation in the project?  "
   qusummary = "<sup>" + msintro + "</sup><br><br>" + st.session_state['plsqualitygoal'] + " The next inspection of deliverables is planned " + "Inspector is " + "Project manager is monitoring for schedule, cost and scope and unforseen risks happens every 2 weeks"
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-sun", qusummary, "Quality")
cb = st.columns(3)
with cb[0]:
   timeintro = "<br>When does the project actually start? What is needed? (e.g. preparations, documents, approvals) When is the project really completed? What is needed? (e.g. documents, releases) How flexible are the start and end dates?  "
   timesummary = "<sup>" + timeintro + "</sup><br><br>" + 'Project start is ' + st.session_state['pldstartdate'].isoformat() + 'End is ' + st.session_state['pldenddate'].isoformat() + ' Benefits begin ' + ' Schedule contingency ' + st.session_state['plptimecontingency']  
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-calendar", timesummary, "Schedule")
   costintro = "<br>iHow much money is needed or available...  ... for the implementation?  ... for possibly necessary resources (e.g. server, people)?"
   costsummary = "<sup>" + costintro + "</sup><br><br>" + 'Project start is '
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-moneybag", costsummary, "Budget")
   teamintro = "<br>iHow much money is needed or available...  ... for the implementation?  ... for possibly necessary resources (e.g. server, people)?"
   teamsummary = "<sup>" + teamintro + "</sup><br><br>" + st.session_state['thepmteam']
   fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-handshake", teamsummary, "Team")

