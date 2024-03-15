"""Page for viewing the awesome Project canvas"""
import pathlib
import streamlit as st
import base64
from PIL import Image
from streamlit_elements import elements, dashboard
from scripts.thepmutilities import reporttitle, gradiant_header, reporttitleonly
from streamlit_extras.grid import grid

def get_first(s):
  # get first sentence in string
  if len(s) > 100:
     sind = s.find('.')
     if sind > 10:
       return s[0: sind] + '.'
     else:
       return s 
  else:
     return s

def split(s):
    thislist = []
    start = 0
    for i in [1,2,3,4,5,6,7,8]:
      txt = str(i) + '.'
      fins = s.find(txt, start)
      if fins > 0:
        end = s.find(":", fins)
        if end < 0:
          end = find + 15
        getstring = s[fins:end]
        thislist.append(getstring)
        start = fins + 3
    return thislist

# Changes:
#   Having a nice print and share image or pdf 
#   streamlit elements better boxes and moving elements
#   button with three canvas options
#     https://canvanizer.com/
#     lean change, customer journey and business model

st.session_state.update(st.session_state)

im = Image.open("assets/images/BlueZoneIT.ico")
st.set_page_config(
      page_title="The PM Monitor Project Canvas",
      page_icon=im,
      layout="wide",
      initial_sidebar_state="collapsed",
)

#hide_decoration_bar_style = '''
#    <style>
#        header {visibility: hidden;}
#    </style>
#'''
#st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.markdown("""
    <style>
        @media print {
            @page {size: A4 landscape; margin: 27mm 16mm 27mm 16mm; }
            body { margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; }
            header {display: none !important;}
            /* Hide the Streamlit menu and other elements you don't want to print */
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            [data-testid="stDecoration"] { display: none !important; }
            [data-testid="stToolbar"] { display: none !important; }
            .css-1iyw2u1 { display: none; }
            .css-15yd9pf { display: none; }
            .css-fblp2m { display: none; }
            .main {
                width: 100vw;
                max-width: 100% !important;
                overflow: visible !important;
            }

            span, p, div, textarea, input {
                color: #textcolor !important;
                word-break: break-all;
            }

            .stMarkdown, .stCodeBlock, [data-testid="caption"], [data-testid="stMarkdownContainer"], [data-testid="stImage"], [data-baseweb="textarea"] {
                max-width: 11in !important;
                word-break: break-all;
                display: block;
                break-inside: avoid;
            }
            #MainMenu{visibility: hidden;} footer{visibility: hidden;} header {visibility: hidden;}
            #root>div:nth-child(1)>div>div>div>div>section>div{padding-top: .2rem;
        }
    </style>
""", unsafe_allow_html=True)

# https://gist.github.com/treuille/8b9cbfec270f7cda44c5fc398361b3b1

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    url = pathlib.Path(__file__).parent.parent.parent / bin_file 
    with open(url, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def wrapbox(color1, color2, align, text, title, icon):
   text = "<p style='text-align: " + align + "; border-radius: 10px; color: " + color1 + "; background: " + color2 + ";opacity:0.6;'>header</p><p style='text-align: " + align + "; border-radius: 10px; color: " + color1 + "; background: " + color2 + ";'>" + title + "<br/>" + text + "</p>"
   return text

# https://css-tricks.com/aspect-ratio-boxes/
def fancy_box(wch_colour_box, wch_colour_font, iconname, sline, i):
  fontsize = 18
  valign = "left"
  lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
  
  aspect = "4 / 3"
  #if len(sline) > 300:
  #  aspect = "1 / 1"
  # st.write(len(sline), padding, i)
  htmlstr = f"""<p style='background-color: rgb({wch_colour_box});
                        color: rgb({wch_colour_font};
                        font-size: {fontsize}px;
                        border-radius: 7px;
                        padding-left: 8px;
                        padding-top: 8px;
                        padding-right: 8px;
                        padding-bottom: 8px;
                        aspect-ratio: {aspect};
                        line-height:25px;'>
                        <i class='{iconname} fa-2x'></i> {i}
                        </style><BR><span style='font-size: 14px;
                        margin-top: 0;'>{sline}</style></span></p>"""

  my_grid.markdown(lnk + htmlstr, unsafe_allow_html=True)
  return(lnk + htmlstr)

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

if 'thepmheader' not in st.session_state:
      st.error('Sorry, plan is missing. Please enter or load a plan')
      st.stop()

#  get the theme colors
color1t = st._config.get_option('theme.primaryColor')
color1b = st._config.get_option('theme.secondaryBackgroundColor')
color1c = st._config.get_option('theme.backgroundColor')
color1d = st._config.get_option('theme.textColor')

theme_scope = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-check-circle'}
font_fmt = {'font-class':'h4','font-size':'50%'}
mySep = ","

gradiant_header ('The PM Monitor Project Canvas')

# 15 elements layout on page
#my_grid = grid(4, [2, 2, 1], 2, 3, 3, 1,  vertical_align="top")
my_grid = grid(4, 3, 2, 2, 3, 1,  vertical_align="top")
#my_grid = grid(2, 2, 2, 2, 2, 2, 2, 1,  vertical_align="bottom")

p1intro = "<br>Project Introduction"
p1summary = "<sup>" + p1intro + "</sup><br><br>" + st.session_state['thepmplannote'].replace('\n', '<br />')   
fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-book", p1summary, "Introduction")
scopeintro = "<br>What exactly should the project deliver for CUSTOMERS?  What is it most likely to deliver?  a new product/a new service new findings/knowledge When is the project successful?  "
scopelist = '.  \n'.join(split(st.session_state.plscopemusthave)) 
scopesummary = "<sup>" + scopeintro + "</sup><br><br>" + scopelist + '.<br />'  
fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-shopping-cart", scopesummary.replace('\n', '<br />'), "Outcome")
p3intro = "<br>What is the intention behind the project?(Also challenge, cause) Why is the project important - and for whom?  What will be different a year after the project?  What would be missing if we did not do the project?"
p3summary = "<sup>" + p3intro + "</sup><br><br>" + st.session_state['plspurpose'].replace('\n', '<br />') + ". " + st.session_state['plsbenchmarks'].replace('\n', '<br />')
fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-file-code", get_first(p3summary), "Purpose")
p4intro = "<br>Are there comparable or similar products or services (benchmarks)?  Which are they?  What do you like about these benchmarks?  What distinguishes this project from them?> "
p4summary = "<sup>" + p4intro + "</sup><br><br>" + st.session_state['plsbenchmarks'].replace('\n', '<br />') 
fancy_box ("0,204,102,.15", "0,0,0,.75", "fas fa-gavel", get_first(p4summary), "Benchmarks")
riskintro = "<br>Which uncertain events, if they were to occur, would jeopardize or inspire the success of the project? Events that can be influenced are to be considered as ENVIRONMENTAL conditions.  In your risk plan these would be classified as Avoid assuming you have plans in place."
risklist = '.  \n'.join(split(st.session_state.plpresourcecontingency)) 
risksummary = "<sup>" + riskintro + "</sup><br><br>" + risklist.replace('\n', '<br />')  
fancy_box ("244,140,148,.25", "0,0,0,.75", "fas fa-crosshairs", risksummary, "Risks and Opportunities")
flexintro = "<br>Which characteristics of the project do you consider to be the most flexible?  Projects that have flexibilty to adjust to constraints or unexpected issues are more successful.  When risks are high it is important to have contingency plans. "
impactlist = ['High','Very Low', 'Low', 'Moderate', 'High', 'Very High']
flexsummary = "<sup>" + flexintro + "</sup><br><br>" + "<br>Scope Impact " + impactlist[st.session_state.plnscoperange] + "<br>Schedule Impact " + impactlist[st.session_state.plnschedulerange] + "<br>Cost Impact " + impactlist[st.session_state.plnbudgetrange] + "<br>Team Impact " + impactlist[st.session_state.plnteamrange] + "<br>Resource Impact " + impactlist[st.session_state.plnresourcerange]
fancy_box ("244,140,148,.25", "0,0,0,.75", "fas fa-check", flexsummary, "Flexibility of Project Constraints")
envintro = "<br>Known forces, conditions, events and people influencing the project.  Who/what supports the project?  Who/what obstructs the project?"
envsummary = "<sup>" + envintro + "</sup><br><br>" + "Technology deliverables provided by services - " + ', '.join(st.session_state.plmlistscopeoption) + "  The quality inspector supports the customer and team - " + ', '.join(st.session_state.plmlistqualitytypes)
fancy_box ("244,140,148,.25", "0,0,0,.75", "fas fa-thermometer", envsummary, "Environment")
milestones = st.session_state['thepmmilestones'] 
   #mssummary = "<sup>" + msintro + "</sup><br><br>" + " ".join(milestones.values.tolist())
msintro = "<br>Which milestones are important? What are the deadlines for ...  ... intermediate results ... important decisions ... visible and measurable successes "
mssummary = "<sup>" + msintro + "</sup><br><br>" + "Design " + st.session_state.plddesigndate.isoformat() + "<br/> Build " + st.session_state.pldbuilddate.isoformat() + "<br/> Inspect " + st.session_state.pldinspectdate.isoformat() + "<br/> Accept " + st.session_state.pldacceptdate.isoformat() + "</sup><br><br>" 
fancy_box ("120,173,214,.25", "0,0,0,.75", "fas fa-tasks", mssummary, "Milestones")
quintro = "<br>What makes the CUSTOMERS really happy in terms of the OUTCOME of the product (besides the project is delivered on time and on budget)? The MILESTONES on the way there?  The kind of information/cooperation in the project?  "
qusummary = "<sup>" + quintro + "</sup><br><br>" + st.session_state['plsqualitygoal'].replace('\n', '<br>') + "<br><br>" 
   #qusummary = "<sup>" + quintro + "</sup><br><br>" + st.session_state['plsqualitygoal'].replace('\n', '<br>') + "<br><br>"+  st.session_state['thepmquality'] 
fancy_box ("120,173,214,.2", "0,0,0,.75", "fas fa-signal", get_first(qusummary), "Quality")

timeintro = "<br>When does the project actually start? What is needed? (e.g. preparations, documents, approvals) When is the project really completed? What is needed? (e.g. documents, releases) How flexible are the start and end dates?  "
timesummary = "<sup>" + timeintro + "</sup><br><br>" + 'Project start is ' + st.session_state['pldstartdate'].isoformat() + '  End is ' + st.session_state['pldenddate'].isoformat() + ' Inspection date is ' + st.session_state['pldinspectdate'].isoformat() + ' Deliverables ' + ', '.join(st.session_state.plmlistscopelist)  
fancy_box ("120,173,214,.25", "0,0,0,.75", "fas fa-calendar", timesummary, "Schedule")
risklist = ["High", "Low", "Low", "Moderate", "High", "High"]
costintro = "<br>How much money is needed or available...  ... for the implementation?  ... for possibly necessary resources (e.g. server, people)?"
costsummary = "<sup>" + costintro + "</sup><br><br>  The planned investment in Product Design and Delivery is " + str(st.session_state.plnbudget) + ' The project controller is ' + st.session_state.plpfinancename
fancy_box ("120,173,214,.25", "0,0,0,.75", "fas fa-bolt", costsummary, "Budget")
custintro = "<br>Who is a customer? People who...  ... finance the project (sponsor) ... start & finish the project (owner) ... receive the project results (recipient, user) Are there foreseeable conflicts?  "
custsummary = "<sup>" + custintro + "</sup><br><br>"  + st.session_state['thepmusers'].replace('\n', '<br />')  
fancy_box ("239,209,100,.25", "0,0,0,.75", "fas fa-paper-plane", custsummary, "Users")
teamintro = "<br>Who is in it/should be there?  ... in the Core-Team ... in the extended team ... as external partner ... as contact person & decision maker"
teamsummary = "<sup>" + teamintro + "</sup><br><br>" + st.session_state.thepmteam.replace('\n', '<br />')   
fancy_box ("239,209,100,.25", "0,0,0,.75", "fas fa-handshake", teamsummary, "Team")
resintro = "<br>What resources does the project need to be implemented? (excl. time and knowledge)"
ressummary = "<sup>" + resintro + "</sup><br><br>" + mySep.join(st.session_state.plmlistscopeoption) 
fancy_box ("239,209,100,.25", "0,0,0,.75", "fas fa-space-shuttle", ressummary.replace(',', '<br />'), "Resources")

successmsg = f'The PM Monitor project canvas poster presented by {st.session_state.plpmname} on {st.session_state.pldcharterdate}.  Thank you for using The PM Monitor. thepmmonitor.streamlit.app.  '
my_grid.success(successmsg)

# To capture the screen
# image = pyscreenshot.grab()

# st.image(image)  
# To display the captured screenshot
# image.show()
  
# To save the screenshot
#img = image.save("GeeksforGeeks.png")

# btn = st.download_button(
#       label="Download image",
#       data=image,
#       file_name="imagename.png",
#       mime="image/png")
#  this does not take screenshot, only print static contents
#converter.convert('http://localhost:8501/Canvas', 'canvas.pdf')

#with open("canvas.pdf", "rb") as pdf_file:
#    PDFbyte = pdf_file.read()
#
#st.download_button(label="Export_Report",
#                    data=PDFbyte,
#                    file_name="canvas.pdf",
#                    mime='application/octet-stream')
