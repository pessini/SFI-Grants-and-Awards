import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import pathlib
from bs4 import BeautifulSoup
import logging
import shutil
import os

# -------------- SETTINGS --------------
page_title = "Science Foundation Ireland (SFI) - Grants and Awards"
page_subtitle = "🎓 SFI - Grants & Awards"
# page_icon = ":mortar-board:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
page_icon = "🇮🇪"
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

def inject_ga():
    GA_JS = """
    <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FKJ7B5EVFT"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-FKJ7B5EVFT');
</script>"""

    st.markdown(GA_JS, unsafe_allow_html=True)

inject_ga()

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
        # menu_title="Main Menu",
        menu_title=None,
        options=["About", "Awards Distribution", "Gender Equality"],
        icons=["award", "geo-alt", "gender-ambiguous"],  # https://icons.getbootstrap.com/
        # orientation="vertical",  # "horizontal" or "vertical"
        menu_icon="menu-up", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "steelblue", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#69b3a2"},
        }
    )
    
    footer_github = """<div style='position: fixed; bottom:10px; width:100%; font-size: 12px;'>
    <img title="GitHub Mark" src="https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/images/GitHub-Mark-64px.png?raw=true" 
    style="height: 28px; padding-right: 8px" alt="GitHub Mark" align="left"> 
    <a href='https://github.com/pessini/SFI-Grants-and-Awards' target='_blank'>GitHub Repository</a> <br>Author: Leandro Pessini
    </div>"""
    st.markdown(footer_github, unsafe_allow_html=True)

def main():
    #------- About --------#  
    if selected == "About":
        st.subheader("About")
        st.write('''The Agreed Programme for Government, published June 2002, provided for establishing SFI as a separate legal entity. In July 2003, SFI was established on a statutory basis under the Industrial Development (Science Foundation Ireland) Act, 2003.''')
        st.write('''[Science Foundation Ireland (SFI)](https://www.sfi.ie/) provides awards to support scientists and engineers working in the fields of science and engineering that underpin biotechnology, information and communications technology and sustainable energy and energy-efficient technologies.''')

        st.write('''### Datasets''')
        st.write('''
                The first dataset is [Science Foundation Ireland Grant Commitments][1] and it details all STEM (science, technology, engineering and maths) research and ancillary projects funded by Science Foundation Ireland (SFI) since its foundation in 2000. For more information, check out the [Data Dictionary][3] available.
                
                The second one, [SFI Gender Dashboard][2], includes SFI research programmes from 2011 that were managed end-to-end in SFI's Grants and Awards Management System and reflects a binary categorisation of gender, e.g. male or female between 2011 and 2018. For more information, check out the [Data Dictionary][4] available.

                [1]: https://data.gov.ie/dataset/science-foundation-ireland-grant-commitments
                [2]: https://data.gov.ie/dataset/sfi-gender-dashboard-2019
                [3]: https://www.sfi.ie/about-us/governance/open-data/Science-Foundation-Ireland-Grant-Commitments-Metadata.pdf
                [4]: http://www.sfi.ie/about-us/women-in-science/gender/SFI-Gender-Dashboard-Data-Summary.pdf
                ''')
        
        st.success("Project consists in reporting research funding and geographical distribution of grant awardees and gender differences in research grant applications.", 
                   icon="🇮🇪")
        col1, col2 = st.columns(2)
        with col1:
            st.write('''##### Awards Distribution Analysis''')
            st.image('https://pessini.me/SFI-Grants-and-Awards/images/research-grant-approved.jpeg', width=300)
            st.write('''[See Jupyter Notebook](https://pessini.me/SFI-Grants-and-Awards/awards-distribution/)''')
        with col2:
            st.write('''##### Gender differences in research grant applications''')
            st.image('https://pessini.me/SFI-Grants-and-Awards/images/gender_equality.jpeg', width=300)
            st.write('''[See Jupyter Notebook](https://pessini.me/SFI-Grants-and-Awards/gender-equality/)''')
            
        st.write('''---''')
        st.write('''The two datasets analized on this project were provided by 
                [Ireland's Open Data Portal](https://data.gov.ie/). The portal helds public data from Irish Public Sectors 
                such as Agriculture, Economy, Housing, Transportation etc.\n''')
        st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/images/dgi-logo.png?raw=true', width=200)


    #------- Awards Distribution --------#
    if selected == "Awards Distribution":
        st.subheader("An overview of science funding distribution in Ireland")
        st.write('''This report will provide an **overview of awards** applied by Science Foundation Ireland (SFI). The data provided covers a period of time from 2000 to 2019.
                 
The focus of this report is on research funding and **geographical distribution** of **grant awardees**.''')

        st.write('''### Dataset''')
        awards_dist = pd.read_csv('data/Open-Data-Final.csv')
        st.caption(f"""{awards_dist.shape[0]} rows with {awards_dist.shape[1]} columns""")
        st.dataframe(awards_dist.head(5), use_container_width=True)
        
        st.write('''### Audience''')
        st.write('''This ad hoc analysis aims to deliver a presentation to the SFI Board Members. The Board has several responsibilities which include the revision of strategies of the Agency and major plans of action. One of their major functions is to establish the Agency's direction and how the resources are allocated.''')
        
        st.write('''### A few insights''')
        col1, col2 = st.columns(2)
        with col1:
            st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/deployment/images/output_27_0.png?raw=true', use_column_width=True)
        with col2:
            st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/deployment/images/output_46_0.png?raw=true', use_column_width=True)
            
        st.write('''[See Jupyter Notebook](https://pessini.me/SFI-Grants-and-Awards/awards-distribution/)''')
        
        st.write('''### Tableau® Dashboard''')
        st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/images/awards-dist-dashboard.png?raw=true', 
                 use_column_width=True, caption='Image of Tableau® Dashboard')
        
        st.write('''---''')
        with st.expander("Tableau® Embedded"):
            html_temp = """<div class='tableauPlaceholder' id='viz1669992134032' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;ScienceFoundationIrelandSFI-AwardsDistribution&#47;AwardsDistributionDashboard&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ScienceFoundationIrelandSFI-AwardsDistribution&#47;AwardsDistributionDashboard' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;ScienceFoundationIrelandSFI-AwardsDistribution&#47;AwardsDistributionDashboard&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='pt-BR' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1669992134032');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1300px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
            components.html(html_temp, height=1000)
            st.caption('[See on Tableau website](https://public.tableau.com/app/profile/pessini/viz/ScienceFoundationIrelandSFI-AwardsDistribution/AwardsDistributionDashboard)')
        

    #------- Gender Equality --------#  
    if selected == "Gender Equality":
        # st.header('Demand Forecasting')
        st.subheader("Gender Equality in STEM Research Programmes in Ireland")
        st.write('''This report will provide an overview of gender equality in awards applied by Science Foundation Ireland (SFI). The data provided covers a period of time between 2011 and 2018.
                 
The analysis is on **gender differences** in research grants offered by SFI whether the **award was accepted or declined** by the applicant.''')
        
        st.write('''### Dataset''')
        gender_df = pd.read_csv('data/SFIGenderDashboard_TableauPublic_2019.csv')
        st.caption(f"""{gender_df.shape[0]} rows with {gender_df.shape[1]} columns""")
        st.dataframe(gender_df.tail(5), use_container_width=True)
        
        st.write('''### Audience''')
        st.write('''This ad hoc analysis aims to deliver a presentation to the SFI Executive staff, Director of Science for Society. The director has the responsibility for overseeing all Science Foundation Ireland research funding programs and management of funded awards.''')
        
        st.write('''### A few insights''')
        col1, col2 = st.columns(2)
        with col1:
            st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/deployment/images/output_40_0.png?raw=true', use_column_width=True)
        with col2:
            st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/deployment/images/output_35_0.png?raw=true', use_column_width=True)
            
        st.write('''[See Jupyter Notebook](https://pessini.me/SFI-Grants-and-Awards/gender-equality/)''')
        
        st.write('''### Tableau® Dashboard''')
        st.image('https://raw.githubusercontent.com/pessini/SFI-Grants-and-Awards/main/images/gender-dashboard.png?raw=true', 
                 use_column_width=True, caption='Image of Tableau® Dashboard')
        
        st.write('''---''')
        with st.expander("Tableau® Embedded"):
            html_temp = """<div class='tableauPlaceholder' id='viz1669995414079' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;ScienceFoundationIrelandSFI-Gender&#47;Awards-Gender&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ScienceFoundationIrelandSFI-Gender&#47;Awards-Gender' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;ScienceFoundationIrelandSFI-Gender&#47;Awards-Gender&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='pt-BR' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1669995414079');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1450px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
            components.html(html_temp, height=1000)
            st.caption('[See on Tableau website](https://public.tableau.com/profile/leandro.pessini#!/vizhome/ScienceFoundationIrelandSFI-Gender/Awards-Gender)')

if __name__ == "__main__":    
    main()