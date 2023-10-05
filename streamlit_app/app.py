from collections import OrderedDict

import streamlit as st

# Global variables in config.py: 
#   TITLE, TEAM_MEMBERS, PROMOTION values
#   path to files
import config
#from streamlit_app.tabs import intro
from tabs import intro, tab2, tab3, tab4, gnn, outro


st.set_page_config(
    page_title=config.TITLE,
    page_icon="https://datascientest.com/wp-content/uploads/2020/03/cropped-favicon-datascientest-1-32x32.png",
)

with open("style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)


# TODO: add new and/or renamed tab in this ordered dict by
# passing the name in the sidebar as key and the imported tab
# as value as follow :
TABS = OrderedDict(
    [
        (intro.sidebar_name, intro),
        (tab2.sidebar_name, tab2),
        (tab3.sidebar_name, tab3),
        (tab4.sidebar_name, tab4),
        (gnn.sidebar_name, gnn),
        (outro.sidebar_name, outro),
    ]
)


def run():
    st.sidebar.image(
        "https://dst-studio-template.s3.eu-west-3.amazonaws.com/logo-datascientest.png",
        width=200,
    )

    tab_name = st.sidebar.radio("", list(TABS.keys()), 0)

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"## {config.PROMOTION}")

    st.sidebar.markdown("### Team members:")
    for member in config.TEAM_MEMBERS:
        st.sidebar.markdown(member.sidebar_markdown(), unsafe_allow_html=True)

    tab = TABS[tab_name]    # Get current tab selected in the sidebar 

    tab.run()               # run the tab code


if __name__ == "__main__":
    run()
