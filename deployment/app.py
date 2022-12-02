import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import pathlib
from bs4 import BeautifulSoup
import logging
import shutil

# -------------- SETTINGS --------------
page_title = "Science Foundation Ireland (SFI) - Grants and Awards"
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

def inject_ga():
    GA_ID = "google_analytics"
    GA_JS = """
    <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FKJ7B5EVFT"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-FKJ7B5EVFT');
</script>"""

    # Insert the script in the head tag of the static template inside your virtual
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID): 
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  
        else:
            shutil.copy(index_path, bck_index)  
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_JS)
        index_path.write_text(new_html)


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
        # menu_title="Menu",
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
    <img title="GitHub Mark" src="https://github.com/pessini/avian-flu-wild-birds-ireland/blob/main/img/GitHub-Mark-64px.png?raw=true" 
    style="height: 28px; padding-right: 8px" alt="GitHub Mark" align="left"> 
    <a href='https://github.com/pessini/moby-bikes' target='_blank'>GitHub Repository</a> <br>Author: Leandro Pessini
    </div>"""
    st.markdown(footer_github, unsafe_allow_html=True)

def main():
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
        st.subheader("An overview of science funding distribution in Ireland")
        
        with st.expander("Table of Contents"):
            st.markdown('''
                        * [1. Introduction](#an-overview-of-science-funding-distribution-in-ireland)
                        * [2. Dataset](#dataset)
                        * [3. Audience](#audience)
                        * [4. Dashboard](#tableau-dashboard)''')

        st.write('''This report will provide an overview of awards applied by [Science Foundation Ireland (SFI)](https://www.sfi.ie/) which is the national foundation for investment in scientific and engineering research. The data provided covers a period of time from 2000 to 2019.

The Agreed Programme for Government, published June 2002, provided for establishing SFI as a separate legal entity. In July 2003, SFI was established on a statutory basis under the Industrial Development (Science Foundation Ireland) Act, 2003.

SFI provides awards to support scientists and engineers working in the fields of science and engineering that underpin biotechnology, information and communications technology and sustainable energy and energy-efficient technologies.

The **focus** of this report is on research funding and **geographical distribution** of **grant awardees**.''')

        st.write('''### Dataset''')
        # st.caption('Data from the past three months')
        awards_dist = pd.read_csv('data/Open-Data-Final.csv')
        st.dataframe(awards_dist, use_container_width=True)
        
        st.write('''### Audience''')
        st.write('''A core principle of data analysis is understanding your audience before designing your visualization. It is important to match your visualization to your viewer’s information needs.

This ad hoc analysis aims to deliver a presentation to the SFI Board Members. The Board has several responsibilities which include the revision of strategies of the Agency and major plans of action. One of their major functions is to establish the Agency's direction and how the resources are allocated.

The dataset used is Science Foundation Ireland Grant Commitments and it details all STEM (science, technology, engineering and maths) research projects funded by Science Foundation Ireland (SFI) since its foundation in 2000. For more information, check out the Data Dictionary available.

Dataset provided by Ireland's Open Data Portal which helds public data from Irish Public Sectors such as Agriculture, Economy, Housing, Transportation etc.''')
        
        st.write('''### Tableau® Dashboard''')
        st.caption('[Awards Distribution](https://public.tableau.com/app/profile/pessini/viz/ScienceFoundationIrelandSFI-AwardsDistribution/AwardsDistributionDashboard)')
        html_temp = """<div class='tableauPlaceholder' id='viz1669992134032' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;ScienceFoundationIrelandSFI-AwardsDistribution&#47;AwardsDistributionDashboard&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ScienceFoundationIrelandSFI-AwardsDistribution&#47;AwardsDistributionDashboard' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;ScienceFoundationIrelandSFI-AwardsDistribution&#47;AwardsDistributionDashboard&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='pt-BR' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1669992134032');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1300px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
        components.html(html_temp, height=1200)
        

    #------- Gender Equality --------#  
    if selected == "Gender Equality":
        # st.header('Demand Forecasting')
        st.subheader("Gender Equality in STEM Research Programmes in Ireland")
        
        with st.expander("Table of Contents"):
            st.markdown('''
                        * [1. Introduction](#gender-equality-in-stem-research-programmes-in-ireland)
                        * [2. Dataset](#dataset)
                        * [3. Audience](#audience)
                        * [4. Dashboard](#tableau-dashboard)''')

        st.write('''This report will provide an overview of gender equality in awards applied by Science Foundation Ireland (SFI) which is the national foundation for investment in scientific and engineering research. The data provided covers a period of time between 2011 and 2018.

The Agreed Programme for Government, published June 2002, provided for establishing SFI as a separate legal entity. In July 2003, SFI was established on a statutory basis under the Industrial Development (Science Foundation Ireland) Act, 2003.

SFI provides awards to support scientists and engineers working in the fields of science and engineering that underpin biotechnology, information and communications technology and sustainable energy and energy-efficient technologies.

The analysis is on gender differences in research grants offered by SFI whether the award was accepted or declined by the applicant.''')
        
        st.write('''### Audience''')
        st.write('''A core principle of data analysis is understanding your audience before designing your visualization. It is important to match your visualization to your viewer’s information needs.

This ad hoc analysis aims to deliver a presentation to the SFI Executive staff, Director of Science for Society. The director has the responsibility for overseeing all Science Foundation Ireland research funding programs and management of funded awards.''')
        
        st.write('''### Tableau® Dashboard''')
        st.caption('[Gender differences in research grant applications](https://public.tableau.com/profile/leandro.pessini#!/vizhome/ScienceFoundationIrelandSFI-Gender/Awards-Gender)')
        html_temp = """<div class='tableauPlaceholder' id='viz1669995414079' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;ScienceFoundationIrelandSFI-Gender&#47;Awards-Gender&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ScienceFoundationIrelandSFI-Gender&#47;Awards-Gender' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;ScienceFoundationIrelandSFI-Gender&#47;Awards-Gender&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='pt-BR' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1669995414079');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1450px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
        components.html(html_temp, height=1200)

if __name__ == "__main__":    
    main()