import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import base64
import seaborn as sns
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor

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
    options = st.sidebar.radio("Select option" , ["Option {x}".format(x=x) for x in range(1,7)])

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

                **option4**
                $$H_0: \mu_e <= \mu_c$$
                $$H_1: \mu_e > \mu_c$$    

                **option5**
                $$H_0: \mu_e >= \mu_c$$
                $$H_1: \mu_e < \mu_c$$   

                **option6**
                $$H_0: \mu_e - \mu_c = 0$$ 
                $$H_1: \mu_e - \mu_c != 0$$   

            """.format(x=x))
    if options in ["Option 1" , "Option 2" , "Option 3"] and file_uploader != None:
        controler = st.selectbox("Select the Controler group" , list(df.columns))
    elif options in ["Option 4" , "Option 5" , "Option 6"] and file_uploader != None:
        controler = st.selectbox("Select the Controler group" , list(df.columns))
        experiment = st.selectbox("Select the experiment group" , list(df.columns))
    if st.button("Calculate"):

        sampling_dist = []
        my_bar = st.progress(0)
        p = st.empty()
        with st.echo():
            if options in ["Option 1" , "Option 2" , "Option 3"]:
                #Generate Normal distrubution from bootstraping 
                for i in range(10000):
                    p.text ("In progress... {:.2f} %".format(i / 10000 * 100))
                    sample = df.sample(df.shape[0], replace = True)
                    sample_mean = sample[controler].mean()
                    sampling_dist.append(sample_mean)
                    my_bar.progress(i/10000)
            elif options in ["Option 4" , "Option 5" , "Option 6"]:
                    for i in range(10000):
                        p.text ("In progress... {:.2f} %".format(i / 10000 * 100))
                        sample = df.sample(df.shape[0], replace = True)
                        sample_mean1 = sample[controler].mean()
                        sample_mean2 = sample[experiment].mean()

                        sampling_dist.append(sample_mean2 -  sample_mean1)
                        my_bar.progress(i/10000)
        
    
            # assume the null value is True
            null_vals = np.random.normal(x, np.std(sampling_dist), 10000)

            #visualize data
            plt.figure(figsize=[15,10])
            plt.subplot(1,2,1)
            plt.hist(sampling_dist)
            plt.title("sampling distribution from bootsstraping")

            plt.subplot(1,2,2)
            plt.hist(null_vals)
            plt.title("if we assume the null value is True then the distibution looks like")

            obs_mean = df[controler].mean()

            plt.axvline(x=obs_mean, color = 'red'); # where our sample mean falls on null dist
            plt.axvline(x= x - (obs_mean - x), color = 'red'); # where our sample mean falls on null dist

            st.pyplot()

        if options == "Option 1" or options == "Option 6":
            with st.echo():
                # probability of a statistic higher than observed
                prob_more_extreme_high = (null_vals < obs_mean).mean()             
                # probability a statistic is more extreme lower
                prob_more_extreme_low = (x - (obs_mean - x) < null_vals).mean()
                pval = prob_more_extreme_low + prob_more_extreme_high
                st.markdown("Pval =  `{}`".format(pval))
        elif options in ["Option 3" , "Option 4"]:
            with st.echo():
                pval = (null_vals > obs_mean).mean()
                st.markdown("Pval =  `{}`".format(pval))
        elif options == "Option 2" or options == "Option 5":
            with st.echo():
                pval = (null_vals < obs_mean).mean()
                st.markdown("Pval =  `{}`".format(pval))
# regression
if st.sidebar.checkbox("regression" , False):
    linearOrLogistic = st.sidebar.radio("Type of regression" , ["linear regression","Logistic regression"])
    st.title(linearOrLogistic)
    if file_uploader != None:

        if st.radio("Do you want to include the categorical variable into your consideration" , ["No" , "Yes"]) == "Yes":
            if linearOrLogistic == "linear regression":
                st.warning("""
                when you create dummy variables using 0, 1 encodings, you always need to drop one of the columns from the model to make sure your matrices are full rank (and that your solutions are reliable from Python).

    The reason for this is linear algebra. Specifically, in order to invert matrices, a matrix must be full rank (that is, all the columns need to be linearly independent). Therefore, you need to drop one of the dummy columns, to create linearly independent columns (and a full rank matrix).
                يعنى لو أنت عاوز تضع البيانات النصية فى عين الاعتبار ما تعمل اعمده من صفر ل واحد تمثل المتغير هيكون موجود ولا لاء
                فى عمود هتحذفه اللى احنا هنقارن على اساسه لنفترض عندنا  بيانات مثل الشرق والغرب يبقى هنعمل عمودين كل عمود بيمثل وجود المتغير او لاء بقيمة صفر وواحد
                بعد كده هنحذف عمود منهم اللى هو هنقارن على اساسة ..خلاصة القول ما تشغلش بالك بس حبيت اوضح الفكرة 
            لما تيجى تضع البيانات النصية فى عين الاعتبار هتحدد الcolumn
            الذى يحتوى على هذه البيانات وبعدين هتختار الاساس اللى هتقارن عليه واحد منهم لو معملتش كده يبقى النتيجة مش شغالة
            الbase line ده 
            هيكون هو نفسه ال intercept
                
           
            بالمختصر المفيد لازم تستبعد واحد من المتغيرات النصية  واللى  انت هتستبعده هو اللى انت  هتقارن على اساسه 
           وده لكل عمود يحتوى على عدد من البيانات وليكن عمود الفرع يحتوى على الفرع ا و ب و س 
           يبقى لازم نستبعد فرع فى المتغير المستقل والمتغير ده هو اللى بنقارن على اساسه وليكن س
           طيب لو عندى عمود بيتحوى على بيانات مثل الشركة ا و ب وعاوزين نقارن بيهم هما كمان نفس الوضع لازم نستبعد واحد واللى هنستبعده هو اللى بنقارن على اساسه 

                """)
            dummy_variables = st.multiselect("Select your dummy variables" , list(df.columns))
            if st.checkbox("Convert into dummy variable" , False):
                with st.echo():
                    # code for convert categorical variable into  dummy 
                    try:
                        df_new = pd.get_dummies(df[dummy_variables])
                        df = df.join(df_new)    
                        st.success("Convert successfuly")
                        if st.checkbox("Do you Want to see a Sample" , False):
                            st.write(df.sample(10))
            
                    except ValueError as identifier:
                        st.error(identifier)
                        st.error("Failed to convert")



        # st.write(df)
        independant_var = st.multiselect("Choose independant (x-axis , explanatory) variable " , list(df.columns))
        dependant_var = st.selectbox("Choose dependant (y-axis , response) variable " , list(df.columns))

        # "Issue with Multi regression model"
        if  linearOrLogistic == "linear regression"   and st.checkbox("Issue with Multi regression model" , False):
            st.warning(" In Multi regression model x-variables just only realted to y variable and we assume there is no relationship between x-variable to another x-variable")
            st.markdown(""" so we will graph the relationship between your selected variable to
             make sure there is no relationship betwwen two indepentant variable if you see this kind or
              relation then your model is incorrect and in this cause we can't use Multi regression model""")
            with st.echo(code_location="below"):
                # code we used to graph
                sns.pairplot(df[independant_var])
            st.pyplot()
            st.markdown("""
                another way to do that using VIF (Variance inflation factor) if this indicator large than (>) 10
                then we should exclude these x-variables from our model otherwise this will be unreliable model (inaccurate model)
            """)
            with st.echo():
                y , x = dmatrices( " {y} ~  {x}".format(y=dependant_var , x = " + ".join(independant_var)) , df , return_type = "dataframe")
                vif = pd.DataFrame()
                vif["VIF Factor"] = [variance_inflation_factor(x.values , i) for i in range(x.shape[1])]
                vif["features"] = x.columns
            st.table(vif)


        if st.button("Calculate"):
            with st.echo():
                df["intercept"] = 1
                if linearOrLogistic == "linear regression":
                    result = sm.OLS(df[dependant_var] , df[independant_var + ["intercept"]]).fit().summary()
                else:
                    result = sm.Logit(df[dependant_var] , df[independant_var + ["intercept"]]).fit().summary2()

            with open("lr.txt" , "w+") as f:
                f.write(str(result))
            st.text(result)
            f = open("lr.txt").read()
            b64 = base64.b64encode(f.encode()).decode()  # some strings <-> bytes conversions necessary here
            st.warning("Please add .txt at the end of the name when you save file otherwise it will not work")
            href = f'<a href="data:file/txt;base64,{b64}">Download result.txt File</a> (click and save as &lt;some_name&gt;.txt)'
            st.markdown(href, unsafe_allow_html=True)
      
        if linearOrLogistic == "Logistic regression":
            if st.checkbox("How you can interpret result from Logistic regression" , False):
                st.markdown("""
                First, you need exponantial this variable  on your calculator you will see  : e ^ variable 
                """)

st.markdown("### Copyright@Ahmed Maher Fouzy Mohamed Salam")