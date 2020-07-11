import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Applied Statistics")


@st.cache(persist = True)
def read_file(path):
    df = pd.read_csv(path)
    return df

file_uploader = st.file_uploader("Please select your file" , "csv")
if file_uploader != None:
    df = read_file(file_uploader)
    if st.checkbox("Show raw data" , False):
        st.write(df)


hypothesis_testing = st.sidebar.checkbox("Hypothesis Testing" , False)

if hypothesis_testing:
    options = st.sidebar.radio("Select option" , ["Option {x}".format(x=x) for x in range(1,4)])

    x = st.number_input("X value" , 0.0)

    st.markdown(r"""
                **option1** :

                $$H_0: \mu = {x}$$
                $$H_1: \mu \neq {x}$$

                **option2**

                $$H_0: \mu >= {x}$$
                $$H_1: \mu < {x}$$

                **option3**

                $$H_0: \mu <= {x}$$
                $$H_1: \mu > {x}$$

            """.format(x=x))

