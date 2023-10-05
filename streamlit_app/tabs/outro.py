import streamlit as st
import pandas as pd
import numpy as np


title = "Conclusion"
sidebar_name = "Conclusion"


def run():

    st.title(title)

    st.markdown(
        """
        C'est la conclusion
        """
    )

    st.write(pd.DataFrame(np.random.randn(100, 4), columns=list("ABCD")))
