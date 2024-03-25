import streamlit as st

def page_media_print():
  st.markdown("""
    <style>
        @media print {
            @page {
                size: A4 portrait; 
                margin: 0; 
            }
            body { margin: 0; padding-top: 10px; display: inline; overflow:visible; }
            header {display: none !important;}
            header {visibility: hidden;}
            /* Hide the Streamlit menu and other elements you don't want to print */
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            [data-testid="stDecoration"] { display: none !important; }
            [data-testid="stToolbar"] { display: none !important; }
            .css-1iyw2u1 { display: none; }
            .css-15yd9pf { display: none; }
            .css-fblp2m { display: none; }
            .main {
                max-width: 100% !important;
            }
            .stHeadingContainer {
              page-break-before: always;
            }
            a::after {
              content: " (" attr(href) ")";
            }
            @bottom-right {
                padding-right:20px;
                content: "Page " counter(page);
            }
            @bottom-left {
               content: "Page " counter(page) " of " counter(pages);
            }
            footer {
               position: fixed;
               bottom: 0;
               content: "Page " 
            }
            h3 {
              page-break-before: always;
            }
            span, p, div, textarea, input {
                color: #textcolor !important;
                word-break: normal;
            }
            h6 {
              page-break-after: always;
            }
            .stMarkdown, .stCodeBlock, [data-testid="caption"], [data-testid="stMarkdownContainer"], [data-testid="stImage"], [data-baseweb="textarea"] {
                max-content: 80% !important;
                word-break: normal;
                break-inside: avoid;
                font-size: 10px;
            }
            #MainMenu{visibility: hidden;} footer{visibility: hidden;} header {visibility: hidden;}
            #root>div:nth-child(1)>div>div>div>div>section>div{padding-top: .2rem;
        }
    }
    </style>
  """, unsafe_allow_html=True)
