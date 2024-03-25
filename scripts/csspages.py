import streamlit as st

def page_media_print():
  st.markdown("""

  <link media="print" rel="stylesheet"
    href="https://www.pagedjs.org/css/pagedjs/interface.min.9b2f873f23cdd2a5e7c0f7a444b030c5.css">
  <script src="https://www.pagedjs.org/js/paged.polyfill.e35b32228f7c0ce277c05a9b4d3db5c5.js" type="module"></script>
  <script>
    window.PagedConfig = { auto: false };
    window.addEventListener("load", function () {
      if (document.querySelector('#print')) {
        document.querySelector('#print').addEventListener("click", preview);
      }
    });
    async function preview() {
      await window.PagedPolyfill.preview();
      window.print();
    }
  </script>

  <style>
    #print {
      position: fixed;
      z-index: 20000;
      padding: .7em;
      right: 10px;
      top: 10px;
      font-size: 1.5em;
      background-color: greenyellow;
      border: 1px dashed red;
    }

    .chapter {
      border: 1px dotted green;
    }

    @media print {
      h1 {
        string-set: title content(text);
      }
      #print {
        display: none;
      }


      @page {
        size: A4;

        @bottom-center {
          content: "Page "counter(page) " of "counter(pages);
          font-size: 4mm;
          color: gray;
        }

        @top-left {
          content: string(title);
          color: gray;
          font-size: 4mm;
        }

      }

      @page :blank {
        @top-left {
          content: none;
        }
      }

      .chapter {
        border: none;

        break-before: right;
      }
    }
  </style>



  """, unsafe_allow_html=True)
