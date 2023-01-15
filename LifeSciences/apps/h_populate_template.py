import sys
sys.path.append("../")
from packages import *
from backend import populate_template

def app():
    ################################################# SIDEBAR ##################################################
    st.sidebar.title('Input Parameters')

    patent_file = st.sidebar.file_uploader('Patent File', key = 'thirty') #'output_2022-12-04/b_google_patent.xlsx'

    trials_df = st.sidebar.file_uploader('Trials File', key = 'thirtyone') #'output_2022-12-04/c_clinical_trial.xlsx'

    button = st.sidebar.button('Submit', key='thirtytwo')

    ################################################# MAIN PAGE ################################################
    st.header('Output')

    if(button==True and patent_file is not None and trials_df is not None):
        populate_template().scrape(patent_file, trials_df)

        st.success('Extraction Complete!!')