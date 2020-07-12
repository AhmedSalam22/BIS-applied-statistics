import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import base64
import seaborn as sns


st.title("Applied Statistics")


@st.cache(persist = True , allow_output_mutation=True)
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
    st.title("Hypothesis Testing")
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

# Simple linear regression
if st.sidebar.checkbox("Simple linear regression" , False):
    st.title("Simple linear regression")
    if file_uploader != None:
        independant_var = st.selectbox("Choose independant (x-axis , explanatory) variable " , list(df.columns))
        dependant_var = st.selectbox("Choose dependant (y-axis , response) variable " , list(df.columns))
        if st.button("Calculate"):
            with st.echo():
                df["intercept"] = 1
                result = sm.OLS(df[dependant_var] , df[["intercept" , independant_var]]).fit().summary()
            with open("slr.txt" , "w+") as f:
                f.write(str(result))
            f = open("slr.txt").read()
            b64 = base64.b64encode(f.encode()).decode()  # some strings <-> bytes conversions necessary here
            st.warning("Please add .txt at the end of the name when you save file otherwise it will not work")
            href = f'<a href="data:file/txt;base64,{b64}">Download result.txt File</a> (click and save as &lt;some_name&gt;.txt)'
            st.markdown(href, unsafe_allow_html=True)
            st.header("scatter plot")
            plt.scatter( x= df[independant_var] , y=df[dependant_var] )
            plt.xlabel("independant variable")
            plt.ylabel("dependant variable")
            st.pyplot()
            st.markdown("#### Correlation coefficients: `{}` ".format(np.corrcoef( df[independant_var] ,df[dependant_var] )[-1][0]))
