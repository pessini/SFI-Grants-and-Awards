import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import socket
import pandas as pd
import numpy as np

# -------------- SETTINGS --------------
page_title = "SFI - Grants & Awards"
page_subtitle = "SFI - Grants & Awards"
page_icon = ":mortar_board:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "wide" # Can be "centered" or "wide". In the future also "dashboard", etc.
#---------------------------------#
# Page layout
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.header(page_subtitle)
#---------------------------------

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
                /*#MainMenu {visibility: hidden;}*/
                /*footer {visibility: hidden;}*/
                /* header {visibility: hidden;} */
                .row_heading.level0 {display:none}
                .blank {display:none}
                a.btn {
                    color: #fff;
                    background-color: #206b82;
                    text-decoration: none;
                    text-align: center;
                    padding: 6px 12px 12px 14px; /* top right bottom left */
                    font-size: 16px;
                    border-radius: 8px;
                }
                a.btn:hover{
                    opacity: 90%;
                    text-decoration: none;
                    color: #fff;
                }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#####################################################
##### Trick to hide table and dataframe indexes #####
# .row_heading.level0 {display:none}
# .blank {display:none}

# --- NAVIGATION MENU ---
with st.sidebar:
    st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/images/SFI_logo_2017__Dual(long)_CMYK.png?raw=true', 
             use_column_width='always')
    # st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/images/sfi-logo.svg?raw=true', use_column_width='always')
    st.write('---') # separator
    
    selected = option_menu(
        # menu_title="Menu",
        menu_title=None,
        options=["About", "Awards Distribution", "Gender Equality"],
        icons=["award", "geo-alt", "gender-ambiguous"],  # https://icons.getbootstrap.com/
        # orientation="vertical",  # "horizontal" or "vertical"
        menu_icon="menu-up", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "steelblue", "font-size": "20px"}, 
            "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#69b3a2"},
        }
    )
    
    footer_github = """<div style='position: fixed; bottom:10px; width:100%;'>
    <img title="GitHub Mark" src="https://github.com/pessini/avian-flu-wild-birds-ireland/blob/main/img/GitHub-Mark-64px.png?raw=true" 
    style="height: 32px; padding-right: 15px" alt="GitHub Mark" align="left"> 
    <a href='https://github.com/pessini/moby-bikes' target='_blank'>GitHub Repository</a> <br>Author: Leandro Pessini
    </div>"""
    st.markdown(footer_github, unsafe_allow_html=True)

#---------------------------------#

def host_is_local(hostname, port=None):
    """returns True if the hostname points to the localhost, otherwise False."""
    if port is None:
        port = 22  # no port specified, lets just use the ssh port
    hostname = socket.getfqdn(hostname)
    if hostname in ("localhost", "0.0.0.0"):
        return True
    localhost = socket.gethostname()
    localaddrs = socket.getaddrinfo(localhost, port)
    targetaddrs = socket.getaddrinfo(hostname, port)
    for (family, socktype, proto, canonname, sockaddr) in localaddrs:
        for (rfamily, rsocktype, rproto, rcanonname, rsockaddr) in targetaddrs:
            if rsockaddr[0] == sockaddr[0]:
                return True
    return False

# Check if it is local or remote
if socket.gethostname() == 'MacBook-Air-de-Leandro.local': # my mac
    APP_PATH = '/Users/pessini/Dropbox/Data-Science/moby-bikes/dashboard/'
elif socket.gethostname() == 'lpessini-mbp': # work
    APP_PATH = '/lpessini/SFI-Grants-and-Awards/deployment/'
else: # remote
    APP_PATH = '/app/moby-bikes/dashboard/'


#------- About --------#  
if selected == "About":

    st.write('''The two datasets analized on this project were provided by 
             [Ireland's Open Data Portal](https://data.gov.ie/). The portal helds public data from Irish Public Sectors 
             such as Agriculture, Economy, Housing, Transportation etc.\n''')

    st.write('''### Datasets''')
    st.write('''
             The first dataset is [Science Foundation Ireland Grant Commitments][1] and it details all STEM (science, technology, engineering and maths) research and ancillary projects funded by Science Foundation Ireland (SFI) since its foundation in 2000. For more information, check out the [Data Dictionary][3] available.
             
            The second one, [SFI Gender Dashboard][2], includes SFI research programmes from 2011 that were managed end-to-end in SFI's Grants and Awards Management System and reflects a binary categorisation of gender, e.g. male or female between 2011 and 2018. For more information, check out the [Data Dictionary][4] available.

            [1]: https://data.gov.ie/dataset/science-foundation-ireland-grant-commitments
            [2]: https://data.gov.ie/dataset/sfi-gender-dashboard-2019
            [3]: https://www.sfi.ie/about-us/governance/open-data/Science-Foundation-Ireland-Grant-Commitments-Metadata.pdf
            [4]: http://www.sfi.ie/about-us/women-in-science/gender/SFI-Gender-Dashboard-Data-Summary.pdf
             ''')


#------- Awards Distribution --------#
if selected == "Awards Distribution":
    # st.header('Demand Forecasting')
    st.subheader("Awards Distribution")

    st.write('''This report will provide an overview of awards applied by [Science Foundation Ireland (SFI)](https://www.sfi.ie/) which is the national foundation for investment in scientific and engineering research. The data provided covers a period of time from 2000 to 2019.

The Agreed Programme for Government, published June 2002, provided for establishing SFI as a separate legal entity. In July 2003, SFI was established on a statutory basis under the Industrial Development (Science Foundation Ireland) Act, 2003.

SFI provides awards to support scientists and engineers working in the fields of science and engineering that underpin biotechnology, information and communications technology and sustainable energy and energy-efficient technologies.

The **focus** of this report is on research funding and **geographical distribution** of **grant awardees**.''')

    st.write('''### Dataset''')
    # st.caption('Data from the past three months')
    awards_dist = pd.read_csv('data/Open-Data-Final.csv')
    st.dataframe(awards_dist, use_container_width=True)

#------- Gender Equality --------#  
if selected == "Gender Equality":
    # st.header('Demand Forecasting')
    st.subheader("Gender Equality")

    st.write('''This table shows the predicted bike rentals demand for the next hours based on Weather data.\n''')
    
    
    
    
    
    
    
    
