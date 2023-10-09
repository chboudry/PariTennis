import streamlit as st
import pandas as pd
import numpy as np


title = "Interprétabilité"
sidebar_name = "Interprétabilité"


def run():

    st.title(title)

    st.markdown(
        """
        

        """
    )

    st.write(pd.DataFrame(np.random.randn(100, 4), columns=list("ABCD")))
