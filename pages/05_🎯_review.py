"""Page for viewing the awesome Project canvas"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import datetime
import base64
#import pandas as pd
from annotated_text import annotated_text
from PIL import Image
import textwrap
import hydralit_components as hc

# https://gist.github.com/treuille/8b9cbfec270f7cda44c5fc398361b3b1

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    url = pathlib.Path(__file__).parent.parent.parent / bin_file 
    with open(url, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

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

def set_media_print():
    page_print = '''
    <style>
    @media print {
      .pagebreak { page-break-inside: avoid; page-break-before: always; }
    }
    }
    </style>
    ''' 
    st.markdown(page_print, unsafe_allow_html=True)
    return

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

def render_svg_example():
#    svg = """
#        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
#            <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
#        </svg>
#    """
    svg = """
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0.1 35.28 2.17" preserveAspectRatio="none"><path d="M0 1.85c2.56-.83 7.68-.3 11.79-.42 4.1-.12 6.86-.61 9.58-.28 2.73.33 5.61 1.17 8.61 1 3-.19 4.73-.82 5.3-.84V.1H0z" fill="%23fbd8c2"/></svg>
#    """
#    st.code(textwrap.dedent(svg), 'svg')
    render_svg(svg)

set_media_print()
set_bg_hack('background.png')
    # initialize session state variables
if 'plnumber' not in st.session_state:
      st.session_state.plnumber = ""
      st.error('Please enter a plan')

theme_scope = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-check-circle'}
font_fmt = {'font-class':'h4','font-size':'50%'}
st.markdown("<h4 style='text-align: center; color: white; background: grey;'>The PM Monitor</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white; background: green;'>Goal Setting</h4>", unsafe_allow_html=True)
cc = st.columns(4)
with cc[0]:
      hc.info_card(title='Some heading GOOD', content=st.session_state.plscopenicetohave,theme_override=theme_scope)
      annotated_text("is some text", "8ef")
with cc[1]:
      hc.info_card(title='Users', content=st.session_state.plscopenicetohave,theme_override=theme_scope)
with cc[2]:
      hc.info_card(title='Benefits', content=st.session_state.plscopenicetohave,theme_override=theme_scope)
with cc[3]:
  wch_colour_box = (0,204,102)
  wch_colour_font = (0,0,0)
  fontsize = 18
  valign = "left"
  iconname = "fas fa-asterisk"
  sline = "Observations"
  lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
  i = 123

  htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
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
col4, col5 = st.columns([4, 1])
with col4:
      st.info("Stakeholders :thought_balloon:")
with col5:
      st.success("Risks chart :grinning:")
     # page break
st.markdown("<div class='pagebreak'>Key Factors</div>", unsafe_allow_html=True)
col4, col5 = st.columns(2)
with col4:
      st.info("Team :thought_balloon:")
with col5:
  st.success("Resources :grinning:")
  st.markdown("<div style='break-after: left;'>Key Factors</div>", unsafe_allow_html=True)
  st.markdown("<h1 style=text-align: center; color: white; background: green; break-before: always;'>Goal Setting</h1>", unsafe_allow_html=True)
col4, col5 = st.columns(2)
with col4:
      st.info("Budget :thought_balloon:")
with col5:
      st.success("Actions :grinning:")
st.write("Planning :grinning:")
color1 = '#1aa3ff'
color2 = '#00ff00'
color3 = '#ffffff'
content = 'sample'
st.markdown(f'<p style="text-align:center;background-image: linear-gradient(to right,{color1}, {color2});color:{color3};font-size:14px;border-radius:5px;">{content}</p>', unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: white; background: blue'>Timeframe</h4>", unsafe_allow_html=True)
st.write(":red_circle: :yellow_circle: :green_circle:", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white; background: yellow'>Team</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white; background: pink;'>Environment</h4>", unsafe_allow_html=True)
     #download = st.form_submit_button("Download Analysis")
     #df = pd.DataFrame({'numbers': [1, 2, 3], 'colors': ['red', 'white', 'blue']})
     # d = {'Budget': [plbudget], 'Hours': [plhours]} 
     # st.markdown(get_table_download_link(df), unsafe_allow_html=True)
     #if download:
     #   open('df.csv', 'w').write(df.to_csv())
     # st.success("The download is presented in another tab,  thank you for using the PM monitor")
     # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/


